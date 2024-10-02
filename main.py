import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Membuat Judul
st.title("Visualisasi Hasil Analisis Dataset Penyewaan Sepeda Menggunakan Streamlit")
st.markdown("""
    Dasboard ini berfungsi untuk menampilkan hasil analisis dan visualisasi penyewaan sepeda 
    berdasarkan 2 faktor utama yaitu faktor cuaca dan faktor hari (perbedaan antara hari kerja dan hari libur)
""")

#Menampilkan Dataset
@st.cache_resource
def load_data():
    day_df = pd.read_csv('day.csv')
    hour_df = pd.read_csv('hour.csv')
    return day_df, hour_df

day_df, hour_df = load_data()

# Membuat Sidebar
dataset_option = st.sidebar.selectbox("Pilih Dataset", ("Berdasarkan Hari", "Berdasarkan jam"))

# Dataset dapat dilihat dan dipilih untuk ditampilkan pada menu sidebar
if dataset_option == "Hari":
    st.subheader("Dataset Hari")
    st.dataframe(day_df.head())
else:
    st.subheader("Dataset Jam")
    st.dataframe(hour_df.head())

# Scatter Plot
st.subheader(" Hubungan Faktor Cuaca dengan Jumlah Penyewaan Sepeda ")

x_axis = st.selectbox("Pilih Faktor Cuaca untuk X-Axis", ["temp", "hum", "windspeed"])
y_axis = "cnt"

fig, ax = plt.subplots()
sns.scatterplot(x=day_df[x_axis], y=day_df[y_axis], ax=ax)
ax.set_xlabel(x_axis.capitalize())
ax.set_ylabel("Jumlah Penyewaan Sepeda")
ax.set_title(f"Scatter Plot: {x_axis.capitalize()} vs Jumlah Penyewaan Sepeda")

st.pyplot(fig)

# Analisis Data Berdasarkan Musim dan Hari Kerja
st.subheader("Analisis Berdasarkan Musim dan Hari Kerja")

season_option = st.selectbox("Pilih Musim", ["1: Dingin", "2: Hujan", "3: Panas", "4: Gugur"])
workingday_option = st.radio("Pilih Hari Kerja", ["1: Hari Kerja", "0: Hari Libur"])

filtered_data = day_df[(day_df['season'] == int(season_option[0])) & (day_df['workingday'] == int(workingday_option[0]))]

st.write(f"Data penyewaan sepeda pada musim {season_option} dan {'hari kerja' if workingday_option == '1: Hari Kerja' else 'Hari Libur'}:")
st.dataframe(filtered_data.head())

# Analisis Jumlah Penyewaan
st.subheader("Rata-rata Jumlah Penyewaan Berdasarkan Musim dan Hari Kerja")
avg_rentals = filtered_data['cnt'].mean()
st.metric(label="Rata-rata Penyewaan Sepeda", value=f"{avg_rentals:.2f}")

# Pilihan variabel untuk X-Axis
x_axis = st.selectbox("Pilih Faktor ", ["season", "workingday", "weathersit"])

# Box Plot
y_axis = "cnt"

fig, ax = plt.subplots()
sns.boxplot(x=day_df[x_axis], y=day_df[y_axis], color="grey", ax=ax)

# Set judul dan label
ax.set_xlabel(x_axis.capitalize())
ax.set_ylabel("Jumlah Penyewaan Sepeda")
ax.set_title(f"Box Plot: {x_axis.capitalize()} vs Jumlah Penyewaan Sepeda (cnt)")

# Tampilkan plot di Streamlit
st.pyplot(fig)