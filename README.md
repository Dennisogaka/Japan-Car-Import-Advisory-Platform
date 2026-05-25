# Vehicle Price Prediction and Comparison Pipeline

This is a Machine Learning pipeline that scrapes vehicle listings, cleans the data, and trains a scikit-learn model to predict values, integrating KRA tax schedules and port fees to calculate total landed import costs and compare them directly against local market prices.

---

## Project Lifecycle Workflow

1. **Data Scraping**: Extracting raw vehicle listings and specifications.
2. **Data Cleaning**: Handling missing values, removing duplicates, and fixing data types.
3. **Model Training**: Engineering features and training a machine learning pipeline (`ColumnTransformer` + Regression).
4. **Deployment**: Serving the model locally via Flask API endpoint.

---

## Project Structure
```text
├── notebook/
│   ├── 1_japan_car.ipynb         
├── car_import_advisory_api.py                  
├── car_price_prediction.py                
├── car_pricing_model_V1.pkl                            
└── README.md                      
