import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "olympics2024.csv")
    df = pd.read_csv(file_path)
    return df


# Set page config
st.set_page_config(
    page_title="Olympics 2024 Medal Analysis",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('olympics2024.csv')
    df['Gold_percent'] = df['Gold'] / df['Total'] * 100
    return df

df = load_data()

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Medal Calculator", "Country Analysis"])

if page == "Overview":
    # Title and description
    st.title("🏅 Olympics 2024 Medal Analysis")
    st.markdown("""
        Explore the fascinating world of Olympic medals! This interactive dashboard provides insights into 
        medal distribution and country performance at the Paris 2024 Olympics.
    """)

    # Key Statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Countries", len(df))
    with col2:
        st.metric("Total Medals Awarded", df['Total'].sum())
    with col3:
        st.metric("Average Medals per Country", round(df['Total'].mean(), 1))

    # Top 10 Countries by Total Medals
    st.subheader("Top 10 Countries by Total Medals")
    top_10 = df.nlargest(10, 'Total')
    fig = px.bar(top_10, x='Country', y=['Gold', 'Silver', 'Bronze'],
                 title='Medal Distribution for Top 10 Countries',
                 barmode='stack')
    st.plotly_chart(fig, use_container_width=True)

    # Medal Distribution Scatter Plot
    st.subheader("Medal Distribution Analysis")
    fig = px.scatter(df, x='Total', y='Gold', 
                    size='Total', color='Gold',
                    hover_data=['Country'],
                    title='Gold vs Total Medals Distribution')
    st.plotly_chart(fig, use_container_width=True)

elif page == "Medal Calculator":
    st.subheader("🏆 Gold Dominance Calculator")
    st.markdown("""
        Calculate how dominant a country's gold medal performance is compared to their total medals.
        A country is considered 'Gold Dominant' if more than 40% of their medals are gold!
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        country = st.selectbox("Select a Country", df['Country'].tolist())
    with col2:
        gold_medals = st.number_input("Number of Gold Medals", min_value=0, max_value=100)
        total_medals = st.number_input("Total Medals", min_value=0, max_value=200)
    
    if gold_medals > 0 and total_medals > 0:
        gold_percent = (gold_medals / total_medals) * 100
        st.metric("Gold Medal Percentage", f"{gold_percent:.1f}%")
        
        if gold_percent > 40:
            st.success("🏆 Gold Dominant Performance!")
        elif 30 <= gold_percent <= 40:
            st.info("⚖️ Balanced Performance")
        else:
            st.warning("🥈 Bronze/Silver Heavy Performance")

elif page == "Country Analysis":
    st.subheader("Detailed Country Analysis")
    
    selected_country = st.selectbox("Select a Country", df['Country'].tolist())
    country_data = df[df['Country'] == selected_country].iloc[0]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Rank", country_data['Rank'])
    with col2:
        st.metric("Gold Medals", country_data['Gold'])
    with col3:
        st.metric("Silver Medals", country_data['Silver'])
    with col4:
        st.metric("Bronze Medals", country_data['Bronze'])
    
    # Medal distribution pie chart
    fig = px.pie(values=[country_data['Gold'], country_data['Silver'], country_data['Bronze']],
                 names=['Gold', 'Silver', 'Bronze'],
                 title=f'Medal Distribution for {selected_country}')
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Data source: [Kaggle - Paris 2024 Olympics Medals](https://www.kaggle.com/datasets/berkayalan/paris-2024-olympics-medals)") 
