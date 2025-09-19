**polygon-data-pipeline**

Building a batch pipeline that extracts stock market data (tickers) from Polygon.io, ingests it into cloud storage,
and prepares it for downstream analytics.

⚠️ Note: This project is currently ongoing...

______________________________________________________________________________________________________________________________________

**Current Stage**

- ✅ REST API Extraction: Fetching stock tickers and metadata from Polygon.io using Python.
- ✅ Data Export: Writing raw data into CSV file (tickers.csv) with a consistent schema for ingestion.
- ✅ Automated Job Function: Created `run_stock_job()` function in `script.py` that handles the complete data extraction pipeline.
- ✅ Scheduler Implementation: Set up automated scheduling using the `schedule` library to run the stock job every minute via `scheduler.py`.

**Key Features Implemented:**
- **Batch Data Processing**: Fetches up to 1000 tickers per request with pagination support
- **Rate Limiting**: Implements 15-second delays between API requests to respect Polygon.io limits
- **CSV Export**: Automatically writes structured data to `tickers.csv` with consistent schema
- **Automated Execution**: Scheduler runs the job every minute for continuous data updates
- **Error Handling**: Robust data extraction with proper API key management via environment variables
