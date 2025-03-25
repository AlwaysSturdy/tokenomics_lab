import streamlit as st


def render_tab0():
    st.title("📖 README - Hướng dẫn sử dụng hệ thống Tokenomics Analysis")

    # Giới thiệu hệ thống
    with st.expander("📌 Giới thiệu hệ thống"):
        st.markdown(
            """
            Đây là một nền tảng **phân tích Tokenomics và đánh giá hiệu quả kinh tế của các dự án Crypto**.

            Hệ thống cung cấp:
            - 📊 **Phân tích vesting schedule và token allocation**.
            - 🛠️ **Nhập thông tin Tokenomics tùy chỉnh**.
            - 🔍 **Dự đoán Tokenomic Stability Index (TSI)**.
            - 🎯 **Xếp loại dự án thành 4 nhóm**.
            - 🔄 **Đề xuất cách cải thiện Tokenomics**.
            """
        )

    # Tiêu chí đánh giá Tokenomics
    with st.expander("📊 Tiêu chí đánh giá Tokenomics"):
        st.markdown(
            """
            Hệ thống đánh giá dựa trên 3 chỉ số chính:
            - 🏦 **Sell Pressure Index (SPI)** – đo áp lực bán từ vesting.
            - 🏗️ **Allocation Concentration Index (ACI)** – mức độ tập trung phân bổ token.
            - 💧 **Vesting Liquidity Score (VLS)** – mức độ thanh khoản của tokenomics.

            🚀 **Tokenomic Stability Index (TSI)** là tổng hợp của 3 chỉ số trên.

            Hệ thống phân loại dự án thành 4 nhóm:
            - ✅ **Rất tốt**: TSI > 900
            - ✅ **Tốt**: TSI ~ 870-900
            - ⚠️ **Trung bình**: TSI ~ 800-870
            - ❌ **Rất xấu**: TSI < 750 (cần điều chỉnh tokenomics)
            """
        )

    # Hướng dẫn sử dụng
    with st.expander("🛠️ Hướng dẫn sử dụng giao diện"):
        st.markdown(
            """
            🔷 **Tab 1 – Token Allocation & Vesting Overview**
            - **Chọn dự án có sẵn** từ danh sách.
            - **Xem phân bổ token, lịch vesting và chỉ số tokenomics**.
            - **Nhận đánh giá TSI và xếp loại dự án**.

            🔷 **Tab 2 – Custom Tokenomics Input & Evaluation**
            - **Nhập thông tin token allocation**.
            - **Tạo lịch vesting và tính toán chỉ số tokenomics**.
            - **Nhận dự đoán TSI và đề xuất cải thiện nếu cần**.
            """
        )

    # Cơ chế đánh giá & cải thiện Tokenomics
    with st.expander("🔄 Cơ chế đánh giá & cải thiện Tokenomics"):
        st.markdown(
            """
            📌 Nếu dự án có TSI thấp (**"Trung bình" hoặc "Rất xấu"**), hệ thống sẽ:
            1. **Phân tích điểm yếu** trong tokenomics.
            2. **Đưa ra đề xuất cải thiện**, ví dụ:
               - 📉 Giảm áp lực bán bằng cách tăng cliff hoặc kéo dài vesting.
               - 🔄 Điều chỉnh phân bổ token để giảm tập trung quá mức.
               - 💰 Tối ưu hóa thanh khoản dựa trên mô hình vesting.

            📍 **Người dùng có thể thử nghiệm chỉnh sửa và đánh giá lại.**
            """
        )


if __name__ == "__main__":
    render_tab0()
