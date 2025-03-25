import json
import pickle
import joblib
from sqlalchemy import create_engine, MetaData, Table, select
from xgboost import Booster
from io import BytesIO

# 🔗 Kết nối Neon
DATABASE_URL = 'postgresql://tokenomics_db_owner:npg_pxdgnu20lCzf@ep-raspy-pine-a8r3jbtu-pooler.eastus2.azure.neon.tech/tokenomics_db?sslmode=require'
engine = create_engine(DATABASE_URL)


def load_model_from_neon(model_name):
    """
    Load mô hình từ bảng 'models' trong Neon PostgreSQL
    - model_json → xử lý bằng XGBoost (nếu là xgboost) hoặc json.loads
    - model_binary → xử lý bằng pickle.load
    """
    metadata = MetaData()
    metadata.reflect(bind=engine)

    if "models" not in metadata.tables:
        raise ValueError("❌ Bảng 'models' chưa tồn tại trong database.")

    models_table = metadata.tables["models"]

    with engine.connect() as conn:
        stmt = select(models_table).where(models_table.c.model_name == model_name)
        result = conn.execute(stmt).mappings().fetchone()

        if result is None:
            raise ValueError(f"❌ Không tìm thấy model với tên '{model_name}'.")

        # 🎯 Nếu là JSON string
        if result["model_json"]:
            if result["model_type"] == "xgboost":
                booster = Booster()
                booster.load_model(bytearray(result["model_json"], "utf-8"))  # Đọc từ string
                return booster
            else:
                return json.loads(result["model_json"])

        # 🎯 Nếu là dữ liệu nhị phân pickle
        elif result["model_binary"]:
            return joblib.load(BytesIO(result["model_binary"]))

        else:
            raise ValueError(f"⚠️ Model '{model_name}' không chứa dữ liệu (json hoặc binary).")
