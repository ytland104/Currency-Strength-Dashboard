# Currency Strength Dashboard

A Dash application for visualizing relative currency strength across major currencies over time.

## Features

- Tracks relative strength of 9 major currencies (USD, EUR, GBP, AUD, NZD, CAD, CHF, JPY, CNY)
- Interactive date range selection
- Visualization of cumulative strength changes
- Correlation heatmap between currencies for the selected period

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/ytland104/Currency-Strength-Dashboard.git
   cd Currency-Strength-Dashboard
   ```

2. Create and activate a virtual environment (recommended):
   ```
   # Using venv (Python 3.3+)
   python -m venv venv
   
   # Activate virtual environment
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the Dash application:
```
python CurrencyStrengthDash.py
```

Then open your web browser and go to [http://127.0.0.1:8050/](http://127.0.0.1:8050/) to view the dashboard.

The dashboard consists of two main visualizations:
1. The **Strength Chart** showing the cumulative change in strength for each currency over the selected time period
2. The **Correlation Heatmap** displaying correlation coefficients between currencies in the selected time range

## Data Source

This application uses Yahoo Finance data accessed through the yfinance library to retrieve historical currency pair data.

## License

[MIT](LICENSE)