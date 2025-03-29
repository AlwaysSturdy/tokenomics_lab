# 📊 Tokenomics Lab - Tokenomics Analysis and Economic Efficiency Evaluation

Welcome to **Tokenomics Lab**, a powerful and interactive platform for analyzing the tokenomics of DeFi projects. Our tool provides deep insights into the **Tokenomic Stability Index (TSI)**, offering project evaluation, risk assessment, and recommendations for improvement.

## 🌟 Features
- **Automated Vesting Schedule Calculation:** Generate detailed schedules based on token allocation data.
- **Tokenomics Analysis & Evaluation:** Predict TSI and assess project stability.
- **Improvement Suggestions:** Identify weaknesses and get recommendations for optimizing tokenomics.
- **Custom Tokenomics Input:** Test and evaluate your own token allocation scenarios.
- **Interactive Visualizations:** View pie charts, radar charts, and unlock progress bars for clear insights.

## 🛠️ Technologies Used
- **Python**: Core programming language.
- **Streamlit**: Frontend interactive UI.
- **XGBoost**: Predicting Tokenomic Stability Index (TSI).
- **KMeans Clustering**: Grouping projects based on stability metrics.
- **SQLAlchemy & Neon**: Database management.
- **Pandas & NumPy**: Data processing and analysis.
- **Matplotlib & Plotly**: Data visualization.

## 📂 Project Structure
```
tokenomics_lab/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Dependencies
├── models/                # XGBoost and KMeans models
├── assets/                # Data files (CSV)
├── scripts/               # Data upload scripts
├── utils/                 # Utility functions
│   ├── db_utils.py        # Database connection
│   ├── model_loader.py    # Load models from Neon
│   ├── feature_engineering.py # Tokenomics calculations
│   ├── visualization.py   # Charts and plots
│   └── improvement_scenarios.py # Improvement suggestions
└── pages/                 # Streamlit page organization
    ├── tab0_readme.py     # Introduction and guide
    ├── tab1_existing_project.py # Existing project analysis
    └── tab2_custom_input.py # Custom tokenomics input
```

## ⚙️ Getting Started
### Prerequisites
- Python 3.9+
- Neon database credentials
- Streamlit

### Installation
```bash
git clone https://github.com/AlwaysSturdy/tokenomics_lab.git
cd tokenomics_lab
pip install -r requirements.txt
```

### Running the App
```bash
streamlit run app.py
```

## 💻 Usage Guide
### Tab 0 - README
An interactive guide to the features and structure of the Tokenomics Lab.

### Tab 1 - Existing Project Analysis
- Select a project from the dropdown list.
- View token allocation, vesting schedule, and TSI analysis.
- Receive improvement suggestions based on TSI and clustering results.

### Tab 2 - Custom Tokenomics Input
- Manually input token allocation, vesting parameters, and supply.
- Generate custom vesting schedules and analyze stability.
- Compare results to optimize tokenomics.

## 🔍 Evaluation Criteria
- **TSI Score**: Represents overall tokenomic stability.
- **KMeans Clustering**: Groups projects into 4 categories: Very Good, Good, Average, and Very Bad.
- **Conflict Detection**: Identifies inconsistencies between TSI and clustering results.

## 🌱 Future Enhancements
- **Advanced Predictive Models:** Incorporate more metrics.
- **Dynamic Report Generation:** Export insights as PDF.
- **User Profile System:** Save and compare multiple scenarios.

## 💡 Contributions
Contributions are welcome! Please fork the repo and submit pull requests for new features or improvements.

## 📜 License
This project is licensed under the MIT License.

Happy analyzing! 🚀

