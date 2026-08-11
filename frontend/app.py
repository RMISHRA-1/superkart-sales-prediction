import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://localhost:7860"

# Page title
st.title("SuperKart System")
st.write(
    "Enter the product and store details below to predict the total sales."
)

# Input fields for product and store data
Product_Weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
Product_Allocated_Area = st.number_input("Product Allocated Area", min_value=0.0, value=0.027)
Product_MRP = st.number_input("Product MRP", min_value=0.0, value=117.08)
Store_Size = st.selectbox("Store Size", ["Small", "Medium", "High"])
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Supermarket Type3", "Departmental Store", "Food Mart"])
Product_Id_char = st.selectbox("Product ID Character", ["FD", "DR", "NC"])
Store_Age_Years = st.number_input("Store Age (Years)", min_value=0, value=16)
Product_Type_Category = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])

# Create JSON payload
product_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Product_Id_char": Product_Id_char,
    "Store_Age_Years": Store_Age_Years,
    "Product_Type_Category": Product_Type_Category
}

# Single Prediction
if st.button("Predict", type='primary'):
    try:
        response = requests.post(
            f"{BACKEND_URL}/v1/predict",
            json=product_data,
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            predicted_sales = result["Sales"]
            st.success(f"Predicted Product Store Sales Total: ₹{predicted_sales:.2f}")
        else:
            st.error("Unable to connect to the prediction API.")
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Cannot connect to backend at {BACKEND_URL}. Make sure the backend is running.")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Batch Prediction
st.subheader("Batch Prediction")

uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    if st.button("Predict for Batch", type='primary'):
        try:
            response = requests.post(
                f"{BACKEND_URL}/v1/predictbatch",
                files={"file": uploaded_file},
                timeout=30
            )

            if response.status_code == 200:
                results = response.json()
                st.success("✅ Predictions completed successfully!")
                
                # Debug: Show what we received
                st.write(f"Received {len(results)} predictions")
                
                try:
                    # Convert dict to DataFrame with proper formatting
                    # Backend returns {"0": 4049.22, "1": 3261.13, ...}
                    rows = []
                    for k, v in sorted(results.items(), key=lambda x: int(x[0])):
                        rows.append({"Row Index": int(k), "Predicted Sales": round(float(v), 2)})
                    
                    df = pd.DataFrame(rows)
                    st.write("📊 Predictions Table:")
                    st.text(df.to_string(index=False))
                    
                    # Add download button
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="⬇️ Download Results as CSV",
                        data=csv,
                        file_name="predictions.csv",
                        mime="text/csv"
                    )

                except Exception as e:
                    st.error(f"❌ Error displaying table: {str(e)}")
                    st.write("Raw JSON Response:")
                    st.json(results)

            else:
                st.error("Unable to connect to the prediction API.")
        except requests.exceptions.ConnectionError:
            st.error(f"❌ Cannot connect to backend at {BACKEND_URL}. Make sure the backend is running.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
