import pickle 
import streamlit as st
import mysql.connector

# Membaca model
diabetes_model = pickle.load(open('diabetes_model.sav', 'rb'))

def simpan_hasil_ke_database(age, gender, bmi, sbp, dbp, fpg, chol, ffpg, hasil_klasifikasi):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database="Diabetes"
        )
        cursor = conn.cursor()

        sql = "INSERT INTO hasil_klasifikasi (Age, Gender, BMI, SBP, DBP, FPG, Chol, FFPG, Diabetes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (age, gender, bmi, sbp, dbp, fpg, chol, ffpg, hasil_klasifikasi)
        
        cursor.execute(sql, val)
        conn.commit()
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        conn.close()

# Judul web
st.title('KLASIFIKASI POTENSI PENYAKIT DIABETES MELLITUS TIPE II PADA PASIEN MENGGUNAKAN ALGORITME NAÏVE BAYES GAUSSIAN')

# Membagi kolom
col1, col2 = st.columns(2)

with col1 :
    Age = st.number_input('Input Nilai Age')

with col2 :
    Gender = st.number_input('Input Nilai Gender')

with col1 :
    BMI = st.number_input('Input Nilai BMI')

with col2 :
    SBP = st.number_input('Input Nilai SBP (Systolic Blood Pressure)')

with col1 :
    DBP = st.number_input('Input Nilai DBP (Diastolic Blood Pressure)')

with col2 :
    FPG = st.number_input('Input Nilai FPG (Fasting Plasma Glucose)')
    
with col1 :
    Chol = st.number_input('Input Nilai Cholesterol')

with col2 :
    FFPG = st.number_input('Input Nilai FFPG (Final Fasting Plasma Glucose)')

# Code untuk prediksi
diabetes_diagnosis = ''

# Tombol untuk prediksi
if st.button('Klasifikasi Diabetes'):
    diabetes_prediction = diabetes_model.predict([[Age, Gender, BMI, SBP, DBP, FPG, Chol, FFPG]])
    
    if(diabetes_prediction[0] == 0):
        diabetes_diagnosis = 'Pasien Tidak Terkena Diabetes'
    else:
        diabetes_diagnosis = 'Pasien Terkena Diabetes'   
    st.success(diabetes_diagnosis)

# Tombol untuk menyimpan hasil klasifikasi ke dalam database
hasil_klasifikasi = st.selectbox("Hasil Klasifikasi", [0, 1])

if st.button("Simpan Hasil Klasifikasi"):
    simpan_hasil_ke_database(Age, Gender, BMI, SBP, DBP, FPG, Chol, FFPG, hasil_klasifikasi)
    st.success("Hasil Klasifikasi berhasil disimpan ke database.")
