# 🏠 PropertyPulse – Smart Real Estate Analytics

**PropertyPulse** is a data-driven web application built using **Streamlit** that helps users **predict property prices**, assess **ROI potential**, and evaluate **environmental metrics** in various locations across **Jaipur, India**.

> 🚀 Empowering smarter real estate decisions with predictive analytics.

---

## 🔍 Features

### 🎯 Price Prediction
- Predict property prices based on:
  - Location (20+ areas in Jaipur)
  - Area (in square feet)
  - Number of bedrooms and bathrooms
- Shows estimated price and price per square foot

### 📈 ROI Analysis
- Forecast property value appreciation over:
  - 5 Years
  - 10 Years
  - 15 Years
- Based on an annual growth rate of 7%
- Displays % increase over current price

### 🌍 Environmental Analysis
- Simulated metrics for livability insights:
  - **Air Quality Index (AQI)**
  - **Noise Level (dB)**
  - **Green Space Percentage**
- Uses color-coded indicators (Good, Moderate, Poor)

### 📊 Market Insights
- Displays:
  - Average price/sq ft (based on selected area)
  - Total active listings
  - Model accuracy (~95%)
- Interactive bar graph of top localities

### 📍 Popular Locations
- Visual comparison of average price/sq ft in:
  - Malviya Nagar
  - Vaishali Nagar
  - Civil Lines
  - Bapu Nagar
  - Mansarovar Ext.

---

## 🖥️ Tech Stack

| Tool/Library     | Purpose                             |
|------------------|--------------------------------------|
| `Streamlit`      | Frontend Web Application             |
| `Scikit-learn`   | ML model for price prediction        |
| `Pickle`         | Model serialization                  |
| `Plotly`         | Interactive visualizations           |
| `NumPy`, `Pandas`| Data manipulation                    |
| `JSON`           | Location feature encoding            |
| `PIL`            | Logo display                         |
| `Custom CSS`     | Styled dark-themed UI                |

---

## 🧪 Sample Input & Output

### 🔹 Input

| Feature     | Value         |
|-------------|---------------|
| Area        | 1200 sq ft    |
| Bedrooms    | 3 BHK         |
| Bathrooms   | 2             |
| Location    | Malviya Nagar |

### 🔸 Output

- 💰 **Predicted Price:** ₹94.5 Lakhs  
- 📐 **Price per sq ft:** ₹7,875  
- 📈 **5-Year ROI:** ₹132.8 Lakhs  
- 🌿 **Environment:** AQI: 89 | Noise: 45 dB | Green Cover: 23%


## 🙌 Acknowledgements

- Built with using **Python** and **Streamlit**
- Inspired by real estate data apps and housing market trends
- Dataset sourced and cleaned from **Jaipur housing listings**

