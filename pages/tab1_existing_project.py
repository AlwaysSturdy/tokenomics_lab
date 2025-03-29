import streamlit as st
import pandas as pd
import io
from datetime import datetime
from sqlalchemy import create_engine
from services.predictor import predict_tsi
from utils.feature_engineering import calculate_tokenomics_features
from utils.vesting_utils import generate_vesting_schedule
from utils.visualization import (
    plot_allocation_pie,
    plot_tokenomics_radar,
    display_unlock_progress,
)
from utils.model_loader import load_model_from_neon
from utils.improvement_scenarios import cluster_labels, check_feature_issue

def evaluate_tsi_vs_cluster(tsi, cluster_id):
    """
    Đánh giá mối quan hệ giữa TSI và phân cụm KMeans để phát hiện xung đột.
    """
    if cluster_id == 0 and tsi >= 900:
        return "✅ Rất tốt – Tokenomics ổn định và bền vững."
    elif cluster_id == 1 and tsi >= 850:
        return "⚠️ TSI cao nhưng phân cụm Trung bình – Có thể mất cân đối về phân bổ."
    elif cluster_id == 2 and tsi >= 800:
        return "✅ Tốt – Tokenomics hợp lý nhưng có thể tối ưu thêm."
    elif cluster_id == 3 and tsi >= 750:
        return "⚠️ TSI khá nhưng phân cụm xấu – Cần cải thiện phân bổ vesting."
    elif cluster_id == 3 and tsi < 750:
        return "❌ Rất rủi ro – Tokenomics mất cân bằng, cần cải thiện đáng kể."
    else:
        return "📌 Xem xét thêm để đưa ra kết luận chính xác."

def render_tab():
    st.markdown("## 📊 Phân Tích Tokenomics từ Dự Án Có Sẵn")
    st.markdown("Chọn một dự án từ cơ sở dữ liệu để phân tích cấu trúc tokenomics và đánh giá TSI.")

    # Kết nối CSDL Neon
    DATABASE_URL = "postgresql://tokenomics_db_owner:npg_pxdgnu20lCzf@ep-raspy-pine-a8r3jbtu-pooler.eastus2.azure.neon.tech/tokenomics_db?sslmode=require"
    engine = create_engine(DATABASE_URL)

    try:
        project_info = pd.read_sql("SELECT * FROM project_info", engine)
        token_allocation = pd.read_sql("SELECT * FROM token_allocation", engine)
        vesting_schedule_all = pd.read_sql("SELECT * FROM vesting_schedule", engine)
        vesting_schedule_all["unlock_date"] = pd.to_datetime(vesting_schedule_all["unlock_date"])
    except Exception as e:
        st.error("❌ Lỗi khi truy cập dữ liệu từ Neon DB.")
        st.exception(e)
        return

    # Chọn project_id
    st.markdown("### 🔍 Chọn dự án để phân tích")
    project_info["display_name"] = project_info["project_id"].astype(str) + " - " + project_info["project_name"]
    selected_display = st.selectbox("Project", project_info["display_name"])
    selected_project = selected_display.split(" - ")[0]
    if project_info["project_id"].dtype == 'int64':
        selected_project = int(selected_project)

    proj_df = project_info[project_info["project_id"] == selected_project]
    if proj_df.empty:
        st.warning(f"⚠️ Không tìm thấy project_id: {selected_project}")
        return
    proj = proj_df.iloc[0]

    alloc_df = token_allocation[token_allocation["project_id"] == selected_project]

    # Hiển thị thông tin cơ bản về dự án
    st.markdown("### 📘 Thông tin cơ bản của dự án")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Tên dự án:** {proj['project_name']}")
        st.markdown(f"**Symbol:** {proj['symbol']}")
    with col2:
        st.markdown(f"**FDV:** {proj['fdv']:,}")
        st.markdown(f"**Total Supply:** {proj['total_supply']:,}")
    with col3:
        st.markdown(f"**Category:** {proj['category']}")
        st.markdown(f"**Launch Date:** {proj['launch_date'].strftime('%d/%m/%Y')}")

    # Ưu tiên lấy vesting từ bảng đã tính
    if selected_project in vesting_schedule_all["project_id"].unique():
        vesting_df = vesting_schedule_all[vesting_schedule_all["project_id"] == selected_project]
    else:
        launch_date_str = proj["launch_date"].strftime("%d/%m/%Y")
        vesting_df = generate_vesting_schedule(
            alloc_df,
            total_token_supply=proj["total_supply"],
            project_id=selected_project,
            launch_date=launch_date_str
        )

    # Phân tích đặc trưng
    features = calculate_tokenomics_features(vesting_df, alloc_df)
    tsi_score = predict_tsi(features)

    # Load mô hình KMeans + Scaler
    kmeans_model = load_model_from_neon("kmeans_cluster")
    kmeans_scaler = load_model_from_neon("kmeans_scaler")

    # Dự đoán phân cụm
    X_cluster = pd.DataFrame([features])
    X_scaled = kmeans_scaler.transform(X_cluster)
    cluster_id = int(kmeans_model.predict(X_scaled)[0])
    cluster_label = cluster_labels.get(cluster_id, "Không xác định")

    # Đánh giá xung đột giữa TSI và Cluster
    tsi_vs_cluster_analysis = evaluate_tsi_vs_cluster(tsi_score, cluster_id)

    # Hiển thị kết quả
    st.markdown("""<h4 style='color:#4CAF50'>🎯 Tokenomic Stability Index (TSI): 
        <span style='font-size: 28px; color:#2196F3'>{:.2f}/1000</span></h4>
    """.format(tsi_score), unsafe_allow_html=True)

    st.markdown(f"📌 **Phân loại Tokenomics:** <span style='color:#f44336'>{cluster_label}</span>", unsafe_allow_html=True)
    st.markdown(f"🔎 **Phân tích TSI vs Cluster:** {tsi_vs_cluster_analysis}")

    # Hiển thị gợi ý cải thiện nếu cần
    st.markdown("### 💡 Gợi ý cải thiện")
    improvement_found = False
    for feat_name, feat_value in features.items():
        advice = check_feature_issue(feat_name, feat_value)
        if advice:
            improvement_found = True
            st.markdown(f"- {advice}")
    if not improvement_found:
        st.success("✅ Không có đặc trưng nào vượt ngưỡng – Tokenomics đã khá ổn!")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_allocation_pie(alloc_df), use_container_width=True)
    with col2:
        st.plotly_chart(plot_tokenomics_radar(features), use_container_width=True)

    display_unlock_progress(vesting_df)

    with st.expander("📆 Lịch vesting tổng hợp"):
        vesting_summary = vesting_df.groupby(["month_number", "category"], as_index=False)["unlocked_tokens"].sum()
        vesting_summary = vesting_summary[vesting_summary["unlocked_tokens"] > 0]
        vesting_summary.columns = ["Tháng", "Vòng", "Số token unlock"]
        st.dataframe(vesting_summary, use_container_width=True)

        csv_vesting = io.StringIO()
        vesting_df.to_csv(csv_vesting, index=False)
        st.download_button("📥 Tải lịch vesting (.csv)", csv_vesting.getvalue(), f"vesting_project_{selected_project}.csv")

    with st.expander("📄 Allocation"):
        st.dataframe(alloc_df, use_container_width=True)
        csv_alloc = io.StringIO()
        alloc_df.to_csv(csv_alloc, index=False)
        st.download_button("📥 Tải allocation (.csv)", csv_alloc.getvalue(), f"allocation_{selected_project}.csv")
