# Streamlit app for Emergency Vehicle Routing
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="Emergency Vehicle Routing", layout="wide")
st.title("🚑 Emergency Vehicle Routing Simulation")

# -------------------------
# Load Data and Model
# -------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Emergency-Vehicle-Routing-main/all_edge_data_cleaned.csv")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

@st.cache_resource
def load_model():
    try:
        model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
        model = joblib.load(model_path)
        return model
    except Exception as e:
        st.warning("Model not found. Upload model.pkl if you want predictions.")
        return None

traffic_data = load_data()
model = load_model()

# -------------------------
# Sidebar Inputs
# -------------------------
st.sidebar.header("Simulation Controls")
start_point = st.sidebar.text_input("Start Junction", "j1")
end_point = st.sidebar.text_input("End Junction", "j5")

show_raw = st.sidebar.checkbox("Show Raw Traffic Data")

# -------------------------
# Display Traffic Data
# -------------------------
if traffic_data is not None:
    st.subheader("Traffic Data Snapshot")
    st.dataframe(traffic_data.head(20))

    if show_raw:
        st.write("### Full Traffic Data")
        st.dataframe(traffic_data)

    # Aggregated statistics
    st.write("### Traffic Summary by Edge")
    edge_summary = traffic_data.groupby("edge_id").agg({
        "avg_speed": "mean",
        "vehicle_count": "mean",
        "traffic_flow": "mean"
    }).reset_index()
    st.dataframe(edge_summary)

# -------------------------
# Prediction Section
# -------------------------
if model is not None and traffic_data is not None:
    st.subheader("Route Prediction")

    if st.button("Predict Best Route"):
        try:
            # Extract features (example: average per edge)
            features = edge_summary[["avg_speed", "vehicle_count", "traffic_flow"]].values
            preds = model.predict(features)

            edge_summary["Predicted_Congestion"] = preds
            st.write("### Predicted Congestion Levels")
            st.dataframe(edge_summary)

            # Highlight best edge (mock logic)
            best_edge = edge_summary.sort_values("Predicted_Congestion").iloc[0]
            st.success(f"Recommended edge for emergency vehicle: {best_edge['edge_id']}")

        except Exception as e:
            st.error(f"Prediction failed: {e}")

# -------------------------
# File Upload Section
# -------------------------
st.sidebar.subheader("Upload Custom Files")
uploaded_data = st.sidebar.file_uploader("Upload Traffic Data (CSV)", type=["csv"])
if uploaded_data:
    traffic_data = pd.read_csv(uploaded_data)
    st.sidebar.success("Custom data uploaded!")

uploaded_model = st.sidebar.file_uploader("Upload Trained Model (pkl)", type=["pkl"])
if uploaded_model:
    model = joblib.load(uploaded_model)
    st.sidebar.success("Custom model uploaded!")
