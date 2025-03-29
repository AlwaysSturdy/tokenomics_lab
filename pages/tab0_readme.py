import streamlit as st

def render_tab0():
    st.title("📖 README - Hướng dẫn sử dụng hệ thống Tokenomics Analysis")

    # Giới thiệu hệ thống
    with st.expander("📌 Giới thiệu hệ thống"):
        st.markdown("""
        Đây là nền tảng phân tích Tokenomics và đánh giá hiệu quả kinh tế của các dự án Crypto.
        Cung cấp:
        - 📊 Phân tích vesting schedule và token allocation.
        - 🛠️ Nhập thông tin Tokenomics tùy chỉnh.
        - 🔍 Dự đoán Tokenomic Stability Index (TSI).
        - 🎯 Xếp loại dự án thành 4 nhóm (Rất tốt, Tốt, Trung bình, Rất xấu).
        - 🔄 Đề xuất cách cải thiện Tokenomics.
        """)

    with st.expander("📊 Tiêu chí đánh giá Tokenomics"):
        st.markdown("""
        Các đặc trưng chính:
        - 🏦 SPI: Áp lực bán.
        - 🏗️ ACI: Mức độ tập trung phân bổ.
        - 💧 VLS: Độ dài vesting.
        - 💰 CSP_TGE: Tỷ lệ unlock tại TGE.
        - 🌊 UVS: Độ biến động unlock.
        - 🪙 LUE: Số lần unlock lớn.
        - 📅 VCI: Độ nhất quán vesting.
        - 🧑‍🤝‍🧑 Team & Investor Percentage: Tỷ lệ phân bổ cho team & investors.
        """)

    with st.expander("🛠️ Hướng dẫn sử dụng"):
        st.markdown("""
        - Tab 1: Chọn dự án từ cơ sở dữ liệu để phân tích.
        - Tab 2: Nhập thông tin tùy chỉnh để phân tích.
        - Nhận kết quả TSI và phân loại, cùng với đề xuất cải thiện.
        """)

if __name__ == "__main__":
    render_tab0()
