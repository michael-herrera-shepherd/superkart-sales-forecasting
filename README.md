# SuperKart Sales Forecasting: From Model to Deployed App

An end-to-end machine learning project: forecasting product-store sales for a four-store retail chain, then serving the model through a REST API and an interactive web app.

**Live app:** LIVE_APP_URL
*(The API runs on a free server that sleeps when idle, so the first forecast may take about a minute.)*

## Problem
SuperKart needs reliable sales forecasts for each product at each store to plan inventory and regional sales strategy. The dataset has ~8,700 product-store records with product attributes (weight, MRP, shelf area, sugar content, type) and store attributes (size, city tier, type, age).

## Approach
| Step | What I did |
|---|---|
| EDA | Univariate and bivariate analysis of sales drivers by product type, price, and store |
| Feature engineering | Product ID prefix (food / drink / non-consumable), perishable vs. non-perishable category, store age |
| Modeling | Random Forest and XGBoost regressors in scikit-learn pipelines (one-hot encoding plus numeric passthrough) |
| Tuning | GridSearchCV with 3-fold cross-validation |
| Deployment | Flask REST API served by Gunicorn in Docker on **Render**, plus a **Streamlit** frontend on Streamlit Community Cloud |

## Results (test set)
| Model | R² | MAPE |
|---|---|---|
| Random Forest | 0.923 | 5.0% |
| **Random Forest (tuned, deployed)** | **0.927** | **5.2%** |
| XGBoost | 0.916 | 5.7% |
| XGBoost (tuned) | 0.917 | 5.7% |


## Business insights
- **One store drives the business:** OUT004 (medium Supermarket Type 2, Tier 2 city) generates about half (51%) of total sales. Its practices are worth benchmarking across the other stores.
- **Weak categories:** Seafood and Breakfast products are consistently low earners, so they are candidates for promotions, bundling, or better shelf placement.
- **Price matters most:** Product MRP is the dominant sales driver, so pricing decisions carry the most forecasting weight.

## Architecture
```
Streamlit app (Streamlit Community Cloud)      frontend/app.py
        │  POST /v1/predict (JSON)
        ▼
Flask API + Gunicorn in Docker (Render)        backend/app.py, backend/Dockerfile
        │
        ▼
scikit-learn pipeline (one-hot encoding → tuned Random Forest), loaded with joblib
```

Example request:
```bash
curl -X POST https://superkart-api.onrender.com/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"Product_Weight": 12.66, "Product_Sugar_Content": "Low Sugar", "Product_Allocated_Area": 0.027,
       "Product_MRP": 117.08, "Store_Size": "Medium", "Store_Location_City_Type": "Tier 2",
       "Store_Type": "Supermarket Type2", "Product_Id_char": "FD", "Store_Age_Years": 16,
       "Product_Type_Category": "Non Perishables"}'
```

## Repository structure
```
SuperKart_Sales_Forecasting.ipynb   EDA, modeling, tuning, and generation of the deployment files
backend/                            Flask API, Dockerfile, pinned requirements, trained model
frontend/                           Streamlit app
```

## How to run
- **Notebook:** open in Google Colab or Jupyter, place `SuperKart.csv` in the working directory (or update the Drive path), and run all cells.
- **API locally:** `cd backend && pip install -r requirements.txt && gunicorn -b 0.0.0.0:10000 app:superkart_api`
- **App locally:** `pip install -r frontend/requirements.txt && streamlit run frontend/app.py` (set `BACKEND_URL` at the top of `frontend/app.py`)

## Tools
Python · pandas · scikit-learn · XGBoost · Flask · Gunicorn · Docker · Streamlit · Render
