from flask import Flask, request, jsonify
import joblib 
import pandas as pd

app = Flask(__name__) 

loaded_model=joblib.load('car_pricing_model_V1.pkl') 


@app.route('/')
def home():
    return '''
    <h1>Japan Car Import Price Prediction</h1>

    <form action="/predict" method="post">
    <p>Mileage(KM): </p>
    <input type="number" name="mileage">

    <p>Engine(CC): </p>
    <input type="number" name="engine">

    <p>Vehicle Age: </p>
    <input type="number" name="vehicle_age">

    <p>Transmission: </p>
    <input type="text" name="transmission">

    <p>Model Code: </p>
    <input type="text" name="model_code">

    <button type="submit">
        predict
    </button>
    </form>
'''

@app.route('/predict', methods=['POST']) 
def predict():
    # receive data from the client
    mileage = float(request.form['mileage'])
    engine = float(request.form['engine'])
    vehicle_age = float(request.form['vehicle_age'])
    transmission = request.form['transmission']
    model_code = request.form['model_code']

    input_df = pd.DataFrame([{
        'Mileage (KM)': mileage,
        'Engine (CC)': engine,
        'Vehicle Age': vehicle_age,
        'Transmission': transmission,
        'Model Code': model_code,
    }])

    # make prediction
    prediction = loaded_model.predict(input_df)[0]

    return f'''
        <h1>prediction result</h1>
        <h2>{prediction}</h2
    '''

@app.route('/health')
def health():
    
    return jsonify({
        'status': 'ok',
        'loaded_model': 'car_pricing_model_v1.0.0'
    })
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)