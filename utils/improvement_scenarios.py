# utils/improvement_scenarios.py

# 📌 Mapping nhãn KMeans thành mô tả dễ hiểu
cluster_labels = {
    0: "✅ Rất tốt",
    1: "⚠️ Trung bình",
    2: "✅ Tốt",
    3: "❌ Rất xấu"
}

# 📌 Đánh giá xung đột giữa TSI và Cluster
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

# 📌 Rule-based đề xuất cải thiện theo từng đặc trưng tokenomics
feature_improvement_rules = {
    "SPI": {
        "threshold": 0.3,
        "comparison": "<",
        "advice": "⚠️ SPI thấp → Dự án unlock quá ít trong 12 tháng đầu. Cân nhắc giảm Initial Unlock hoặc tăng số tháng Vesting."
    },
    "ACI": {
        "threshold": 0.7,
        "comparison": ">",
        "advice": "⚠️ ACI cao → Token bị phân bổ quá tập trung. Nên phân bổ đều hơn giữa các nhóm."
    },
    "VLS": {
        "threshold": 0.3,
        "comparison": "<",
        "advice": "⚠️ VLS thấp → Vesting period quá ngắn. Kéo dài thời gian vesting để đảm bảo cam kết lâu dài."
    },
    "CSP_TGE": {
        "threshold": 0.2,
        "comparison": ">",
        "advice": "⚠️ CSP_TGE cao → Quá nhiều token unlock tại TGE. Giảm Initial Unlock để tránh áp lực bán."
    },
    "UVS": {
        "threshold": 50,
        "comparison": ">",
        "advice": "⚠️ UVS cao → Unlock hàng tháng biến động lớn. Điều chỉnh lại lịch unlock để đều hơn."
    },
    "LUE": {
        "threshold": 2,
        "comparison": ">",
        "advice": "⚠️ LUE cao → Quá nhiều đợt unlock lớn. Cân nhắc chia nhỏ các đợt lớn thành các vesting nhỏ hơn."
    },
    "VCI": {
        "threshold": 0.5,
        "comparison": ">",
        "advice": "⚠️ VCI cao → Độ ổn định thấp. Điều phối lại vesting để đều hơn giữa các tháng."
    },
    "Team_Investor_Percentage": {
        "threshold": 40,
        "comparison": ">",
        "advice": "⚠️ Phân bổ Team & Investors quá cao. Cân nhắc giảm % allocation để tăng tính công bằng."
    }
}

def check_feature_issue(feature_name, value):
    rule = feature_improvement_rules.get(feature_name)
    if not rule:
        return None
    if rule["comparison"] == "<" and value < rule["threshold"]:
        return rule["advice"]
    if rule["comparison"] == ">" and value > rule["threshold"]:
        return rule["advice"]
    return None
