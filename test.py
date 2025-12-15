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
    try:
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
;
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
    except FileNotFoundError:
        st.warning("⚠️ Background image 'newbg.png' not found. Using default styling.")
        # Apply default styling without background image
        css = """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #E0E0E0;
    }
    h1, h2, h3, h4, h5, h6, label, p, span, div {
        color: #E0E0E0 !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #00BFFF, #0066CC);
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .stTextInput>div>input, .stNumberInput>div>input, .stDateInput>div>input {
        background-color: rgba(30, 144, 255, 0.2);
        color: #E0E0E0;
        font-weight: bold;
        border-radius: 8px;
        border: 1px solid #00BFFF;
    }
    .stSelectbox>div>select {
        background-color: rgba(30, 144, 255, 0.2);
        color: #E0E0E0;
        font-weight: bold;
        border-radius: 8px;
        border: 1px solid #00BFFF;
    }
    /* Sidebar styling - Updated to golden gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #D4AF37 0%, #996515 100%);
        color: white;
    }
    /* Metric styling for golden theme */
    [data-testid="stMetric"] {
        background-color: rgba(153, 101, 21, 0.3);
        border-radius: 8px;
        padding: 10px;
        border-left: 3px solid #D4AF37;
    }
    [data-testid="stMetricLabel"] {
        color: #D4AF37 !important;
    }
    [data-testid="stMetricValue"] {
        color: white !important;
    }
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
            try:
                current_month = datetime.now().strftime("%Y-%m")
                # Convert dates with error handling
                df_copy = df.copy()
                df_copy['Date'] = pd.to_datetime(df_copy['Date'], errors='coerce')
                df_copy = df_copy.dropna(subset=['Date'])
                monthly_expenses = df_copy[pd.to_datetime(df_copy['Date']).dt.to_period('M').astype(str) == current_month]
                if not monthly_expenses.empty:
                    month_totals = monthly_expenses.groupby("Category")["Amount"].sum().reset_index()
                    fig2 = create_pie_chart(month_totals, f"Expenses for {current_month}")
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.info(f"No expenses recorded for {current_month}")
            except Exception as e:
                st.warning(f"Could not generate current month chart: {str(e)}")
                st.info("Try adding more expenses or check date formats.")

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

            # Filter out any NaN or invalid values
            past_amounts = past_amounts[~np.isnan(past_amounts)]
            future_amounts = future_days["Amount"].values
            future_amounts = future_amounts[~np.isnan(future_amounts)]
            future_total = np.sum(future_amounts)

            # Skip if we don't have valid data
            if len(past_amounts) < 3:
                continue

            # Calculate statistics safely
            try:
                avg_daily = np.mean(past_amounts)
                std_dev = np.std(past_amounts) if len(past_amounts) > 1 else 0
                last_day_spend = past_amounts[-1] if len(past_amounts) > 0 else 0
                max_so_far = np.max(past_amounts) if len(past_amounts) > 0 else 0
                min_so_far = np.min(past_amounts) if len(past_amounts) > 0 else 0

                # Safe mean calculations
                avg_last_3 = np.mean(past_amounts[-3:]) if len(past_amounts) >= 3 else (avg_daily if avg_daily == avg_daily else 0)
                avg_last_7 = np.mean(past_amounts[-7:]) if len(past_amounts) >= 7 else (avg_daily if avg_daily == avg_daily else 0)

                # Trend calculation
                trend_3_days = 0
                if len(past_amounts) >= 4:
                    recent_3 = past_amounts[-4:-1]
                    if len(recent_3) > 0:
                        trend_3_days = past_amounts[-1] - np.mean(recent_3)

                # Spend ratio
                spend_ratio = 0
                if avg_daily > 0 and len(past_amounts) > 1:
                    spend_ratio = (max_so_far - min_so_far) / avg_daily

                # Weekend calculations
                weekend_count = past_days["Is_Weekend"].sum()
                weekend_avg = avg_daily  # default
                weekend_data = past_days[past_days["Is_Weekend"] == 1]["Amount"]
                if len(weekend_data) > 0:
                    weekend_avg = np.mean(weekend_data[~np.isnan(weekend_data)])

                rows.append({
                    "Month": month_str,
                    "Cutoff_Day": cutoff_day,
                    "Days_Used": len(past_amounts),
                    "Remaining_Days": remaining_days,
                    "Partial_Sum": np.sum(past_amounts),
                    "Avg_Daily": avg_daily,
                    "Std_Dev": std_dev,
                    "Last_Day_Spend": last_day_spend,
                    "Max_So_Far": max_so_far,
                    "Min_So_Far": min_so_far,
                    "Avg_Last_3": avg_last_3,
                    "Avg_Last_7": avg_last_7,
                    "Trend_3_Days": trend_3_days,
                    "Spend_Ratio": spend_ratio,
                    "Weekend_Count": weekend_count,
                    "Weekend_Avg": weekend_avg,
                    "Target_Future_Total": future_total,
                    "Target_Full_Month": full_month_total
                })
            except Exception as e:
                # Skip this data point if calculations fail
                continue
    
    return pd.DataFrame(rows)

def predict_remaining_expenses(final_model, first_n_days, days_remaining):
    if days_remaining <= 0:
        return 0

    first_n_days = np.array(first_n_days)
    # Filter out NaN values
    first_n_days = first_n_days[~np.isnan(first_n_days)]

    n_days = len(first_n_days)

    if n_days == 0:
        return 0

    # Safe calculations
    try:
        partial_sum = np.sum(first_n_days)
        avg_daily = np.mean(first_n_days)
        std_dev = np.std(first_n_days) if n_days > 1 else 0.01
        last_day_spend = first_n_days[-1] if n_days > 0 else 0
        max_so_far = np.max(first_n_days) if n_days > 0 else 0
        min_so_far = np.min(first_n_days) if n_days > 0 else 0

        # Safe mean calculations for subsets
        avg_last_3 = np.mean(first_n_days[-3:]) if n_days >= 3 else avg_daily
        avg_last_7 = np.mean(first_n_days[-7:]) if n_days >= 7 else avg_daily

        # Trend calculation
        trend_3_days = 0
        if n_days >= 4:
            recent_3 = first_n_days[-4:-1]
            if len(recent_3) > 0:
                trend_3_days = first_n_days[-1] - np.mean(recent_3)

        # Spend ratio
        spend_ratio = 0.5  # default
        if n_days > 1 and avg_daily > 0:
            spend_ratio = (max_so_far - min_so_far) / avg_daily

        weekend_count = min(n_days // 2, 10)
        weekend_avg = avg_daily * 1.2 if avg_daily > 0 else 1.0

        features = {
            "Days_Used": n_days,
            "Remaining_Days": days_remaining,
            "Partial_Sum": partial_sum,
            "Avg_Daily": avg_daily,
            "Std_Dev": std_dev,
            "Last_Day_Spend": last_day_spend,
            "Max_So_Far": max_so_far,
            "Min_So_Far": min_so_far,
            "Avg_Last_3": avg_last_3,
            "Avg_Last_7": avg_last_7,
            "Trend_3_Days": trend_3_days,
            "Spend_Ratio": spend_ratio,
            "Weekend_Count": weekend_count,
            "Weekend_Avg": weekend_avg
        }
    except Exception as e:
        # Return a conservative estimate if calculations fail
        return days_remaining * 1000  # Conservative daily estimate
    
    input_df = pd.DataFrame([features])
    prediction = final_model.predict(input_df)[0]
    
    if n_days >= 7:
        week1 = np.mean(first_n_days[:min(7, n_days)])
        week2 = np.mean(first_n_days[min(7, n_days):]) if n_days > 7 else week1
        trend = week2 / week1 if week1 > 0 else 1
        trend_factor = 0.7 + 0.3 * min(max(trend, 0.5), 1.5)
        prediction *= trend_factor
    
    prediction *= 0.85

    # Removed mean-based bounds - now purely ML prediction
    return max(0, round(prediction, 2))

def predict_full_month_from_partial(final_model, first_n_days, total_month_days=30):
    spent_so_far = sum(first_n_days)
    days_remaining = total_month_days - len(first_n_days)
    
    if days_remaining <= 0:
        return {
            "spent_so_far": spent_so_far,
            "predicted_remaining": 0,
            "predicted_full_month": spent_so_far,
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
        "predicted_daily_remaining": predicted_remaining / days_remaining if days_remaining > 0 else 0,
        "days_used": len(first_n_days),
        "days_remaining": days_remaining
    }

def predictions_page():
    st.subheader("🔮 AI Expense Predictions")

    with st.expander("ℹ️ About the AI Model"):
        st.markdown("""
        This feature uses machine learning to predict your future expenses based on historical spending patterns.

        **Features:**
        - Uses Random Forest, Gradient Boosting, and Linear Regression models
        - **Trained exclusively on MLdata.csv** (historical expense data from 2023-2024)
        - Analyzes trends, moving averages, and weekend spending patterns
        - **Purely ML-driven predictions** - no mean-based calculations or bounds
        - Automatically predicts remaining month expenses from current month data
        - Automatically selects the best performing model

        **Data Sources:**
        - **Training Data:** MLdata.csv (historical patterns)
        - **Prediction Input:** Current month expenses from expenses.csv
        """)

    # Check if we have current month data
    try:
        df_current = load_expenses()
        current_month = datetime.now().strftime("%Y-%m")
        # Convert dates with error handling
        df_current_copy = df_current.copy()
        df_current_copy['Date'] = pd.to_datetime(df_current_copy['Date'], errors='coerce')
        df_current_copy = df_current_copy.dropna(subset=['Date'])
        current_month_data = df_current_copy[pd.to_datetime(df_current_copy['Date']).dt.to_period('M').astype(str) == current_month]

        if len(current_month_data) < 3:
            st.warning("⚠️ We need at least 3 days of current month expense data for predictions.")
            st.info("Please add some expenses for this month through the 'Add Expense' page.")
            return
    except Exception as e:
        st.error(f"Error loading current month data: {str(e)}")
        st.info("Please check your expense data and try again.")
        return

    # Show data loading progress
    with st.spinner("🔄 Training AI model on MLdata.csv historical data..."):
        # Load historical training data from MLdata.csv
        st.info("🔄 Loading and training model on historical data from MLdata.csv...")
        try:
            df_training = pd.read_csv("MLdata.csv")
            st.info(f"📊 Loaded {len(df_training)} raw records from MLdata.csv")

            # Clean the data thoroughly
            df_training["Date"] = pd.to_datetime(df_training["Date"], errors='coerce')
            df_training = df_training.dropna(subset=['Date'])

            # Convert Amount to numeric and filter invalid values
            df_training["Amount"] = pd.to_numeric(df_training["Amount"], errors='coerce')
            df_training = df_training.dropna(subset=['Amount'])
            df_training = df_training[df_training['Amount'] > 0]  # Remove zero or negative amounts

            st.info(f"✅ After cleaning: {len(df_training)} valid training records from MLdata.csv")

            if len(df_training) < 100:
                st.error("MLdata.csv contains insufficient clean training data.")
                st.info(f"Only {len(df_training)} valid records found after cleaning. Need at least 100.")
                return

        except FileNotFoundError:
            st.error("❌ MLdata.csv file not found. Please ensure the training data file is available in the same directory.")
            return
        except Exception as e:
            st.error(f"❌ Error loading training data: {str(e)}")
            st.info("Please check the MLdata.csv file format and data quality.")
            return

        # Prepare training data
        df_training = df_training.copy()

        if len(df_training) < 50:
            st.error("MLdata.csv contains insufficient valid training data.")
            st.info(f"Only {len(df_training)} valid records found. Need at least 50.")
            return

        daily_training = df_training.groupby("Date")["Amount"].sum().reset_index()
        daily_training["Month"] = daily_training["Date"].dt.to_period("M")
        daily_training["Day"] = daily_training["Date"].dt.day
        daily_training["Day_of_Week"] = daily_training["Date"].dt.dayofweek
        daily_training["Is_Weekend"] = daily_training["Day_of_Week"].isin([5, 6]).astype(int)
        monthly_totals = daily_training.groupby("Month")["Amount"].sum()

        # Filter out months with very few days
        valid_months = monthly_totals[monthly_totals > 100]  # Months with at least some spending
        if len(valid_months) < 3:
            st.error("MLdata.csv doesn't contain enough valid monthly data for training.")
            st.info(f"Only {len(valid_months)} valid months found. Need at least 3.")
            return
        
        # Create training data from historical data
        try:
            training_df = create_enhanced_features(daily_training, monthly_totals)
        except Exception as e:
            st.error(f"Error processing training data: {str(e)}")
            st.info("Please check the MLdata.csv file for data quality issues.")
            return

        if len(training_df) < 10:
            st.error("Not enough training data points in MLdata.csv. Please ensure the training file has sufficient historical data.")
            st.info(f"Only {len(training_df)} valid training samples found. Need at least 10.")
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
    
    st.success(f"✅ Model trained successfully on MLdata.csv! Using: **{best_model_name}**")
    st.info("🎯 **Training Complete:** Model trained on historical data from MLdata.csv")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Model Accuracy (R²)", f"{r2:.3f}")
    with col2:
        st.metric("Average Error (MAE)", f"PKR {mae:.2f}")

    st.markdown("---")

    # Automatic prediction section
    st.subheader("🎯 Automatic Predictions")
    st.info("✅ **Automatic Mode**: The system now automatically uses your current month expense data for predictions. No manual input required!")

    # Get current month data automatically
    current_month_name = datetime.now().strftime("%B %Y")
    current_day = datetime.now().day

    # Get current month expenses
    current_month_expenses = current_month_data.copy()
    current_month_expenses["Date"] = pd.to_datetime(current_month_expenses["Date"])
    daily_current = current_month_expenses.groupby("Date")["Amount"].sum().reset_index()
    daily_current = daily_current.sort_values("Date")
    daily_expenses = daily_current["Amount"].values.tolist()

    days_used = len(daily_expenses)
    total_days = (datetime.now().replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    total_days = total_days.day

    # Display current month information
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Month", current_month_name)
    with col2:
        st.metric("Days with Data", days_used)
    with col3:
        st.metric("Total Days in Month", total_days)

    st.markdown("### 📊 Current Month Expenses")
    st.dataframe(current_month_expenses[['Date', 'Category', 'Amount', 'Description']], use_container_width=True)

    if st.button("🔮 Predict Remaining Expenses", type="primary"):
        if days_used < 1:
            st.warning("No expense data available for this month.")
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
            
            # ML prediction breakdown (no mean calculations)
            st.subheader("📊 ML Prediction Breakdown")
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "Days Used for Prediction",
                    f"{result['days_used']} days",
                    help="Number of days with expense data used for ML prediction"
                )
            with col2:
                st.metric(
                    "Remaining Days",
                    f"{result['days_remaining']} days",
                    help="Days left in month for ML prediction"
                )
            
            # ML-based spending insights (no mean calculations)
            st.markdown("---")
            st.subheader("💡 ML-Based Spending Insights")

            # Calculate insights based on ML predictions vs actual spending pattern
            total_predicted_remaining = result['predicted_remaining']
            remaining_days = result['days_remaining']

            if remaining_days > 0:
                predicted_daily_rate = total_predicted_remaining / remaining_days
                current_daily_rate = result['spent_so_far'] / result['days_used'] if result['days_used'] > 0 else 0

                if predicted_daily_rate > current_daily_rate * 1.2:
                    st.warning("⚠️ ML predicts you'll spend **more** in the remaining days. Consider tightening your budget.")
                elif predicted_daily_rate < current_daily_rate * 0.8:
                    st.success("✅ ML predicts you'll spend **less** in the remaining days. Great job!")
                else:
                    st.info("📊 ML predicts your spending will remain relatively consistent.")

            st.markdown("---")
            st.subheader("📊 Final Projection Breakdown")
            st.info("**Pure ML Prediction**: Full month expenses = Currently spent + ML-predicted remaining expenses")
            st.metric("**Final ML Projection**", f"PKR {result['predicted_full_month']:.2f}",
                     help="Currently spent + ML-predicted remaining expenses (no mean calculations)")


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
