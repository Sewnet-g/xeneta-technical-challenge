# Rates API

This project is a Flask-based API to fetch average daily prices for shipping routes. The API allows querying prices based on various parameters including date range, origin, and destination ports or regions.

## Table of Contents
- [Overview](#overview)
- [Data Model](#data-model)
- [API Endpoints](#api-endpoints)
- [Setup](#setup)
  - [Using Docker](#using-docker)
  - [Running Locally](#running-locally)
- [Running Tests](#running-tests)
- [Error Handling](#error-handling)
- [Logging](#logging)

## Overview

The Rates API provides a way to retrieve the average daily prices for shipping routes between ports. This is useful for logistics and shipping companies to analyze price trends and make informed decisions.

`Note`: This project is a technical test as part of the interview process for a Senior Software Developer position at Xeneta.

## Data Model

### Ports

Information about ports, including:
- `code`: 5-character port code (e.g., "CNSGH")
- `name`: Name of the port (e.g., "norway_south_east")
- `parent_slug`: Slug describing which region the port belongs to

### Regions

A hierarchy of regions, including:
- `slug`: A machine-readable form of the region name
- `name`: The name of the region
- `parent_slug`: Slug describing which parent region the region belongs to

### Prices

Individual daily prices between ports, in USD:
- `orig_code`: 5-character origin port code
- `dest_code`: 5-character destination port code
- `day`: The day for which the price is valid
- `price`: The price in USD

## API Endpoints

### GET `/rates`

Retrieve the average prices for each day on a route between port codes or region slugs.

**Parameters:**
- `date_from` (required): Start date (YYYY-MM-DD)
- `date_to` (required): End date (YYYY-MM-DD)
- `origin` (required): Origin port code or region slug
- `destination` (required): Destination port code or region slug

**Response:**
```json
[
    {
        "day": "2016-01-01",
        "average_price": 1212.94
    },
    {
        "day": "2016-01-02",
        "average_price": 1112.88
    },
    {
        "day": "2016-01-03",
        "average_price": null
    }
]
```

### GET `/stats`
This endpoint is used to check health of the API.

## Setup

### Using Docker
1. Create a `.env` file in the root directory of your project. This file should contain the environment variables needed for the application.
   - `Note`: For the purpose of this challenge, the `.env` file will be provided separately.
2.  Build and start the Docker containers:
    ```bash
    docker-compose up --build
    ```

3. The Flask application will be accessible at `http://localhost:5001`.



### Running Locally

1. Ensure you have PostgreSQL installed and running.
2. Create the database and load the sample data:
    ```bash
    createdb ratestask
    psql -U postgres -d ratestask -f data/rates.sql
    ```
3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
4. Set the necessary environment variables and run the Flask app:
    ```bash
    export FLASK_APP=app
    export FLASK_ENV=development
    flask run --host=0.0.0.0 --port=5001
    ```

## Running Tests

Run the tests using:
   ```bash
      python -m unittest discover -s tests
   ```
## Error Handling

The API handles errors gracefully and returns appropriate HTTP status codes with error messages:

- **400 Bad Request**: Missing or invalid parameters
- **500 Internal Server Error**: Unexpected errors or database connection issues

## Logging

Logging is configured using the `logging.json` file. Logs include details about incoming requests, errors, and other significant events.

## Contact
If you have any questions or feedback, you can contact the project author at [Sewnet Gebremedhin](mailto:sewnet.gebremedhin@gmail.com).
