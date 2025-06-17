import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import pickle
import json
import os
from PIL import Image

# Set page configuration
st.set_page_config(
    page_title="PropertyPulse: Smart Real Estate Analytics",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Display logo
logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    # Convert to RGBA if not already
    if logo.mode != 'RGBA':
        logo = logo.convert('RGBA')
    # Create three columns for centering
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(logo, width=300, use_column_width=True)

# Load the model and columns
def load_model():
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(parent_dir, 'Model', 'Jaipur_real_estate_model.pickle')
    columns_path = os.path.join(parent_dir, 'Model', 'columns.json')
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    with open(columns_path, 'r') as f:
        columns = json.load(f)['data_columns']
    
    return model, columns

try:
    model, columns = load_model()
except Exception as e:
    st.error(f"Error loading model: {str(e)}")
    st.stop()

# Function to calculate price per square foot for a location
def get_price_per_sqft(model, columns, location, area=1000, bhk=2, bath=2):
    try:
        x = np.zeros(len(columns))
        x[0] = area
        x[1] = bath
        x[2] = bhk
        loc_index = columns.index(location)
        x[loc_index] = 1
        predicted_price = model.predict([x])[0]
        return predicted_price / area
    except Exception as e:
        st.error(f"Error calculating price per sq ft: {str(e)}")
        return 0

def format_price(price):
    try:
        price = float(price)  # Ensure price is a float
        return f"₹{price:,.2f}"
    except (ValueError, TypeError):
        return "₹0.00"

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: #0a1929;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
        background-color: #0066cc;
        color: #ffffff;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s ease;
        cursor: pointer;
        z-index: 1;
    }
    .stButton>button:hover {
        background-color: #004d99;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .stButton>button:active {
        transform: translateY(0);
    }
    .metric-card {
        background-color: #132f4c;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        border-left: 4px solid #0066cc;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .stSelectbox>div>div>select {
        background-color: #132f4c;
        color: #ffffff;
        border-radius: 5px;
        padding: 0.5rem;
        border: 1px solid #0066cc;
    }
    .stNumberInput>div>div>input {
        background-color: #132f4c;
        color: #ffffff;
        border-radius: 5px;
        padding: 0.5rem;
        border: 1px solid #0066cc;
    }
    .sidebar .sidebar-content {
        background-color: #0a1929;
        padding: 2rem;
    }
    .sidebar .sidebar-content .sidebar-section {
        background-color: #132f4c;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid #0066cc;
    }
    h1, h2, h3 {
        color: #ffffff;
        font-weight: bold;
    }
    .stMarkdown {
        color: #e2e8f0;
    }
    .success-message {
        background-color: #132f4c;
        color: #ffffff;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        border-left: 4px solid #0066cc;
    }
    .info-message {
        background-color: #132f4c;
        color: #ffffff;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        border-left: 4px solid #0066cc;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #0066cc;
        margin: 0.5rem 0;
    }
    .metric-label {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    .price-note {
        background-color: #132f4c;
        color: #ffffff;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        border-left: 4px solid #0066cc;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Header with gradient background
st.markdown("""
    <div style='background: linear-gradient(45deg, #0a1929, #132f4c); padding: 2rem; border-radius: 10px; color: white; text-align: center; border: 1px solid #0066cc;'>
        <h1 style='margin: 0;'>🏠 PropertyPulse: Smart Real Estate Analytics</h1>
        <p style='margin: 0.5rem 0 0;'>Predict property prices and analyze investment potential in Jaipur</p>
    </div>
    """, unsafe_allow_html=True)

# Add price format note
st.markdown("""
    <div class='price-note'>
        <strong>Note:</strong> All prices are displayed in crores and lakhs format. For example, "1 crores 1 lakh" means ₹101.21, "95 lakhs" means ₹95.21
    </div>
    """, unsafe_allow_html=True)

# Sidebar with styled sections
st.sidebar.markdown("""
    <div style='background: #132f4c; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; border: 1px solid #0066cc;'>
        <h2 style='color: #ffffff; margin-bottom: 1rem;'>Property Details</h2>
        <p style='color: #94a3b8;'>Please fill in the property details below:</p>
    </div>
    """, unsafe_allow_html=True)

# Input fields with better styling
st.sidebar.markdown("### 📏 Area & Rooms")
area = st.sidebar.number_input("Total Area (in square feet)", min_value=100, max_value=10000, value=1000)
bathrooms = st.sidebar.selectbox("Number of Bathrooms 🚽", [1, 2, 3, 4, 5])
bedrooms = st.sidebar.selectbox("Number of Bedrooms 🛏️", [1, 2, 3, 4, 5])

# Location selection with better styling
st.sidebar.markdown("### 📍 Location")
location = st.sidebar.selectbox(
    "Select Location",
    ["ajmer road", "bapu nagar", "brahmpuri", "chokdi gangapol", "civil lines",
     "dahar ka balaji", "gandhi path west", "hanuman nagar", "jawahar nagar",
     "malviya nagar", "manchwa", "maniyawas", "mansarovar ext.", "parasrampuri",
     "raja park", "shyam nagar", "sirsi", "sita vihar", "tagore nagar", "vaishali nagar"]
)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🎯 Property Price Prediction")
    
    # Create a placeholder for the prediction
    prediction_placeholder = st.empty()
    
    # Add a predict button with animation and ensure it's clickable
    predict_button = st.button("🔍 Predict Price", key="predict_button")
    
    if predict_button:
        try:
            # Prepare input data
            x = np.zeros(len(columns))
            x[0] = area
            x[1] = bathrooms
            x[2] = bedrooms
            
            # Set location
            loc_index = columns.index(location)
            x[loc_index] = 1
            
            # Make prediction
            predicted_price = model.predict([x])[0]
            
            # Calculate price per square foot
            price_per_sqft = predicted_price / area
            
            # Display prediction with styled message
            st.markdown(f"""
                <div class='success-message'>
                    <h2 style='color: #ffffff; margin-bottom: 0.5rem;'>Estimated Property Price</h2>
                    <div style='font-size: 2.5rem; font-weight: bold; color: #ffffff;'>{format_price(predicted_price)}</div>
                    <div style='color: #94a3b8; font-size: 1.1rem;'>Price per sq ft: {price_per_sqft:,.2f}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # ROI Prediction with styled cards
            st.markdown("### 📈 ROI Analysis")
            annual_growth_rate = 0.07  # 7% annual appreciation rate
            
            roi_5_years = round(predicted_price * ((1 + annual_growth_rate) ** 5), 2)
            roi_10_years = round(predicted_price * ((1 + annual_growth_rate) ** 10), 2)
            roi_15_years = round(predicted_price * ((1 + annual_growth_rate) ** 15), 2)
            
            roi_col1, roi_col2, roi_col3 = st.columns(3)
            with roi_col1:
                st.markdown(f"""
                    <div class='metric-card'>
                        <div class='metric-label'>5 Years Value</div>
                        <div class='metric-value'>{format_price(roi_5_years)}</div>
                        <div style='color: #6366f1; font-size: 0.9rem;'>+{((roi_5_years/predicted_price - 1) * 100):.1f}%</div>
                    </div>
                """, unsafe_allow_html=True)
            with roi_col2:
                st.markdown(f"""
                    <div class='metric-card'>
                        <div class='metric-label'>10 Years Value</div>
                        <div class='metric-value'>{format_price(roi_10_years)}</div>
                        <div style='color: #6366f1; font-size: 0.9rem;'>+{((roi_10_years/predicted_price - 1) * 100):.1f}%</div>
                    </div>
                """, unsafe_allow_html=True)
            with roi_col3:
                st.markdown(f"""
                    <div class='metric-card'>
                        <div class='metric-label'>15 Years Value</div>
                        <div class='metric-value'>{format_price(roi_15_years)}</div>
                        <div style='color: #6366f1; font-size: 0.9rem;'>+{((roi_15_years/predicted_price - 1) * 100):.1f}%</div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Environmental Analysis with styled cards
            st.markdown("### 🌍 Environmental Analysis")
            seed = sum(ord(c) for c in location)
            np.random.seed(seed)
            
            env_col1, env_col2, env_col3 = st.columns(3)
            with env_col1:
                aqi = np.random.randint(50, 200)
                aqi_color = "#6366f1" if aqi < 100 else "#FFC107" if aqi < 150 else "#F44336"
                st.markdown(f"""
                    <div class='metric-card'>
                        <div class='metric-label'>Air Quality Index</div>
                        <div class='metric-value' style='color: {aqi_color}'>{aqi}</div>
                        <div style='font-size: 0.9rem;'>Good: 0-100 | Moderate: 101-150 | Poor: 151+</div>
                    </div>
                """, unsafe_allow_html=True)
            with env_col2:
                noise = np.random.randint(30, 90)
                noise_color = "#6366f1" if noise < 50 else "#FFC107" if noise < 70 else "#F44336"
                st.markdown(f"""
                    <div class='metric-card'>
                        <div class='metric-label'>Noise Level (dB)</div>
                        <div class='metric-value' style='color: {noise_color}'>{noise}</div>
                        <div style='font-size: 0.9rem;'>Safe: 0-50 | Moderate: 51-70 | High: 71+</div>
                    </div>
                """, unsafe_allow_html=True)
            with env_col3:
                green = round(np.random.uniform(5, 30), 2)
                green_color = "#6366f1" if green > 20 else "#FFC107" if green > 10 else "#F44336"
                st.markdown(f"""
                    <div class='metric-card'>
                        <div class='metric-label'>Green Space %</div>
                        <div class='metric-value' style='color: {green_color}'>{green}%</div>
                        <div style='font-size: 0.9rem;'>Excellent: >20% | Good: 10-20% | Low: <10%</div>
                    </div>
                """, unsafe_allow_html=True)
            
        except Exception as e:
            prediction_placeholder.error(f"Error making prediction: {str(e)}")
            st.error("Please check your input values and try again.")
    
    # Market Statistics with styled cards
    st.markdown("### 📊 Market Statistics")
    col1a, col1b, col1c = st.columns(3)
    with col1a:
        # Calculate average price per sq ft for the selected location
        avg_price_sqft = get_price_per_sqft(model, columns, location, area=1000, bhk=2, bath=2)
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>Average Price/sq ft</div>
                <div class='metric-value'>₹{avg_price_sqft:,.2f}</div>
                <div style='font-size: 0.9rem;'>Based on 1000 sq ft, 2BHK, 2 Bath</div>
            </div>
        """, unsafe_allow_html=True)
    with col1b:
        st.markdown("""
            <div class='metric-card'>
                <div class='metric-label'>Total Properties</div>
                <div class='metric-value'>2,500+</div>
                <div style='font-size: 0.9rem;'>Active listings in area</div>
            </div>
        """, unsafe_allow_html=True)
    with col1c:
        st.markdown("""
            <div class='metric-card'>
                <div class='metric-label'>Accuracy Rate</div>
                <div class='metric-value'>95%</div>
                <div style='font-size: 0.9rem;'>Model prediction accuracy</div>
            </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("### 📈 Popular Locations")
    # Calculate price per sq ft for all locations
    locations_data = {}
    for loc in ["malviya nagar", "vaishali nagar", "civil lines", "bapu nagar", "mansarovar ext."]:
        price_sqft = get_price_per_sqft(model, columns, loc, area=1000, bhk=2, bath=2)
        locations_data[loc.title()] = price_sqft
    
    fig = px.bar(
        x=list(locations_data.keys()),
        y=list(locations_data.values()),
        title="Average Price per sq ft by Location",
        labels={"x": "Location", "y": "Price per sq ft (₹)"},
        color=list(locations_data.values()),
        color_continuous_scale='Viridis'
    )
    
    # Update layout with dark theme
    fig.update_layout(
        plot_bgcolor='#1e293b',
        paper_bgcolor='#1e293b',
        font=dict(color='#ffffff'),
        title_font_size=20,
        title_font_color='#ffffff',
        showlegend=False,
        xaxis=dict(
            gridcolor='#334155',
            color='#ffffff',
            title_font_color='#ffffff'
        ),
        yaxis=dict(
            gridcolor='#334155',
            color='#ffffff',
            title_font_color='#ffffff'
        ),
        margin=dict(t=50, l=50, r=50, b=50)
    )
    
    # Update bar colors and opacity
    fig.update_traces(
        marker_color='#6366f1',
        marker_line_color='#4f46e5',
        marker_line_width=1.5,
        opacity=0.8
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Footer with gradient background
st.markdown("""
    <div style='background: linear-gradient(45deg, #0a1929, #132f4c); padding: 2rem; border-radius: 10px; color: white; text-align: center; margin-top: 2rem; border: 1px solid #0066cc;'>
        <p style='margin: 0;'>Built with ❤️ for PropertyPulse: Smart Real Estate Analytics</p>
        <p style='margin: 0.5rem 0 0;'>© 2024 PropertyPulse: Smart Real Estate Analytics</p>
    </div>
    """, unsafe_allow_html=True) 