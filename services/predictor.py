import pandas as pd
from xgboost import DMatrix
from utils.model_loader import load_model_from_neon

# Tải model
xgb_model = load_model_from_neon("xgb_tsi")

# Đặc trưng đúng
expected_features = [
    'SPI',
    'ACI',
    'VLS',
    'CSP_TGE',
    'UVS',
    'LUE',
    'VCI',
    'Team_Investor_Percentage'
]

def predict_tsi(features: dict) -> float:
    df = pd.DataFrame([features])
    df = df[expected_features]

    # ✅ Chuyển sang DMatrix trước khi predict
    dmatrix = DMatrix(df)
    prediction = xgb_model.predict(dmatrix)

    return round(float(prediction[0]), 2)
