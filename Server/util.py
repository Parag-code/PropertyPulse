import json
import pickle
import numpy as np
import os

__locations=None
__data_columns=None
__model=None
annual_growth_rate = 0.07  # 7% annual appreciation rate

def get_estimated_price(location,sqft,BHK,bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = BHK
    if loc_index >= 0:
        x[loc_index] = 1
    return round(__model.predict([x])[0],2)

# ✅ Function to calculate future property price
def calculate_future_price(current_price, years, rate=annual_growth_rate):
    """Calculates the future property price using compound growth formula."""
    return round(current_price * ((1 + rate) ** years), 2)

# ✅ ROI Prediction Function
def get_roi_prediction(location, sqft, price):
    """Predicts ROI for 5, 10, and 15 years."""
    try:
        # Validate location
        if location.lower() not in [loc.lower() for loc in __locations]:
            raise ValueError(f"Invalid location: {location}")
            
        # Use the provided price instead of estimating
        roi_5_years = calculate_future_price(price, 5)
        roi_10_years = calculate_future_price(price, 10)
        roi_15_years = calculate_future_price(price, 15)

        return {
            "current_price": price,
            "ROI_5_years": roi_5_years,
            "ROI_10_years": roi_10_years,
            "ROI_15_years": roi_15_years
        }
    except Exception as e:
        raise Exception(f"Error in ROI prediction: {str(e)}")

# ✅ Function to simulate environmental data dynamically
def generate_environmental_data(location):
    """Generates simulated environmental data based on location."""
    # Use location as seed for consistent results
    seed = sum(ord(c) for c in location)
    np.random.seed(seed)

    env_data = {
        "Air_Quality_Index": np.random.randint(50, 200),           # AQI values
        "Noise_Pollution_Level": np.random.randint(30, 90),        # Noise pollution in dB
        "Green_Space_Percentage": round(np.random.uniform(5, 30), 2)  # Green cover %
    }

    return env_data

# ✅ Environmental Analysis Function
def get_environmental_analysis(location):
    """Returns simulated environmental data."""
    try:
        # Validate location
        if location.lower() not in [loc.lower() for loc in __locations]:
            raise ValueError(f"Invalid location: {location}")
            
        return generate_environmental_data(location)
    except Exception as e:
        raise Exception(f"Error in environmental analysis: {str(e)}")




def get_location_names():
    return __locations

def load_saved_artifacts():
    print("Loading Saved Artifacts...")
    global __data_columns
    global __locations

    # Use relative path
    artifacts_folder = os.path.join(os.path.dirname(__file__), "Server", "artifacts")

    with open(os.path.join(artifacts_folder, "columns.json"), 'r') as f:
        __data_columns = json.load(f)["data_columns"]
        __locations = __data_columns[3:]

    global __model
    with open(os.path.join(artifacts_folder, "Jaipur_real_estate_model.pickle"), "rb") as f:
        __model = pickle.load(f)

    print("Loading Saved Artifacts Done!")




if __name__ =='__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('Vaishali Nagar', 1000, 3, 3))
    print(get_estimated_price('Vaishali Nagar', 1000, 2, 2))
    print(get_estimated_price("Ajmer Road", 1000, 2, 2))  # other location
    print(get_estimated_price('Bapu Nagar', 1000, 2, 2))  # other location
    print(get_roi_prediction('Vaishali Nagar', 1000, 500000))

    print(get_environmental_analysis('Vaishali Nagar'))
