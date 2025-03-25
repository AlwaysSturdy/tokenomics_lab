# test_predictor.py

from services.predictor import predict_tsi

# 🧪 Mẫu dữ liệu đầu vào (giá trị giả định – bạn có thể thay đổi)
sample_features = {
    "SPI": 0.42,                         # Sell Pressure Index
    "ACI": 0.31,                         # Allocation Concentration Index
    "VLS": 0.55,                         # Vesting Length Stability
    "CSP_TGE": 0.12,                     # Cumulative Sell Pressure at TGE
    "UVS": 5,                            # Unique Vesting Segments
    "LUE": 1,                            # Late Unlock Events
    "VCI": 0.6,                          # Vesting Continuity Index
    "Team_Investor_Percentage": 25.0     # % Token cho Team + Investor
}

# 🔮 Dự đoán
tsi_score = predict_tsi(sample_features)

# ✅ In kết quả
print("🔮 Tokenomics Stability Index (TSI):", tsi_score)
