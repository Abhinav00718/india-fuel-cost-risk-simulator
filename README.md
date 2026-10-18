# India Fuel Cost Risk Simulator

An interactive Python and Streamlit application that explores how
crude oil price shocks and INR/USD exchange-rate movements affect
the estimated rupee cost of crude oil.

## Features

- Interactive oil-price and exchange-rate assumptions
- User-defined oil-price shocks and rupee depreciation scenarios
- Baseline and stressed crude-cost calculations
- Scenario comparison table
- Sensitivity analysis heatmap
- CSV download of scenario results

## Methodology

Estimated crude cost in INR per barrel:

Crude Cost = Oil Price (USD/barrel) × Exchange Rate (INR/USD)

The stressed cost applies percentage shocks to both inputs:

Stressed Cost = Oil Price × (1 + Oil Shock)
                × Exchange Rate × (1 + Rupee Shock)

The combined effect is multiplicative. For example, a 10% oil
price increase and 5% rupee depreciation increase the estimated
cost by 15.5%.

## Data and Limitations

The application uses WTI crude oil prices and the INR/USD exchange
rate as benchmark inputs. WTI is a US crude oil benchmark and does
not represent India's actual imported crude basket, landed cost,
or retail petrol and diesel prices.

The scenarios are deterministic calculations, not forecasts.
Users can change the assumptions to explore alternative outcomes.

## Technology

- Python
- Streamlit
- Pandas
- NumPy
- Plotly

## Run Locally

Install the dependencies:

    pip install -r requirements.txt

Start the application:

    streamlit run app.py
    
