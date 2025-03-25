from datetime import datetime

import pandas as pd
import plotly.graph_objects as go

def plot_allocation_pie(allocation_df):
    labels = allocation_df["category"]
    values = allocation_df["percentage"]

    total = values.sum()
    gap = 100 - total

    if gap > 0:
        labels = labels.tolist() + ["Unallocated"]
        values = values.tolist() + [gap]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
    fig.update_layout(title_text="📊 Token Allocation Pie Chart")
    return fig


def plot_tokenomics_radar(features: dict):
    categories = list(features.keys())
    values = list(features.values())

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Tokenomics Features'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])
        ),
        showlegend=False,
        title_text="📈 Tokenomics Feature Radar"
    )

    return fig

import streamlit as st

def display_unlock_progress(vesting_df):
    today = datetime.today()

    # ✅ Parse unlock_date về datetime
    vesting_df["unlock_date"] = pd.to_datetime(vesting_df["unlock_date"], format="%d/%m/%Y")

    unlocked_df = vesting_df[vesting_df["unlock_date"] <= today]
    unlocked = unlocked_df["unlocked_tokens"].sum()

    total = vesting_df["unlocked_tokens"].sum()
    remaining = total - unlocked
    pct_unlocked = round(unlocked / total * 100, 2) if total > 0 else 0
    pct_remaining = 100 - pct_unlocked

    # Ước lượng số ngày còn lại đến khi vesting kết thúc
    last_date = vesting_df["unlock_date"].max()
    days_left = (last_date - today).days if last_date > today else 0

    # Hiển thị
    st.markdown("### 🔓 Tiến trình Unlock Token (tính đến hôm nay)")
    st.progress(pct_unlocked / 100 if pct_unlocked <= 100 else 1.0)

    st.write(f"✅ **Đã unlock**: {pct_unlocked:.2f}% ({unlocked:,.0f} tokens)")
    st.write(f"🔒 **Đang bị khóa**: {pct_remaining:.2f}% ({remaining:,.0f} tokens)")
    st.write(f"🕒 **Số ngày còn lại (ước lượng)**: {days_left} ngày")
