import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(layout="wide")  
st.title("📊 Dashboard Analisis Penyewaan Sepeda")
@st.cache_data
def load_data():
    day_df = pd.read_csv("https://raw.githubusercontent.com/HildaOktaviani/Proyek-Analisis-Data/refs/heads/main/data/day.csv")
    hour_df = pd.read_csv("https://raw.githubusercontent.com/HildaOktaviani/Proyek-Analisis-Data/refs/heads/main/data/hour.csv")
    return day_df, hour_df

day_df, hour_df = load_data()

season_mapping = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}
weather_mapping = {1: "Clear", 2: "Mist", 3: "Light Snow/Rain", 4: "Heavy Rain"}

day_df["season_category"] = day_df["season"].map(season_mapping)
day_df["weather_category"] = day_df["weathersit"].map(weather_mapping)

def categorize_day(row):
    if row["holiday"] == 1:
        return "Holiday"
    elif row["workingday"] == 1:
        return "Working Day"
    else:
        return "Weekend"

day_df["day_type"] = day_df.apply(categorize_day, axis=1)

st.sidebar.header("Filter Data")
selected_season = st.sidebar.multiselect("Pilih Musim", day_df["season_category"].unique(), default=day_df["season_category"].unique())
selected_day_type = st.sidebar.multiselect("Pilih Jenis Hari", day_df["day_type"].unique(), default=day_df["day_type"].unique())
selected_weather = st.sidebar.multiselect("Pilih Kondisi Cuaca", day_df["weather_category"].unique(), default=day_df["weather_category"].unique())

filtered_df = day_df[
    (day_df["season_category"].isin(selected_season)) &
    (day_df["day_type"].isin(selected_day_type)) &
    (day_df["weather_category"].isin(selected_weather))
]

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x="season_category", y="cnt", data=filtered_df, ci=None, palette=["lightblue" if season != "Summer" else "blue" for season in filtered_df["season_category"].unique()])
    plt.xlabel("")
    plt.ylabel("Jumlah Penyewaan Sepeda")
    st.pyplot(fig)

with col2:
    st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Jenis Hari")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x="day_type", y="cnt", data=filtered_df, ci=None, palette=["lightblue" if day != "Working Day" else "blue" for day in filtered_df["day_type"].unique()])
    plt.xlabel("")
    plt.ylabel("Jumlah Penyewaan Sepeda")
    st.pyplot(fig)

with col3:
    st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x="weather_category", y="cnt", data=filtered_df, ci=None, palette=["lightblue" if weather != "Clear" else "blue" for weather in filtered_df["weather_category"].unique()])
    plt.xlabel("")
    plt.ylabel("Jumlah Penyewaan Sepeda")
    st.pyplot(fig)

with col4:
    st.subheader("Perbandingan Casual vs Registered per Musim")
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    axes = axes.flatten()
    for i, season in enumerate(season_mapping.values()):
        season_df = day_df[day_df["season_category"] == season]
        sizes = [season_df["casual"].sum(), season_df["registered"].sum()]
        labels = ["Casual", "Registered"]
        axes[i].pie(sizes, labels=labels, autopct='%1.1f%%', colors=["#ff9999", "#66b3ff"], startangle=90)
        axes[i].set_title(season)
    st.pyplot(fig)

st.subheader("Total Penyewaan Sepeda Harian (30 Hari Terakhir)")
fig, ax = plt.subplots(figsize=(12, 5))
last_30_days = day_df.tail(30)
sns.lineplot(x=last_30_days["dteday"], y=last_30_days["cnt"], marker="o", color="blue")
plt.xticks(rotation=45)
plt.xlabel("Tanggal")
plt.ylabel("Total Penyewaan Sepeda")
st.pyplot(fig)

st.subheader("🔍 Insight")
st.write("- Penyewaan sepeda tertinggi terjadi pada musim panas (Summer) dan hari kerja (Working Day).")
st.write("- Kondisi cuaca yang lebih cerah cenderung meningkatkan jumlah penyewaan sepeda.")