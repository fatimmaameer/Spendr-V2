import streamlit as st
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import base64
from datetime import datetime, timedelta
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(page_title="Spendr", page_icon="🪙", layout="centered")

# Function to set dark background using encoded local image
def set_bg_from_local(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()
    css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        color: #E0E0E0;
    }}
    h1, h2, h3, h4, h5, h6, label, p, span, div {{
        color: #E0E0E0 !important;
    }}
    .stButton>button {{
        background: linear-gradient(135deg, #00BFFF, #0066CC);
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }}
    .stTextInput>div>input, .stNumberInput>div>input, .stDateInput>div>input {{
        background-color: rgba(30, 144, 255, 0.2);
        color: #E0E0E0;
        font-weight: bold;
        border-radius: 8px;
        border: 1px solid #00BFFF;
    }}
    .stSelectbox>div>select {{
        background-color: rgba(30, 144, 255, 0.2);
        color: #E0E0E0;
        font-weight: bold;
        border-radius: 8px;
        border: 1px solid #00BFFF;
    }}
    .css-1aumxhk {{
        background-color: rgba(30, 144, 255, 0.2);
        border-radius: 10px;
        padding: 10px;
    }}
    /* Sidebar styling - Updated to golden gradient */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #D4AF37 0%, #996515 100%);
        color: white;
    }}
    .sidebar .sidebar-content {{
        color: white;
    }}
    /* Radio button styling for golden theme */
    div[role="radiogroup"] > label {{
        background-color: rgba(212, 175, 55, 0.2);
        border-radius: 8px;
        padding: 8px 12px;
        margin: 4px 0;
        transition: all 0.3s;
    }}
    div[role="radiogroup"] > label:hover {{
        background-color: rgba(212, 175, 55, 0.4);
    }}
    div[role="radiogroup"] > label[data-baseweb="radio"]:has(input:checked) {{
        background-color: rgba(153, 101, 21, 0.6);
        border-left: 4px solid #D4AF37;
        font-weight: bold;
    }}
    /* Metric styling for golden theme */
    [data-testid="stMetric"] {{
        background-color: rgba(153, 101, 21, 0.3);
        border-radius: 8px;
        padding: 10px;
        border-left: 3px solid #D4AF37;
    }}
    [data-testid="stMetricLabel"] {{
        color: #D4AF37 !important;
    }}
    [data-testid="stMetricValue"] {{
        color: white !important;
    }}
    /* Coin logo styling */
    .coin-logo {{
        filter: drop-shadow(0 0 5px rgba(212, 175, 55, 0.7));
        transition: transform 0.3s;
    }}
    .coin-logo:hover {{
        transform: rotate(15deg);
    }}
    /* Loading bar styling */
    .gold-loading-bar {{
        height: 8px;
        background: linear-gradient(90deg, #D4AF37, #F1C40F, #D4AF37);
        border-radius: 4px;
        width: 100%;
        margin: 20px 0;
        position: relative;
        overflow: hidden;
    }}
    .gold-loading-bar::after {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        animation: shimmer 5s infinite;
    }}
    @keyframes shimmer {{
        0% {{ transform: translateX(-100%); }}
        100% {{ transform: translateX(100%); }}
    }}
    /* Wider chart styling */
    .stPlotlyChart {{
        width: 100% !important;
    }}
    /* Delete button styling */
    .delete-button {{
        background: linear-gradient(135deg, #FF0000, #990000) !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        margin-top: 20px !important;
    }}
    /* About page styling */
    .about-card {{
        background: linear-gradient(135deg, rgba(30, 144, 255, 0.2), rgba(0, 102, 204, 0.2)) !important;
        border-radius: 15px !important;
        padding: 25px !important;
        margin-bottom: 20px !important;
        border-left: 5px solid #D4AF37 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    }}
    .about-header {{
        color: #D4AF37 !important;
        text-align: center !important;
        margin-bottom: 20px !important;
        font-size: 2.5rem !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3) !important;
    }}
    .about-subheader {{
        color: #00BFFF !important;
        border-bottom: 2px solid #D4AF37 !important;
        padding-bottom: 5px !important;
        margin-top: 20px !important;
    }}
    .skill-pill {{
        display: inline-block !important;
        background: rgba(212, 175, 55, 0.3) !important;
        color: #D4AF37 !important;
        padding: 5px 15px !important;
        border-radius: 20px !important;
        margin: 5px !important;
        font-weight: bold !important;
        border: 1px solid #D4AF37 !important;
    }}
    .social-icon {{
        font-size: 30px !important;
        margin: 10px !important;
        color: #00BFFF !important;
        transition: all 0.3s !important;
    }}
    .social-icon:hover {{
        color: #D4AF37 !important;
        transform: scale(1.2) !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Set background
set_bg_from_local("newbg.png")

# CSV file path
CSV_FILE = "expenses.csv"

# Initialize CSV if not exists
def init_csv():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
        df.to_csv(CSV_FILE, index=False)

# Load existing expenses - FIXED VERSION
def load_expenses():
    df = pd.read_csv(CSV_FILE)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date
    df = df.dropna(subset=['Date'])
    return df

# Save a new expense
def save_expense(date, category, amount, description):
    if amount <= 0:
        st.error("Amount must be greater than 0! Please enter a valid amount.")
        return False
    
    df = load_expenses()
    if isinstance(date, str):
        date = pd.to_datetime(date).date()
    elif hasattr(date, 'date'):
        date = date.date()
    
    new_data = pd.DataFrame([[date, category, amount, description]], 
                            columns=["Date", "Category", "Amount", "Description"])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    return True

# Edit an expense by index
def update_expense(index, date, category, amount, description):
    if amount <= 0:
        st.error("Amount must be greater than 0! Please enter a valid amount.")
        return False
    
    df = load_expenses()
    if 0 <= index < len(df):
        if isinstance(date, str):
            date = pd.to_datetime(date).date()
        elif hasattr(date, 'date'):
            date = date.date()
        df.loc[index] = [date, category, amount, description]
        df.to_csv(CSV_FILE, index=False)
        return True
    return False

# Delete all expenses
def delete_all_expenses():
    try:
        os.remove(CSV_FILE)
        init_csv()
        return True
    except:
        return False

# Loading Page
def loading_screen():
    st.markdown("""<h1 style='text-align:center; font-size: 72px;'></h1>""", unsafe_allow_html=True)

# Add Expense
def add_expense():
    st.subheader("➕ Add a New Expense")
    date = st.date_input("Date", datetime.now(), key="date_picker")
    category = st.selectbox("Category", ["Food", "Transport", "Stationery", "Internet", "Recreation", "Other"])
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    description = st.text_input("Description")
    if st.button("Add Expense", key="add_expense_button"):
        if save_expense(date, category, amount, description):
            st.success("Expense added successfully!")
            st.balloons()

# Create colorful Plotly pie chart
def create_pie_chart(data, title):
    colors = px.colors.qualitative.Vivid + px.colors.qualitative.Pastel
    fig = px.pie(data, values='Amount', names='Category', title=title, color_discrete_sequence=colors, hole=0.3)
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        marker=dict(line=dict(color='#000000', width=1)),
        textfont=dict(size=14, color='white'),
        pull=[0.05] * len(data)
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        title_font=dict(size=20, color='white', family="Arial Black"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
            font=dict(size=12)
        ),
        hoverlabel=dict(bgcolor="black", font_size=14, font_family="Arial")
    )
    return fig

# Table Styling
def gradient_style(df):
    styled_df = df.copy()
    if 'Date' in styled_df.columns:
        styled_df['Date'] = styled_df['Date'].astype(str)
    return (
        styled_df.style
        .format({"Amount": "{:,.2f}"})
        .background_gradient(cmap="Blues", subset=['Amount'])
        .set_properties(**{
            'color': 'white',
            'font-weight': 'bold',
            'background-color': '#111111',
            'border': '1px solid rgba(255, 255, 255, 0.2)',
            'text-align': 'left'
        })
        .set_table_styles([{
            'selector': 'th',
            'props': [
                ('background-color', '#0066CC'),
                ('color', 'white'),
                ('font-weight', 'bold'),
                ('border', '1px solid rgba(255, 255, 255, 0.2)'),
                ('text-align', 'left')
            ]
        }, {
            'selector': 'td',
            'props': [('padding', '8px 12px')]
        }])
        .highlight_max(subset=['Amount'], color='#0066CC', props='color: white; font-weight: bold;')
    )

# View Expenses
def view_expenses():
    st.subheader("📋 All Expenses")
    df = load_expenses()
    st.dataframe(gradient_style(df), use_container_width=True, height=400)

    if not df.empty:
        st.subheader("📊 Visual Analysis")

        # Overall Pie Chart
        st.markdown("### 🎯 Overall Expense Distribution")
        category_totals = df.groupby("Category")["Amount"].sum().reset_index()
        fig1 = create_pie_chart(category_totals, "Total Expenses by Category")
        st.plotly_chart(fig1, use_container_width=True)

        # Monthly Pie Charts
        st.markdown("### 📅 Monthly Expense Breakdown")
        df_monthly = df.copy()
        df_monthly['Month'] = pd.to_datetime(df_monthly['Date']).dt.to_period('M').astype(str)
        monthly_totals = df_monthly.groupby(['Month', 'Category'])['Amount'].sum().reset_index()
        months = df_monthly['Month'].unique()
        tabs = st.tabs([f"📌 {month}" for month in months])

        for tab, month in zip(tabs, months):
            with tab:
                month_data = monthly_totals[monthly_totals['Month'] == month]
                if not month_data.empty:
                    fig_month = create_pie_chart(month_data, f"Expenses for {month}")
                    st.plotly_chart(fig_month, use_container_width=True)
                else:
                    st.info(f"No expenses recorded for {month}")

        # Daily Trend
        st.markdown("### ⏳ Daily Expense Trend")
        daily_totals = df.groupby('Date')['Amount'].sum().reset_index()
        fig4 = px.line(daily_totals, x='Date', y='Amount', title="Daily Expense Trend", markers=True,
                       color_discrete_sequence=['#00BFFF'])
        fig4.update_traces(line_color='#B8860B', line_width=3,
                           marker=dict(size=8, color='#0066CC', line=dict(width=1, color='DarkSlateGrey')))
        fig4.update_layout(
            xaxis_title="Date",
            yaxis_title="Amount",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            title_font=dict(size=20, color='white', family="Arial Black"),
            hovermode="x unified",
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)', showline=True, linecolor='rgba(255,255,255,0.5)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)', showline=True, linecolor='rgba(255,255,255,0.5)')
        )
        st.plotly_chart(fig4, use_container_width=True)

        # Monthly Trend Graph (NEW) - Wider version
        st.markdown("### 📈 Monthly Expense Trends")
        df_monthly_line = df.copy()
        df_monthly_line['Month'] = pd.to_datetime(df_monthly_line['Date']).dt.to_period("M").astype(str)
        monthly_trends = df_monthly_line.groupby(['Month', 'Category'])['Amount'].sum().reset_index()
        fig5 = px.line(monthly_trends, x='Month', y='Amount', color='Category', markers=True,
                       title='Monthly Trends by Category',
                       color_discrete_sequence=px.colors.sequential.Plasma)
        fig5.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            title_font=dict(size=20, color='white'),
            width=1200
        )
        st.plotly_chart(fig5, use_container_width=True)

# Dashboard
def dashboard():
    # Display the image
    st.image("https://github.com/HarisFarooq23/FirstApp/blob/main/pic.png?raw=true", use_container_width=True)
    
    # Add beautiful golden loading bar
    st.markdown('<div class="gold-loading-bar"></div>', unsafe_allow_html=True)
    
    # Add two pie charts below the image
    df = load_expenses()
    if not df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Overall Pie Chart
            category_totals = df.groupby("Category")["Amount"].sum().reset_index()
            fig1 = create_pie_chart(category_totals, "Total Expenses by Category")
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Current Month Pie Chart
            current_month = datetime.now().strftime("%Y-%m")
            monthly_expenses = df[pd.to_datetime(df['Date']).dt.to_period('M').astype(str) == current_month]
            if not monthly_expenses.empty:
                month_totals = monthly_expenses.groupby("Category")["Amount"].sum().reset_index()
                fig2 = create_pie_chart(month_tots, f"Expenses for {current_month}")
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info(f"No expenses recorded for {current_month}")

# Edit Expenses
def edit_expense():
    st.subheader("✏️ Edit Existing Expense")
    df = load_expenses()
    if df.empty:
        st.info("No expenses to edit.")
        return
    st.dataframe(gradient_style(df), use_container_width=True)
    index = st.number_input("Enter the index number of the expense to edit", min_value=0, max_value=len(df)-1)
    date = st.date_input("New Date", df.loc[index, "Date"])
    category = st.selectbox("New Category", 
                            ["Food", "Transport", "Stationery", "Internet", "Recreation", "Other"], 
                            index=["Food", "Transport", "Stationery", "Internet", "Recreation", "Other"].index(df.loc[index, "Category"]))
    amount = st.number_input("New Amount", min_value=0.0, format="%.2f", value=float(df.loc[index, "Amount"]))
    description = st.text_input("New Description", value=df.loc[index, "Description"])
    if st.button("Update Expense", key="update_expense_button"):
        if update_expense(index, date, category, amount, description):
            st.success("Expense updated successfully!")
            st.balloons()
    
    # Add delete all button with confirmation
    st.markdown("---")
    st.subheader("⚠️ Danger Zone")
    if st.button("❌ Delete ALL Expenses", key="delete_all_button", help="This will permanently delete all your expense records"):
        if st.warning("Are you sure you want to delete ALL expenses? This action cannot be undone!"):
            if delete_all_expenses():
                st.error("All expenses have been deleted!")
                st.balloons()
            else:
                st.error("Failed to delete expenses. Please try again.")

# About Page
def about_page():
    st.balloons()
    st.markdown('<h1 class="about-header">About Spendr</h1>', unsafe_allow_html=True)
    st.markdown("""
    <p style='text-align: center; font-size: 18px; color: #888888;'>
        Spendr is a personal expense tracking application designed to help you monitor your spending habits 
        and gain financial awareness. With beautiful visualizations and intuitive controls, managing your 
        money has never been easier.
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="about-subheader">🌍 About the Developer</h2>', unsafe_allow_html=True)
    
    # Developer info in columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
                    <br><br> 
        <div style='text-align: center;'>
            <img src='https://media.licdn.com/dms/image/v2/D4D03AQHnjp96gkwCZA/profile-displayphoto-shrink_400_400/B4DZVRSQG5HIAg-/0/1740825496309?e=1756339200&v=beta&t=zOwgJ-pTDxNpTzLHJ7pzer2RFHtDVd_GhwJKQrMzG4E' 
                 style='width: 150px; height: 150px; border-radius: 50%; border: 4px solid #D4AF37;'>
            <h3 style='color:#666666; margin-top: 10px;'>-Haris Farooq</h3>
            <p style='color: #888888;' > UI/UX Enthusiast</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <p style='font-size: 16px; color: #888888;'>
        <br><br>
            Hi! I'm Haris Farooq, a student of BS Artificial Intelligence (Batch 34) at GIK Institute. I'm passionate about using technology to solve real-world problems, especially in the fields of AI, data science, and automation. I love taking on creative challenges and constantly seek opportunities to learn and grow.This is my first Streamlit app, and I'm excited to share it as part of my journey into building interactive, user-friendly tools with real-world impact!
        </p>
        <p style='font-size: 16px;'>
            When I'm not coding, you can find me exploring new technologies, contributing to 
            open-source projects, or enjoying outdoor activities.
        </p>
        """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="about-subheader">🛠️ Technical Skills</h2>', unsafe_allow_html=True)
    st.markdown(""" 
        <br> 
    <div style='text-align: center;'>
        <span class='skill-pill'>Python</span>
        <span class='skill-pill'>Streamlit</span>
        <span class='skill-pill'>Pandas</span>
        <span class='skill-pill'>Plotly</span>
        <span class='skill-pill'>Data Visualization</span>
        <span class='skill-pill'>Web Development</span>
        <span class='skill-pill'>UI/UX Design</span>
        <span class='skill-pill'>Data Analysis</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="about-subheader">🌍 Connect With Me</h2>', unsafe_allow_html=True)
    st.markdown("""
        <br> 
    <div style='text-align: center;'>
        <a href='https://github.com/HarisFarooq23' class='social-icon'>GitHub</a>
        <a href='https://www.linkedin.com/in/harisfarooq23/' class='social-icon'>LinkedIn</a>
        
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="about-subheader">🌍 Special Thanks</h2>', unsafe_allow_html=True)
    st.markdown("""
        <br> 
    <p style='text-align: center; font-size: 16px;color: #888888;'>
        Thank you for using Spendr! If you enjoy this application, please consider starring 
        the project on GitHub or sharing it with friends who might find it useful.
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------
# PREDICTION FUNCTIONS (Integrated from Python code)
# ----------------------------------------------------
def create_enhanced_features(daily_df, monthly_totals):
    rows = []
    
    for month, group in daily_df.groupby("Month"):
        group = group.sort_values("Day")
        month_str = str(month)
        
        if month_str not in monthly_totals.index:
            continue
            
        full_month_total = monthly_totals.loc[month_str]
        total_days_in_month = len(group)
        
        for cutoff_day in range(5, min(25, total_days_in_month)):
            past_days = group[group["Day"] <= cutoff_day]
            future_days = group[group["Day"] > cutoff_day]
            
            if len(past_days) < 3 or len(future_days) < 3:
                continue
                
            past_amounts = past_days["Amount"].values
            future_total = future_days["Amount"].sum()
            remaining_days = len(future_days)
            
            rows.append({
                "Month": month_str,
                "Cutoff_Day": cutoff_day,
                "Days_Used": len(past_days),
                "Remaining_Days": remaining_days,
                "Partial_Sum": np.sum(past_amounts),
                "Avg_Daily": np.mean(past_amounts),
                "Std_Dev": np.std(past_amounts) if len(past_amounts) > 1 else 0,
                "Last_Day_Spend": past_amounts[-1],
                "Max_So_Far": np.max(past_amounts),
                "Min_So_Far": np.min(past_amounts),
                "Avg_Last_3": np.mean(past_amounts[-3:]) if len(past_amounts) >= 3 else np.mean(past_amounts),
                "Avg_Last_7": np.mean(past_amounts[-7:]) if len(past_amounts) >= 7 else np.mean(past_amounts),
                "Trend_3_Days": past_amounts[-1] - np.mean(past_amounts[-4:-1]) if len(past_amounts) >= 4 else 0,
                "Spend_Ratio": (np.max(past_amounts) - np.min(past_amounts)) / np.mean(past_amounts) if np.mean(past_amounts) > 0 else 0,
                "Weekend_Count": past_days["Is_Weekend"].sum(),
                "Weekend_Avg": past_days[past_days["Is_Weekend"] == 1]["Amount"].mean() 
                               if (past_days["Is_Weekend"] == 1).any() else np.mean(past_amounts),
                "Target_Future_Total": future_total,
                "Target_Full_Month": full_month_total
            })
    
    return pd.DataFrame(rows)

def predict_remaining_expenses(final_model, first_n_days, days_remaining):
    if days_remaining <= 0:
        return 0
    
    first_n_days = np.array(first_n_days)
    n_days = len(first_n_days)
    
    features = {
        "Days_Used": n_days,
        "Remaining_Days": days_remaining,
        "Partial_Sum": np.sum(first_n_days),
        "Avg_Daily": np.mean(first_n_days),
        "Std_Dev": np.std(first_n_days) if n_days > 1 else 0.01,
        "Last_Day_Spend": first_n_days[-1],
        "Max_So_Far": np.max(first_n_days),
        "Min_So_Far": np.min(first_n_days),
        "Avg_Last_3": np.mean(first_n_days[-3:]) if n_days >= 3 else np.mean(first_n_days),
        "Avg_Last_7": np.mean(first_n_days[-7:]) if n_days >= 7 else np.mean(first_n_days),
        "Trend_3_Days": first_n_days[-1] - np.mean(first_n_days[-4:-1]) if n_days >= 4 else 0,
        "Spend_Ratio": (np.max(first_n_days) - np.min(first_n_days)) / np.mean(first_n_days) 
                      if np.mean(first_n_days) > 0 else 0.5,
        "Weekend_Count": min(n_days // 2, 10),
        "Weekend_Avg": np.mean(first_n_days) * 1.2
    }
    
    input_df = pd.DataFrame([features])
    prediction = final_model.predict(input_df)[0]
    
    if n_days >= 7:
        week1 = np.mean(first_n_days[:min(7, n_days)])
        week2 = np.mean(first_n_days[min(7, n_days):]) if n_days > 7 else week1
        trend = week2 / week1 if week1 > 0 else 1
        trend_factor = 0.7 + 0.3 * min(max(trend, 0.5), 1.5)
        prediction *= trend_factor
    
    prediction *= 0.85
    
    min_pred = np.mean(first_n_days) * days_remaining * 0.5
    max_pred = np.mean(first_n_days) * days_remaining * 2.0
    prediction = max(min_pred, min(prediction, max_pred))
    
    return max(0, round(prediction, 2))

def predict_full_month_from_partial(final_model, first_n_days, total_month_days=30):
    spent_so_far = sum(first_n_days)
    days_remaining = total_month_days - len(first_n_days)
    
    if days_remaining <= 0:
        return {
            "spent_so_far": spent_so_far,
            "predicted_remaining": 0,
            "predicted_full_month": spent_so_far,
            "daily_average_so_far": spent_so_far / len(first_n_days),
            "predicted_daily_remaining": 0,
            "days_used": len(first_n_days),
            "days_remaining": 0
        }
    
    predicted_remaining = predict_remaining_expenses(final_model, first_n_days, days_remaining)
    full_month_prediction = spent_so_far + predicted_remaining
    
    return {
        "spent_so_far": spent_so_far,
        "predicted_remaining": predicted_remaining,
        "predicted_full_month": full_month_prediction,
        "daily_average_so_far": spent_so_far / len(first_n_days),
        "predicted_daily_remaining": predicted_remaining / days_remaining if days_remaining > 0 else 0,
        "days_used": len(first_n_days),
        "days_remaining": days_remaining
    }

def predictions_page():
    st.subheader("🔮 AI Expense Predictions")
    
    with st.expander("ℹ️ About the AI Model"):
        st.markdown("""
        This feature uses machine learning to predict your future expenses based on your spending patterns.
        
        **Features:**
        - Uses Random Forest, Gradient Boosting, and Linear Regression models
        - Analyzes trends, moving averages, and weekend spending patterns
        - Predicts remaining month expenses from partial data
        - Automatically selects the best performing model
        """)
    
    # Check if we have enough data
    df = load_expenses()
    if len(df) < 30:
        st.warning("⚠️ We need at least 30 days of expense data for accurate predictions.")
        st.info("Please add more expenses through the 'Add Expense' page.")
        return
    
    # Show data loading progress
    with st.spinner("Training AI model on your expense data..."):
        # Prepare data
        df = df.copy()
        df["Date"] = pd.to_datetime(df["Date"])
        daily = df.groupby("Date")["Amount"].sum().reset_index()
        daily["Month"] = daily["Date"].dt.to_period("M")
        daily["Day"] = daily["Date"].dt.day
        daily["Day_of_Week"] = daily["Date"].dt.dayofweek
        daily["Is_Weekend"] = daily["Day_of_Week"].isin([5, 6]).astype(int)
        monthly_totals = daily.groupby("Month")["Amount"].sum()
        
        # Create training data
        training_df = create_enhanced_features(daily, monthly_totals)
        
        if len(training_df) < 10:
            st.error("Not enough data points for training. Please add more expenses.")
            return
        
        feature_cols = [
            "Days_Used", "Remaining_Days", "Partial_Sum", "Avg_Daily", "Std_Dev",
            "Last_Day_Spend", "Max_So_Far", "Min_So_Far", 
            "Avg_Last_3", "Avg_Last_7", "Trend_3_Days", "Spend_Ratio",
            "Weekend_Count", "Weekend_Avg"
        ]
        
        X = training_df[feature_cols]
        y = training_df["Target_Future_Total"]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.20, random_state=42, shuffle=True
        )
        
        # Train models
        models = {
            "Random Forest": RandomForestRegressor(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            ),
            "Gradient Boosting": GradientBoostingRegressor(
                n_estimators=150,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            ),
            "Linear Regression": LinearRegression()
        }
        
        best_model = None
        best_score = -np.inf
        model_results = {}
        
        for name, model in models.items():
            cv_scores = cross_val_score(model, X_train, y_train, 
                                        cv=5, scoring='neg_mean_absolute_error')
            avg_mae = -cv_scores.mean()
            
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            r2 = r2_score(y_test, y_pred)
            
            if r2 > best_score:
                best_score = r2
                best_model = model
                best_model_name = name
        
        final_model = best_model
        final_model.fit(X_train, y_train)
        y_pred_final = final_model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred_final)
        r2 = r2_score(y_test, y_pred_final)
    
    st.success(f"✅ Model trained successfully! Using: **{best_model_name}**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Model Accuracy (R²)", f"{r2:.3f}")
    with col2:
        st.metric("Average Error (MAE)", f"PKR {mae:.2f}")
    
    st.markdown("---")
    
    # Interactive prediction section
    st.subheader("🎯 Make Predictions")
    
    current_month = datetime.now().strftime("%B %Y")
    current_day = datetime.now().day
    
    col1, col2 = st.columns(2)
    with col1:
        days_used = st.number_input(
            "Days of expenses available this month", 
            min_value=1, max_value=29, value=min(current_day, 29)
        )
    with col2:
        total_days = st.number_input(
            "Total days in month", 
            min_value=28, max_value=31, value=30
        )
    
    st.markdown("**Enter your daily expenses for this month:**")
    
    daily_expenses = []
    cols = st.columns(min(days_used, 7))
    
    for i in range(days_used):
        with cols[i % 7]:
            daily_expenses.append(st.number_input(
                f"Day {i+1}", 
                min_value=0.0, 
                value=float(np.random.randint(1000, 8000)) if i < len(daily_expenses) else 0.0,
                key=f"day_{i}"
            ))
    
    if st.button("🔮 Predict Future Expenses", type="primary"):
        if sum(daily_expenses) == 0:
            st.warning("Please enter some expense values.")
        else:
            result = predict_full_month_from_partial(final_model, daily_expenses, total_days)
            
            st.markdown("---")
            st.subheader("📊 Prediction Results")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Spent So Far", f"PKR {result['spent_so_far']:.2f}")
            with col2:
                st.metric("Predicted Remaining", f"PKR {result['predicted_remaining']:.2f}")
            with col3:
                st.metric("Full Month Prediction", f"PKR {result['predicted_full_month']:.2f}")
            
            st.markdown("---")
            
            # Visual comparison
            st.subheader("📈 Comparison Chart")
            
            categories = ['Spent So Far', 'Predicted Remaining']
            values = [result['spent_so_far'], result['predicted_remaining']]
            
            fig = go.Figure(data=[
                go.Bar(name='Actual vs Predicted', x=categories, y=values,
                      marker_color=['#00BFFF', '#D4AF37'])
            ])
            
            fig.update_layout(
                title='Spending Breakdown',
                xaxis_title="Category",
                yaxis_title="Amount (PKR)",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Daily averages comparison
            st.subheader("📊 Daily Averages Comparison")
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "Current Daily Average", 
                    f"PKR {result['daily_average_so_far']:.2f}",
                    help="Average daily spending so far"
                )
            with col2:
                st.metric(
                    "Predicted Daily Average (Remaining)", 
                    f"PKR {result['predicted_daily_remaining']:.2f}",
                    delta=f"{result['predicted_daily_remaining'] - result['daily_average_so_far']:.2f}",
                    delta_color="normal"
                )
            
            # Advice based on prediction
            st.markdown("---")
            st.subheader("💡 Spending Insights")
            
            if result['predicted_daily_remaining'] > result['daily_average_so_far'] * 1.2:
                st.warning("⚠️ You're predicted to spend **more** in the remaining days. Consider tightening your budget.")
            elif result['predicted_daily_remaining'] < result['daily_average_so_far'] * 0.8:
                st.success("✅ You're predicted to spend **less** in the remaining days. Great job!")
            else:
                st.info("📊 Your spending is predicted to remain relatively consistent.")
            
            # Simple projection vs model comparison
            simple_projection = result['daily_average_so_far'] * total_days
            st.metric(
                "Simple Projection (avg × total days)", 
                f"PKR {simple_projection:.2f}",
                delta=f"{result['predicted_full_month'] - simple_projection:.2f}",
                delta_color="normal",
                help="Difference between simple projection and AI prediction"
            )


# Main App
init_csv()
if "page_loaded" not in st.session_state:
    loading_screen()
    st.session_state.page_loaded = True

# Sidebar navigation with golden theme
with st.sidebar:
    # Coin Logo and Title with golden styling
    st.markdown("""
    <div style="text-align:center; margin-bottom:20px;">
        <svg width="60" height="60" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" style="margin:0 auto;" class="coin-logo">
            <circle cx="12" cy="12" r="10" fill="#D4AF37" stroke="#996515" stroke-width="2"/>
            <text x="12" y="16" font-family="Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="#000000">$</text>
        </svg>
        <h1 style="color:#D4AF37; margin-top:5px; text-shadow: 1px 1px 3px rgba(0,0,0,0.3);">Spendr</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation with golden selection effect - ADDED PREDICTIONS OPTION
    menu = st.radio(
        "Navigation",
        ["Dashboard", "Add Expense", "View Expenses", "Edit Expenses", "Predictions", "About"],
        index=0,
        key="nav"
    )
    
    # Footer with golden accent
    st.markdown("---")
    st.markdown(
        """<div style="text-align:center; color:#D4AF37; font-size:12px;">
        Track every penny • Spend wisely
        </div>""",
        unsafe_allow_html=True
    )

# Main content area
if menu == "Dashboard":
    dashboard()
elif menu == "Add Expense":
    add_expense()
elif menu == "View Expenses":
    view_expenses()
elif menu == "Edit Expenses":
    edit_expense()
elif menu == "Predictions":  # ADDED NEW MENU OPTION
    predictions_page()
elif menu == "About":
    about_page()
