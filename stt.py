import streamlit as st
import math as mt
import random as r

def randomize(button):
    if button:
        st.write("Random number:", r.randint(1, 100))

a=st.button("Generate Random Number")
randomize(a)