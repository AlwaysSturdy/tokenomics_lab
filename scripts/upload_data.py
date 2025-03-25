import os
from utils.db_utils import create_tables, upload_csv_to_table
import pandas as pd

# ✅ Xác định đường dẫn gốc dự án
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def transform_project_info(df):
    df["launch_date"] = pd.to_datetime(df["launch_date"], errors='coerce').dt.date
    return df

def transform_token_allocation(df):
    return df

# ✅ Dùng đường dẫn tuyệt đối đến file CSV
project_info_path = os.path.join(BASE_DIR, "assets", "superset_info.csv")
token_allocation_path = os.path.join(BASE_DIR, "assets", "core_token_allocation_v1.csv")

# 1. Tạo bảng trong Neon
create_tables()

# 2. Upload CSV với transform
upload_csv_to_table(project_info_path, "project_info", transform_project_info)
upload_csv_to_table(token_allocation_path, "token_allocation", transform_token_allocation)
