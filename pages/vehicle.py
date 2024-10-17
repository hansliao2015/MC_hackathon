import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page title
st.set_page_config(page_title="Vehicle Data Analysis", layout="wide")

# Read CSV file
@st.cache_data
def load_data():
    # Specify dtype for the first column to ensure it's read as string
    df = pd.read_csv("./static/vehicle.csv", thousands=",", dtype={0: str})

    # Process the date column
    def process_date(date_str):
        if not isinstance(date_str, str):
            return pd.NaT
        parts = date_str.replace('年', ' ').replace('月底', '').split()
        year = int(parts[0]) + 1911  # Convert to Western calendar year
        if len(parts) > 1:
            month = int(parts[1])
        else:
            month = 12  # For entries like "92年底"
        return pd.to_datetime(f'{year}-{month:02d}-01')

    df['Date'] = df.iloc[:, 0].apply(process_date)
    
    # Rename columns to English
    column_mapping = {
        '總計': 'Total',
        '汽車': 'Cars',
        '大客車': 'Buses',
        '大貨車': 'Trucks',
        '小客車': 'Sedans',
        '小貨車': 'Vans',
        '特種車': 'Special Vehicles',
        '機車': 'Motorcycles'
    }
    df = df.rename(columns=column_mapping)
    
    # Sort by date
    df = df.sort_values('Date')
    
    return df

df = load_data()

st.title("Taiwan Vehicle Data Analysis")

# Sidebar - Select vehicle types
st.sidebar.header("Select Vehicle Types")
vehicle_types = [col for col in df.columns if col not in ['Date', 'Total']]
selected_types = st.sidebar.multiselect("Choose vehicle types to analyze", vehicle_types, default=vehicle_types[:3])

# Main content
st.header("Vehicle Quantity Trends")

# Line chart
fig, ax = plt.subplots(figsize=(12, 6))
for vehicle_type in selected_types:
    ax.plot(df['Date'], df[vehicle_type], label=vehicle_type)

ax.set_xlabel("Date")
ax.set_ylabel("Quantity")
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)

# Vehicle type distribution
st.header("Vehicle Type Distribution")
latest_data = df.iloc[-1][selected_types]
fig, ax = plt.subplots(figsize=(10, 10))
wedges, texts, autotexts = ax.pie(latest_data, labels=selected_types, autopct='%1.1f%%', pctdistance=0.85)

# Improve label visibility
ax.legend(wedges, selected_types,
          title="Vehicle Types",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

plt.setp(autotexts, size=8, weight="bold")
ax.set_title("Latest Vehicle Type Distribution")
st.pyplot(fig)

# Statistical information
st.header("Statistical Information")
st.dataframe(df[selected_types].describe())

# Correlation analysis
st.header("Vehicle Type Quantity Correlation")
corr = df[selected_types].corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# Raw data
st.header("Raw Data")
st.dataframe(df)

# Debug information
st.header("Debug Information")
st.write("First few rows of the DataFrame:")
st.write(df.head())
st.write("Column names and types:")
st.write(df.dtypes)