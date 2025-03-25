import os
import pickle
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.sql import insert

DATABASE_URL = 'postgresql://tokenomics_db_owner:npg_pxdgnu20lCzf@ep-raspy-pine-a8r3jbtu-pooler.eastus2.azure.neon.tech/tokenomics_db?sslmode=require'
engine = create_engine(DATABASE_URL)

# Reflect bảng models
metadata = MetaData()
metadata.reflect(bind=engine)
models_table = metadata.tables["models"]

def upload_pickle_model(file_path, model_name, model_type):
    with open(file_path, "rb") as f:
        binary_data = f.read()

    with engine.begin() as conn:
        conn.execute(insert(models_table), {
            "model_name": model_name,
            "model_type": model_type,
            "model_json": None,
            "model_binary": binary_data
        })
    print(f"✅ Uploaded {model_name}")

# 📂 Xác định đường dẫn thư mục chứa model
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_DIR = os.path.join(BASE_DIR, "models")

upload_pickle_model(os.path.join(MODEL_DIR, "kmeans_model.pkl"), "kmeans_cluster", "kmeans")
upload_pickle_model(os.path.join(MODEL_DIR, "scaler_kmeans.pkl"), "kmeans_scaler", "scaler")
