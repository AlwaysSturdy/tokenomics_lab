def calculate_tokenomics_features(schedule_df, allocation_df):
    features = {}
    total = allocation_df["percentage"].sum() / 100  # sẽ nhân với total_supply sau nếu cần

    # SPI: unlocked trong 12 tháng đầu
    features["SPI"] = round(schedule_df[schedule_df["month_number"] < 12]["unlocked_tokens"].sum() / schedule_df["unlocked_tokens"].sum(), 3)

    # ACI: Sum(%)^2 của các allocation
    features["ACI"] = round(((allocation_df["percentage"] / 100) ** 2).sum(), 3)


    # VLS: Trung bình số tháng vesting / 36
    features["VLS"] = round(allocation_df["vesting_months"].mean() / 36, 3)

    # CSP_TGE: unlock tại TGE
    features["CSP_TGE"] = round(schedule_df[schedule_df["month_number"] == 0]["unlocked_tokens"].sum() / schedule_df["unlocked_tokens"].sum(), 3)

    # UVS: Std.dev của unlock theo tháng
    features["UVS"] = round(schedule_df.groupby("month_number")["unlocked_tokens"].std().mean(), 3)

    # LUE: số tháng có unlock > 10% tổng unlock
    monthly_total = schedule_df.groupby("month_number")["unlocked_tokens"].sum()
    threshold = 0.10 * schedule_df["unlocked_tokens"].sum()
    features["LUE"] = int((monthly_total > threshold).sum())

    # VCI: std / mean giữa các tháng
    month_std = monthly_total.std()
    month_mean = monthly_total.mean()
    features["VCI"] = round(month_std / month_mean if month_mean > 0 else 0, 3)

    # % Team & Investor
    team_inv_pct = allocation_df[
        allocation_df["category"].str.lower().str.contains("team|investor")
    ]["percentage"].sum()
    features["Team_Investor_Percentage"] = round(team_inv_pct, 2)

    return features
