from sqlalchemy import create_engine, Table, Column, Integer, String, Date, Float, MetaData
import pandas as pd
from sqlalchemy.dialects.postgresql import BYTEA

DATABASE_URL = 'postgresql://tokenomics_db_owner:npg_pxdgnu20lCzf@ep-raspy-pine-a8r3jbtu-pooler.eastus2.azure.neon.tech/tokenomics_db?sslmode=require'

engine = create_engine(DATABASE_URL)
metadata = MetaData()

def create_tables():
    project_info = Table('project_info', metadata,
        Column('project_id', String, primary_key=True),
        Column('project_name', String),
        Column('symbol', String),
        Column('category', String),
        Column('fdv', Float),
        Column('total_supply', Float),
        Column('launch_date', Date)
    )

    token_allocation = Table('token_allocation', metadata,
        Column('project_id', String),
        Column('category', String),
        Column('percentage', Float),
        Column('cliff_months', Integer),
        Column('vesting_months', Integer),
        Column('initial_unlock', Float)
    )

    if 'models' not in metadata.tables:
        Table('models', metadata,
              Column('model_name', String, primary_key=True),
              Column('model_type', String),  # "xgboost", "kmeans", "scaler", ...
              Column('model_json', String),  # NULL nếu dùng model_binary
              Column('model_binary', BYTEA)  # NULL nếu dùng JSON
              )

    metadata.create_all(engine)
    print("✅ Tables created successfully.")

def upload_csv_to_table(csv_path, table_name, transform_func=None):
    try:
        df = pd.read_csv(csv_path)

        # Nếu có hàm xử lý dữ liệu, áp dụng trước khi upload
        if transform_func:
            df = transform_func(df)

        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"✅ Uploaded {csv_path} to '{table_name}' table.")
    except Exception as e:
        print(f"❌ Error uploading {csv_path} to {table_name}: {e}")

