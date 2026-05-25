from flask import Flask, request, jsonify
import joblib 
import pandas as pd

app = Flask(__name__) 

# Load trained pricing model
loaded_model = joblib.load('car_pricing_model_V1.pkl') 

# Importing cost calculation
def calculate_import_cost(predicted_fob_usd, factors):
    usd_to_kes = factors["exchange_rate_kes_per_usd"]
    
    # Convert predicted FOB price from USD to KES
    purchase_price_kes = predicted_fob_usd * usd_to_kes
    
    # Extract operational factors
    shipping_cost_kes = factors["shipping_cost_kes"]
    kra_taxes_kes = factors["kra_taxes_kes"]
    port_charges_kes = factors["port_charges_kes"]                                      
    clearing_fees_kes = factors["clearing_fees_kes"]
    registration_costs_kes = factors["registration_costs_kes"]                                      
    other_charges_kes = factors["other_charges_kes"]                                    
    
    # Sum total landing cost
    total_import_cost_kes = (purchase_price_kes + shipping_cost_kes + kra_taxes_kes + 
                             port_charges_kes + clearing_fees_kes + registration_costs_kes + other_charges_kes)      
    
    return total_import_cost_kes, purchase_price_kes

@app.route('/')
def home():
    return '''
    <h1>Japan Car Import Advisory Platform</h1>
    <form action="/predict" method="post">
        <h3>Vehicle Specifications:</h3>
        <p>Mileage(KM): <input type="number" name="mileage" required></p>
        <p>Engine(CC): <input type="number" name="engine" required></p>
        <p>Vehicle Age: <input type="number" name="vehicle_age" required></p>
        <p>Transmission: <input type="text" name="transmission" placeholder="e.g., Automatic" required></p>
        <p>Model Code: <input type="text" name="model_code" placeholder="e.g., DBA-NSP130" required></p>
        
        <h3>Local Market Baseline (For Savings Comparison):</h3>
        <p>Local Yard Price in Kenya (KES): <input type="number" name="local_price_kes" placeholder="e.g., 1800000" required></p>
        
        <button type="submit">Analyze Import Costs & Savings</button>
    </form>
    '''

@app.route('/predict', methods=['POST']) 
def predict():
    # Client data from the form
    mileage = float(request.form['mileage'])
    engine = float(request.form['engine'])
    vehicle_age = float(request.form['vehicle_age'])
    transmission = request.form['transmission']
    model_code = request.form['model_code']
    local_price_kes = float(request.form['local_price_kes'])

    # Structure data for the ML Model
    input_df = pd.DataFrame([{
        'Mileage (KM)': mileage,
        'Engine (CC)': engine,
        'Vehicle Age': vehicle_age,
        'Transmission': transmission,
        'Model Code': model_code,
    }])

    # Japan FOB price prediction (model outputs USD)
    predicted_fob_usd = float(loaded_model.predict(input_df)[0])

    # Dynamic logistics factors
    factors = {
        "exchange_rate_kes_per_usd": 130.0,  # Baseline market rate
        "shipping_cost_kes": 200000,         # Average RORO shipping to Mombasa
        "kra_taxes_kes": 550000,             # Placeholder (Connect your complex KRA script logic here!)
        "port_charges_kes": 120000,          # Mombasa port handling & SGR
        "clearing_fees_kes": 40000,          # Clearing Agent fee
        "registration_costs_kes": 25000,     # NTSA registration & plates
        "other_charges_kes": 15000            # Marine insurance / miscellaneous
    }

    # Calculation engine
    total_landed_cost, purchase_price_kes = calculate_import_cost(predicted_fob_usd, factors)
    
    # Calculate the advisory "Savings" metric
    net_savings = local_price_kes - total_landed_cost
    if net_savings > 0:
        advice_color = "green"
        advice_text = f"✔ Clear to Import! You save approximately KES {net_savings:,.2f} compared to buying locally."
    else:
        advice_color = "red"
        advice_text = f"✘ Buy Locally! Importing costs KES {abs(net_savings):,.2f} more than local market alternatives."

    # Advisory layout
    return f'''
        <h1>Japan Car Import Advisory Assessment</h1>
        <hr>
        <h3>1. Cost Breakdown</h3>
        <ul>
            <li><strong>Predicted Japan Purchase Price (FOB):</strong> ${predicted_fob_usd:,.2f} (~KES {purchase_price_kes:,.2f})</li>
            <li><strong>Freight & Shipping (Mombasa):</strong> KES {factors['shipping_cost_kes']:,.2f}</li>
            <li><strong>Estimated KRA Taxes:</strong> KES {factors['kra_taxes_kes']:,.2f}</li>
            <li><strong>Port, Clearing & Registration:</strong> KES {(factors['port_charges_kes'] + factors['clearing_fees_kes'] + factors['registration_costs_kes']):,.2f}</li>
        </ul>
        <h2 style="color: navy;">Total Estimated Landed Cost: KES {total_landed_cost:,.2f}</h2>
        
        <hr>
        <h3>2. Market Comparison</h3>
        <p>Local Kenyan Yard Price: KES {local_price_kes:,.2f}</p>
        <h2 style="color: {advice_color};">{advice_text}</h2>
        
        <br>
        <a href="/">← Run Another Search</a>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)