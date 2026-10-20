# Modules
import math as mt
import streamlit as st

# Geometry Formulas
def daire_alan(r):
    return mt.pi * r ** 2
def daire_cevre(r):
    return 2 * mt.pi * r
def kare_alan(a):
    return a ** 2
def kare_cevre(a):
    return 4 * a
def dikdortgen_alan(a, b):
    return a*b
def dikdortgen_cevre(a, b):
    return 2*(a+b)
def ucgen_alan(a, h):
    return (a*h)/2
def ucgen_cevre(a, b, c):
    return a+b+c
def paralelkenar_alan(a, h):
    return a*h
def paralelkenar_cevre(a, b):
    return 2*(a+b)
def yamuk_alan(a, b, h):
    return ((a+b)*h)/2
def yamuk_cevre(a, b, c, d):
    return a+b+c+d
def elips_alan(a, b):
    return mt.pi * a * b
def elips_cevre(a, b):
    return mt.pi * (3*(a+b) - mt.sqrt((3*a + b)*(a + 3*b)))
def koordinat_uzaklik3D(x1,x2,y1,y2,z1,z2):
    return mt.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
def koordinat_uzaklik2D(x1,x2,y1,y2):
    return mt.sqrt((x2-x1)**2 + (y2-y1)**2)


st.set_page_config(
    page_title="IB Math App",
    page_icon=":bar_chart:",
    layout="wide"
)

st.write(
    "📐✏️ IB Math "
)

st.sidebar.header("🗃️ Choose a category")
ana_kategori = st.sidebar.radio(
    "Select a category",
    ["Main Page","Geometry", "Algebra", "Calculus", "Statistics", "Probability"]
)