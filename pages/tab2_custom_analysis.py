import streamlit as st
import pandas as pd
import io
from datetime import datetime

from services.predictor import predict_tsi
from utils.vesting_utils import generate_vesting_schedule
from utils.feature_engineering import calculate_tokenomics_features
from utils.visualization import (
    plot_allocation_pie,
    plot_tokenomics_radar,
    display_unlock_progress,
)

def render_tab():
    st.markdown("## 🧪 Phân Tích Cấu Trúc Tokenomics Tùy Chỉnh")
    st.markdown("Tạo và thử nghiệm cấu trúc tokenomics của riêng bạn để đánh giá độ ổn định và TSI.")

    st.divider()
    st.markdown("### 1️⃣ Nhập thông tin cấu trúc Allocation")

    num_alloc = st.number_input("Số vòng allocation", min_value=1, max_value=20, value=2, step=1)

    default_df = pd.DataFrame({
        "category": ["" for _ in range(num_alloc)],
        "percentage": [0.0] * num_alloc,
        "initial_unlock": [0.0] * num_alloc,
        "cliff_months": [0] * num_alloc,
        "vesting_months": [0] * num_alloc
    })

    edited_df = st.data_editor(default_df, key="custom_alloc_editor", use_container_width=True)
    st.session_state["custom_allocation"] = edited_df

    st.markdown("### 2️⃣ Nhập tổng cung & ngày launch")

    col1, col2 = st.columns(2)
    with col1:
        total_supply = st.number_input("Tổng cung token", value=1_000_000_000, step=1_000_000, min_value=1)
    with col2:
        launch_date = st.date_input("Ngày ra mắt token", value=datetime(2024, 10, 1))
        launch_date_str = launch_date.strftime("%d/%m/%Y")

    st.divider()

    if st.button("🚀 Phân Tích Tokenomics"):
        edited_df = st.session_state.get("custom_allocation", default_df)

        if edited_df.empty or edited_df["category"].str.strip().eq("").all():
            st.warning("⚠️ Vui lòng nhập ít nhất một allocation hợp lệ.")
            return

        try:
            vesting_df = generate_vesting_schedule(
                edited_df,
                total_token_supply=total_supply,
                launch_date=launch_date_str
            )

            features = calculate_tokenomics_features(vesting_df, edited_df)
            tsi_score = predict_tsi(features)

            st.markdown("""
                <h4 style='color:#4CAF50'>🎯 Tokenomic Stability Index (TSI):
                <span style='font-size: 28px; color:#2196F3'>{:.2f}/100</span></h4>
            """.format(tsi_score), unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(plot_allocation_pie(edited_df), use_container_width=True)
            with col2:
                st.plotly_chart(plot_tokenomics_radar(features), use_container_width=True)

            display_unlock_progress(vesting_df)

            with st.expander("📊 Lịch vesting theo tháng"):
                vesting_summary = vesting_df.groupby(["month_number", "category"], as_index=False)["unlocked_tokens"].sum()
                vesting_summary = vesting_summary[vesting_summary["unlocked_tokens"] > 0]
                vesting_summary.columns = ["Tháng", "Vòng", "Số token unlock"]
                st.dataframe(
                    vesting_summary.style.format({"Số token unlock": lambda x: f"{x:,.0f}"}),
                    use_container_width=True
                )

                csv_vesting = io.StringIO()
                vesting_df.to_csv(csv_vesting, index=False)
                st.download_button(
                    label="📥 Tải lịch vesting (.csv)",
                    data=csv_vesting.getvalue(),
                    file_name="vesting_schedule.csv",
                    mime="text/csv"
                )

            with st.expander("📄 Allocation đã nhập"):
                st.dataframe(
                    edited_df.style.format({"percentage": "{:.2f}"}), use_container_width=True
                )
                csv_alloc = io.StringIO()
                edited_df.to_csv(csv_alloc, index=False)
                st.download_button(
                    label="📥 Tải bảng allocation (.csv)",
                    data=csv_alloc.getvalue(),
                    file_name="allocation_input.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.exception(e)
