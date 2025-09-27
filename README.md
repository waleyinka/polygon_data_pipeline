# Stock Trading Data Pipeline

A Python-based data pipeline that extracts stock market data from Polygon.io API and loads it into Snowflake cloud data warehouse for analytics and trading insights.

## Overview

This project fetches comprehensive stock ticker information from Polygon.io, including company metadata, exchange details, and market data, then loads it directly into Snowflake for downstream analytics and reporting.

## Features

- **Batch Data Extraction**: Fetches up to 1000 stock tickers per request with automatic pagination
- **Rate Limiting**: Implements 15-second delays between API requests to respect Polygon.io limits
- **Cloud Data Warehouse Integration**: Direct loading into Snowflake with proper schema management
- **Automated Scheduling**: Configurable job scheduling for continuous data updates
- **Environment-based Configuration**: Secure credential management via environment variables
- **Error Handling**: Robust data extraction with comprehensive error management

## Architecture

```
Polygon.io API → Python Script → Snowflake Data Warehouse
```

## Prerequisites

- Python 3.10+
- Snowflake account with appropriate permissions
- Polygon.io API key
- WSL2 (for Windows users)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd stock_trading_app
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv my_env
   source my_env/bin/activate  # On Windows WSL
   ```

3. **Install dependencies**
   ```bash
   pip install snowflake-connector-python **python-dotenv** **requests** **schedule**
   ```

## Configuration

1. **Create `.env` file in project root**
   ```bash
   # Polygon.io API Configuration
   POLYGON_API_KEY=your_polygon_api_key_here
   
   # Snowflake Configuration
   SNOWFLAKE_USER=your_username
   SNOWFLAKE_PASSWORD=your_password
   SNOWFLAKE_ACCOUNT=your_account_identifier
   SNOWFLAKE_WAREHOUSE=your_warehouse
   SNOWFLAKE_DATABASE=your_database
   SNOWFLAKE_SCHEMA=your_schema
   SNOWFLAKE_ROLE=your_role
   SNOWFLAKE_TABLE=stock_tickers
   ```

2. **Get your Polygon.io API key**
   - Sign up at [Polygon.io](https://polygon.io/)
   - Generate an API key from your dashboard

3. **Configure Snowflake account**
   - Ensure your Snowflake user has CREATE TABLE and INSERT permissions
   - Note your account identifier format

## 4. Usage (Running the Pipeline)

To run the pipeline and schedule continuous updates:

1.  **Run the script once (Manual Execution):**
    ```bash
    python3 script.py
    ```
2.  **Start the automated scheduler:**
    ```bash
    python scheduler.py
    # This will run the extraction job based on the schedule defined in the file
    ```

## Data Schema

The pipeline extracts the following ticker information:

| Field | Type | Description |
|-------|------|-------------|
| ticker | VARCHAR | Stock symbol |
| name | VARCHAR | Company name |
| market | VARCHAR | Market type (stocks) |
| locale | VARCHAR | Market locale (us) |
| primary_exchange | VARCHAR | Primary exchange code |
| type | VARCHAR | Security type |
| active | BOOLEAN | Trading status |
| currency_name | VARCHAR | Currency (usd) |
| cik | VARCHAR | Central Index Key |
| composite_figi | VARCHAR | Composite FIGI identifier |
| share_class_figi | VARCHAR | Share class FIGI |
| last_updated_utc | TIMESTAMP_NTZ | Last update timestamp |
| date_stamp | VARCHAR | Processing date |

## Project Structure

```
stock_trading_app/
├── script.py              # Main data extraction and loading script
├── scheduler.py           # Automated job scheduler
├── requirements.txt       # List of installed Python dependencies
├── .env                   # Environment variables (create this)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues and questions:
- Review Snowflake and Polygon.io documentation
- Open an issue in the repository