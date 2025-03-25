# scripts/upload_models.py

import os
import pickle
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import insert
from utils.db_utils import create_tables  # Đảm bảo bảng models đã tồn tại

# 🔗 Kết nối đến Neon DB
DATABASE_URL = 'postgresql://tokenomics_db_owner:npg_pxdgnu20lCzf@ep-raspy-pine-a8r3jbtu-pooler.eastus2.azure.neon.tech/tokenomics_db?sslmode=require'
engine = create_engine(DATABASE_URL)

# ✅ Đảm bảo bảng models tồn tại trước khi thao tác
create_tables()

# ✅ Reflect metadata sau khi bảng đã được tạo
metadata = MetaData()
metadata.reflect(bind=engine)
models_table = metadata.tables['models']

# Hàm upload model dạng JSON
def upload_json_model(file_path, model_name, model_type):
    with open(file_path, 'r') as f:
        json_data = f.read()

    with engine.begin() as conn:  # 🔐 Transaction tự commit
        conn.execute(insert(models_table), {
            "model_name": model_name,
            "model_type": model_type,
            "model_json": json_data,
            "model_binary": None
        })
    print(f"✅ Uploaded JSON model: {model_name}")

# 🔧 Hàm upload model dạng pickle
def upload_pickle_model(file_path, model_name, model_type):
    with open(file_path, 'rb') as f:
        binary_data = f.read()

    with engine.begin() as conn:  # 🔐 Transaction tự commit
        conn.execute(insert(models_table), {
            "model_name": model_name,
            "model_type": model_type,
            "model_json": None,
            "model_binary": binary_data
        })
    print(f"✅ Uploaded Pickle model: {model_name}")

# 📂 Xác định đường dẫn thư mục chứa model
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# ✅ Upload từng model
upload_json_model(os.path.join(MODEL_DIR, "xgb_tsi_model.json"), "xgb_tsi", "xgboost")
upload_pickle_model(os.path.join(MODEL_DIR, "kmeans_model.pkl"), "kmeans_cluster", "kmeans")
upload_pickle_model(os.path.join(MODEL_DIR, "scaler_kmeans.pkl"), "kmeans_scaler", "scaler")
