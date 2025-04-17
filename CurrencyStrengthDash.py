import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# --- Data preparation ---
currencies = ["USD", "EUR", "GBP", "AUD", "NZD", "CAD", "CHF", "JPY", "CNY"]
pairs = [f"{b}{q}=X" for b in currencies for q in currencies if b != q]

# Last 20 years
years_range = 20
end_date = datetime.today().date() - timedelta(days=2)
start_date = end_date - relativedelta(years=years_range)

data = yf.download(pairs, start=start_date, end=end_date)["Close"]
data.replace(0, np.nan, inplace=True)
data.dropna(how="any", inplace=True)
log_returns = np.log(data / data.shift(1)).dropna()
log_returns = log_returns[(log_returns.abs() <= np.log(2)).all(axis=1)]


def calculate_strength(lr, currs):
    st = pd.DataFrame(index=lr.index, columns=currs)
    for c in currs:
        buys = [p for p in lr.columns if p.startswith(c)]
        sells = [p for p in lr.columns if p.endswith(c + "=X")]
        bs = lr[buys].sum(axis=1) if buys else 0
        ss = -lr[sells].sum(axis=1) if sells else 0
        st[c] = bs + ss
    return st


strength = calculate_strength(log_returns, currencies)

# --- Dash app ---
app = Dash(__name__)
app.title = "Currency Relative Strength"

# Convert date index to list
dates = list(log_returns.index)
n = len(dates)
# Slider marks (only years, evenly spaced)
step = max(n // 10, 1)
marks = {i: dates[i].strftime("%Y") for i in range(0, n, step)}
marks[n - 1] = dates[-1].strftime("%Y")  # Last point

app.layout = html.Div(
    [
        html.H1(f"Currency Relative Strength (Last {years_range} Years)"),
        dcc.RangeSlider(
            id="date-slider",
            min=0,
            max=n - 1,
            value=[0, n - 1],
            marks=marks,
            allowCross=False,  # Prevent crossover of endpoints
            tooltip={"placement": "bottom", "always_visible": True},
        ),
        dcc.Graph(id="strength-graph"),
    ]
)


@app.callback(Output("strength-graph", "figure"), Input("date-slider", "value"))
def update_graph(slider_range):
    start_idx, end_idx = slider_range
    # Map slider indices to dates
    start_date = dates[start_idx]
    end_date = dates[end_idx]
    # Filter & calculate
    lr_filt = log_returns.loc[start_date:end_date]
    st_filt = calculate_strength(lr_filt, currencies)
    cum = st_filt.cumsum()
    norm = cum.subtract(cum.iloc[0])
    # Plot
    fig = go.Figure()
    for c in currencies:
        fig.add_trace(go.Scatter(x=norm.index, y=norm[c], mode="lines", name=c))
    fig.update_layout(
        title=f"Currency Strength: Cumulative Change from {start_date.date()} to {end_date.date()}",
        xaxis_title="Date",
        yaxis_title="Cumulative Change (Relative to Start Date)",
        template="plotly_white",
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=False)