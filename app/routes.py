import datetime
import logging
from collections import OrderedDict

from flask import Blueprint, request, jsonify, current_app
from psycopg2 import DatabaseError
from psycopg2.extras import DictCursor

from app.database import get_db_connection

logger = logging.getLogger(__name__)

bp = Blueprint('routes', __name__)


@bp.route("/status")
def status():
    return "Up and running!", 200


@bp.route('/rates', methods=['GET'])
def get_rates():
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    origin = request.args.get('origin')
    destination = request.args.get('destination')

    # Check for missing query parameters
    if not date_from or not date_to or not origin or not destination:
        missing_params = []
        if not date_from:
            missing_params.append('date_from')
        if not date_to:
            missing_params.append('date_to')
        if not origin:
            missing_params.append('origin')
        if not destination:
            missing_params.append('destination')
        logger.error(f"Missing query parameters: {', '.join(missing_params)}")
        return jsonify({'error': f'Missing query parameters: {", ".join(missing_params)}'}), 400

    # Validate input dates
    try:
        date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d').date()
        date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d').date()
    except ValueError as e:
        logger.error(f"Date validation error: {e}")
        return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD format.'}), 400

    try:
        with get_db_connection(current_app) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                query = """
                    WITH all_days AS (
                        SELECT generate_series(%s::date, %s::date, '1 day'::interval) AS day
                    ),
                    price_data AS (
                        SELECT day, AVG(price) AS average_price, COUNT(price) AS price_count
                        FROM prices
                        WHERE day BETWEEN %s AND %s
                        AND orig_code IN (
                            SELECT code FROM ports WHERE code = %s OR parent_slug = %s
                        )
                        AND dest_code IN (
                            SELECT code FROM ports WHERE code = %s OR parent_slug = %s
                        )
                        GROUP BY day
                    )
                    SELECT a.day, 
                           CASE 
                               WHEN p.price_count >= 3 THEN ROUND(p.average_price, 2)
                               ELSE NULL 
                           END AS average_price
                    FROM all_days a
                    LEFT JOIN price_data p ON a.day = p.day
                    ORDER BY a.day;
                """
                cursor.execute(query,
                               (date_from, date_to, date_from, date_to, origin, origin, destination, destination))
                result = cursor.fetchall()

        rates = [OrderedDict([('day', row['day'].strftime('%Y-%m-%d')), ('average_price', row['average_price'])]) for
                 row in result]
        return jsonify(rates)
    except DatabaseError as db_error:
        logger.error(f"Database error: {db_error}")
        return jsonify({'error': 'Database error occurred. Please try again later.'}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'An unexpected error occurred. Please try again later.'}), 500
