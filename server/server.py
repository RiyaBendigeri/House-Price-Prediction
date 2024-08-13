from flask import Flask, request, jsonify
import util

app = Flask(__name__)

# Initialize the util module
util.load_saved()

@app.route('/')
def index():
    return "Welcome to the Home Price Prediction API!"

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Test successful'})

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    try:
        locations = util.get_location_names()
        if locations is None:
            raise ValueError("Location names could not be retrieved.")
        app.logger.debug(f'Fetched locations: {locations}')
        response = jsonify({'locations': locations})
    except Exception as e:
        response = jsonify({'error': str(e)})
        app.logger.error(f"Error fetching locations: {e}")
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])
        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        response = jsonify({'estimated_price': estimated_price})
    except Exception as e:
        response = jsonify({'error': str(e)})
        app.logger.error(f"Error predicting home price: {e}")
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(port=8080, debug=True)