from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

def generate_vesting_schedule(
    allocation_df,
    total_token_supply,
    project_id="custom_project",
    launch_date="01/10/2024"
):
    """
    Tạo lịch vesting chi tiết theo từng tháng, tuân thủ cấu trúc giống core_vesting_schedule.csv

    Parameters:
    - allocation_df: DataFrame gồm category, percentage, initial_unlock, cliff_months, vesting_months
    - total_token_supply: Tổng cung token
    - project_id: ID dự án (string hoặc số)
    - launch_date: ngày ra mắt (string, format dd/mm/yyyy)

    Returns:
    - vesting_schedule_df: DataFrame gồm các cột chuẩn hóa
    """

    schedule = []
    allocation_id = 1
    launch_dt = datetime.strptime(launch_date, "%d/%m/%Y")

    for _, row in allocation_df.iterrows():
        category = row["category"]
        pct = float(row["percentage"])
        initial = float(row["initial_unlock"])
        cliff = int(row["cliff_months"])
        vesting = int(row["vesting_months"])

        total_tokens = total_token_supply * pct / 100
        initial_tokens = total_tokens * initial / 100
        remaining_tokens = total_tokens - initial_tokens

        # Tổng số tháng (bao gồm tháng 0, cliff và vesting sau cliff)
        total_months = cliff + vesting + 1
        monthly_unlock = (remaining_tokens / vesting) if vesting > 0 else 0

        for m in range(total_months):
            if m == 0:
                unlocked = initial_tokens
            elif m > cliff and vesting > 0 and (m - cliff) <= vesting:
                unlocked = monthly_unlock
            else:
                unlocked = 0

            # Tính ngày unlock từ launch date + m tháng
            dt = launch_dt + relativedelta(months=+m)
            unlock_dt = f"{dt.day}/{dt.month}/{dt.year}"  # Tương thích Windows

            schedule.append({
                "project_id": project_id,
                "allocation_id": allocation_id,
                "category": category,
                "month_number": m,
                "unlock_date": unlock_dt,
                "unlocked_tokens": round(unlocked)
            })

        allocation_id += 1

    return pd.DataFrame(schedule)
