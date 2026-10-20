import streamlit as st
import random as r

# 1. set_page_config her zaman dosyadaki İLK Streamlit komutu olmalıdır
st.set_page_config(page_title="Random Number Generator and Math Operations", page_icon="🔢", layout="wide")

st.title("Random Number Generator and Math Operations")
st.info("This app generates a random number between 1 and 100 or performs basic math operations (addition, subtraction, multiplication, division) on two numbers.")

# Sayfa akışını kontrol etmek için radio buton kullanmak Streamlit'te en sağlıklı yöntemdir
app_mode = st.radio("Select Mode:", ["Random Number Generator", "Math Operations"])

if app_mode == "Random Number Generator":
    if st.button("Generate Random Number"):
        st.write("Random number:", r.randint(1, 100))

elif app_mode == "Math Operations":
    f1 = st.number_input("Enter a number:", value=0.0)
    f2 = st.number_input("Enter another number:", value=0.0)
    
    # Butonları yan yana veya alt alta düzenleyebilirsiniz
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        toplama = st.button("Toplama (+)")
    with col2:
        cıkarma = st.button("Çıkarma (-)")
    with col3:
        carpma = st.button("Çarpma (*)")
    with col4:
        bolme = st.button("Bölme (/)")

    if toplama:
        st.write("Toplam:", f1 + f2)
    elif cıkarma:
        st.write("Fark:", f1 - f2)
    elif carpma:
        st.write("Çarpım:", f1 * f2)
    elif bolme:
        if f2 != 0:
            st.write("Bölüm:", f1 / f2)
        else:
            st.error("Bir sayı 0'a bölünemez!")