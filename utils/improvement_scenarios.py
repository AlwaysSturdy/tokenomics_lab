# utils/improvement_scenarios.py

# 📌 Mapping nhãn KMeans thành mô tả dễ hiểu
cluster_labels = {
    0: "✅ Rất tốt",
    1: "⚠️ Trung bình",
    2: "✅ Tốt",
    3: "❌ Rất xấu"
}

# 📌 Rule-based đề xuất cải thiện theo từng đặc trưng tokenomics
feature_improvement_rules = {
    "SPI": {
        "threshold": 0.3,
        "comparison": "<",
        "advice": "⚠️ SPI thấp → Dự án unlock quá ít trong 12 tháng đầu. Cân nhắc giảm Initial Unlock hoặc tăng số tháng Vesting để đảm bảo có đủ thanh khoản và chống xả giá bất ngờ."
    },
    "ACI": {
        "threshold": 0.7,
        "comparison": ">",
        "advice": "⚠️ ACI cao → Token bị phân bổ quá tập trung. Nên phân bổ đều hơn giữa các nhóm như Community, Ecosystem, Development để tăng sự minh bạch và công bằng."
    },
    "VLS": {
        "threshold": 0.3,
        "comparison": "<",
        "advice": "⚠️ VLS thấp → Vesting period quá ngắn so với chuẩn ngành. Cân nhắc kéo dài thời gian vesting (>= 36 tháng) để đảm bảo cam kết lâu dài."
    },
    "CSP_TGE": {
        "threshold": 0.2,
        "comparison": ">",
        "advice": "⚠️ CSP_TGE cao → Quá nhiều token được unlock tại TGE. Điều này có thể tạo áp lực bán ngay khi niêm yết. Nên giảm Initial Unlock cho các allocation lớn."
    },
    "UVS": {
        "threshold": 50,
        "comparison": ">",
        "advice": "⚠️ UVS cao → Biến động unlock hàng tháng quá lớn. Hãy cân bằng lại vesting giữa các tháng để tránh tạo ra các đợt xả đột ngột."
    },
    "LUE": {
        "threshold": 2,
        "comparison": ">",
        "advice": "⚠️ LUE cao → Có quá nhiều đợt unlock lớn. Cân nhắc chia nhỏ các đợt lớn thành các vesting nhỏ hơn, mượt hơn."
    },
    "VCI": {
        "threshold": 0.5,
        "comparison": ">",
        "advice": "⚠️ VCI cao → Độ ổn định trong vesting thấp. Tokenomics hiện tại bị lệch, cần điều phối lại để vesting đều hơn giữa các tháng."
    },
    "Team_Investor_Percentage": {
        "threshold": 40,
        "comparison": ">",
        "advice": "⚠️ Tỷ lệ phân bổ cho Team & Investors quá cao. Cân nhắc giảm % allocation cho nhóm này để tăng sự phân tán và tính công bằng."
    }
}

# 📌 Hàm tiện ích để đánh giá điều kiện

def check_feature_issue(feature_name, value):
    rule = feature_improvement_rules.get(feature_name)
    if not rule:
        return None

    if rule["comparison"] == "<" and value < rule["threshold"]:
        return rule["advice"]
    if rule["comparison"] == ">" and value > rule["threshold"]:
        return rule["advice"]

    return None
