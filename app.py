import requests
import streamlit as st

# URL of the backend API on Render (update if your Render service has a different name)
BACKEND_URL = "https://superkart-api.onrender.com/v1/predict"

st.set_page_config(page_title="SuperKart Sales Forecast", page_icon="🛒")
st.title("SuperKart Sales Forecast")
st.write("Enter product and store details to forecast total sales for that product at that store.")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Product")
    product_id_char = st.selectbox("Product category code", ["FD", "DR", "NC"],
                                   help="FD = food, DR = drinks, NC = non-consumables")
    product_type_category = st.selectbox("Perishability", ["Perishables", "Non Perishables"])
    product_sugar_content = st.selectbox("Sugar content", ["Low Sugar", "Regular", "No Sugar"])
    product_weight = st.number_input("Weight", min_value=0.0, value=12.66)
    product_mrp = st.number_input("MRP (price)", min_value=0.0, value=147.0)
    product_allocated_area = st.number_input("Allocated shelf area (ratio)", min_value=0.0, max_value=1.0, value=0.056, format="%.3f")
with col2:
    st.subheader("Store")
    store_type = st.selectbox("Store type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])
    store_size = st.selectbox("Store size", ["Small", "Medium", "High"])
    store_location_city_type = st.selectbox("City tier", ["Tier 1", "Tier 2", "Tier 3"])
    store_age_years = st.number_input("Store age (years)", min_value=0, value=16)

if st.button("Forecast sales", type="primary"):
    payload = {
        "Product_Weight": product_weight,
        "Product_Sugar_Content": product_sugar_content,
        "Product_Allocated_Area": product_allocated_area,
        "Product_MRP": product_mrp,
        "Store_Size": store_size,
        "Store_Location_City_Type": store_location_city_type,
        "Store_Type": store_type,
        "Product_Id_char": product_id_char,
        "Store_Age_Years": store_age_years,
        "Product_Type_Category": product_type_category,
    }
    with st.spinner("Contacting the forecasting API (the free server may take up to a minute to wake up)..."):
        try:
            response = requests.post(BACKEND_URL, json=payload, timeout=120)
            if response.status_code == 200:
                st.success(f"Forecast total sales: ${response.json()['Sales']:,.2f}")
            else:
                st.error(f"API error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Could not reach the API: {e}")

st.caption("Model: tuned Random Forest (test R² ≈ 0.93). API: Flask on Render. Frontend: Streamlit.")
