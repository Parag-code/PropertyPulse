from flask import Flask, request, jsonify
from Server import util

app = Flask(__name__)



@app.route("/home", methods=["GET"])
def health():
    return "OK", 200


# Step 1: Fetching Locations
@app.route('/get_locations_names', methods=['GET'])
def get_location_names():
    try:
        locations = util.get_location_names()
        response = jsonify({"locations": locations})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Step 2: Estimating Home Price
@app.route('/get_estimated_price', methods=['POST'])
def get_home_price():
    try:
        # Input Validation
        total_sqft = float(request.form.get('sqft', 0))
        location = request.form.get('location', '')
        BHK = int(request.form.get('BHK', 0))
        bath = int(request.form.get('bath', 0))

        # Check for invalid inputs
        if not location or total_sqft <= 0 or BHK <= 0 or bath <= 0:
            return jsonify({'error': 'Invalid input values'}), 400

        # Get Estimated Price
        estimated_price = util.get_estimated_price(location, total_sqft, BHK, bath)
        response = jsonify({'estimated_price': float(estimated_price)})
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response
    except ValueError:
        return jsonify({'error': 'Invalid input type'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ✅ Route 3: ROI Prediction
@app.route('/get_roi_prediction', methods=['POST'])
def get_roi():
    """Returns the ROI prediction for 5, 10, and 15 years."""
    try:
        location = request.form.get('location', '')
        sqft = float(request.form.get('sqft', 0))
        price = float(request.form.get('price', 0))

        if not location or sqft <= 0 or price <= 0:
            return jsonify({'error': 'Invalid input values'}), 400

        roi = util.get_roi_prediction(location, sqft, price)

        response = jsonify({
            "current_price": roi["current_price"],
            "ROI_5_years": roi["ROI_5_years"],
            "ROI_10_years": roi["ROI_10_years"],
            "ROI_15_years": roi["ROI_15_years"]
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ Route 4: Environmental Analysis
@app.route('/get_environmental_analysis', methods=['POST'])
def get_environmental_analysis():
    """Returns simulated environmental analysis data."""
    try:
        location = request.form.get('location', '')

        if not location:
            return jsonify({'error': 'Invalid location'}), 400

        env_data = util.get_environmental_analysis(location)

        response = jsonify({
            "Air_Quality_Index": env_data["Air_Quality_Index"],
            "Noise_Pollution_Level": env_data["Noise_Pollution_Level"],
            "Green_Space_Percentage": env_data["Green_Space_Percentage"]
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500




# Step 3: Running the Flask Server
if __name__ == "__main__":
    print("Starting Python Flask server for home price prediction...")
    try:
        util.load_saved_artifacts()
        app.run()
    except Exception as e:
        print(f"Error starting server: {e}")


