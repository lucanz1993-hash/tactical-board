import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io

# --- 1. Configurazione ---
st.set_page_config(page_title="Tactical Board", page_icon="⚽", layout="centered")

# CSS per cursore mano
st.markdown("""
<style>
    div[data-baseweb="select"] > div, div[data-baseweb="select"] input { cursor: pointer !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. Database Formazioni ---
tactics_db = {
    "Calcio a 5": {
        "dims": (25, 40),
        "formations": {
            "1-2-1": [{'name':'P','r':'P','p':(12.5,2)},{'name':'D','r':'D','p':(12.5,8)},{'name':'LS','r':'C','p':(4,18)},{'name':'LD','r':'C','p':(21,18)},{'name':'PIV','r':'F','p':(12.5,25)}],
            "2-2":   [{'name':'P','r':'P','p':(12.5,2)},{'name':'DS','r':'D','p':(6,10)},{'name':'DD','r':'D','p':(19,10)},{'name':'AS','r':'F','p':(6,25)},{'name':'AD','r':'F','p':(19,25)}]
        }
    },
    "Calcio a 7": {
        "dims": (45, 60),
        "formations": {
            "3-2-1": [{'name':'P','r':'P','p':(22.5,3)},{'name':'DS','r':'D','p':(8,12)},{'name':'DC','r':'D','p':(22.5,10)},{'name':'DD','r':'D','p':(37,12)},{'name':'CS','r':'C','p':(15,25)},{'name':'CD','r':'C','p':(30,25)},{'name':'ATT','r':'F','p':(22.5,40)}],
            "2-3-1": [{'name':'P','r':'P','p':(22.5,3)},{'name':'DS','r':'D','p':(12,12)},{'name':'DD','r':'D','p':(33,12)},{'name':'ES','r':'C','p':(5,25)},{'name':'CC','r':'C','p':(22.5,22)},{'name':'ED','r':'C','p':(40,25)},{'name':'ATT','r':'F','p':(22.5,40)}]
        }
    },
    "Calcio a 9": {
        "dims": (60, 70),
        "formations": {
            "3-3-2": [{'name':'P','r':'P','p':(30,4)},{'name':'DS','r':'D','p':(10,15)},{'name':'DC','r':'D','p':(30,12)},{'name':'DD','r':'D','p':(50,15)},{'name':'CS','r':'C','p':(15,30)},{'name':'CC','r':'C','p':(30,28)},{'name':'CD','r':'C','p':(45,30)},{'name':'AS','r':'F','p':(20,45)},{'name':'AD','r':'F','p':(40,45)}],
