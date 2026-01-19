import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io

# --- 1. Configurazione ---
st.set_page_config(page_title="Tactical Board", page_icon="⚽", layout="centered")

st.markdown("""
<style>
    div[data-baseweb="select"] > div, div[data-baseweb="select"] input { cursor: pointer !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. Database Formazioni (Coordinate 0-100% Campo) ---
tactics_db = {
    "Calcio a 5": {
        "dims": (25, 40),
        "formations": {
            "1-2-1": [{'name':'P','r':'P','p':(12.5,2)},{'name':'D','r':'D','p':(12.5,8)},{'name':'LS','r':'C','p':(4,18)},{'name':'LD','r':'C','p':(21,18)},{'name':'PIV','r':'F','p':(12.5,30)}],
            "2-2":   [{'name':'P','r':'P','p':(12.5,2)},{'name':'DS','r':'D','p':(6,10)},{'name':'DD','r':'D','p':(19,10)},{'name':'AS','r':'F','p':(6,28)},{'name':'AD','r':'F','p':(19,28)}]
        }
    },
    "Calcio a 7": {
        "dims": (45, 60),
        "formations": {
            "3-2-1": [{'name':'P','r':'P','p':(22.5,3)},{'name':'DS','r':'D','p':(8,12)},{'name':'DC','r':'D','p':(22.5,10)},{'name':'DD','r':'D','p':(37,12)},{'name':'CS','r':'C','p':(15,25)},{'name':'CD','r':'C','p':(30,25)},{'name':'ATT','r':'F','p':(22.5,45)}],
            "2-3-1": [{'name':'P','r':'P','p':(22.5,3)},{'name':'DS','r':'D','p':(12,12)},{'name':'DD','r':'D','p':(33,12)},{'name':'ES','r':'C','p':(5,25)},{'name':'CC','r':'C','p':(22.5,22)},{'name':'ED','r':'C','p':(40,25)},{'name':'ATT','r':'F','p':(22.5,45)}]
        }
    },
    "Calcio a 9": {
        "dims": (60, 70),
        "formations": {
            "3-3-2": [{'name':'P','r':'P','p':(30,4)},{'name':'DS','r':'D','p':(10,15)},{'name':'DC','r':'D','p':(30,12)},{'name':'DD','r':'D','p':(50,15)},{'name':'CS','r':'C','p':(15,30)},{'name':'CC','r':'C','p':(30,28)},{'name':'CD','r':'C','p':(45,30)},{'name':'AS','r':'F','p':(20,55)},{'name':'AD','r':'F','p':(40,55)}],
            "3-4-1": [{'name':'P','r':'P','p':(30,4)},{'name':'DS','r':'D','p':(12,15)},{'name':'DC','r':'D','p':(30,12)},{'name':'DD','r':'D','p':(48,15)},{'name':'ES','r':'C','p':(8,30)},{'name':'CCS','r':'C','p':(22,28)},{'name':'CCD','r':'C','p':(38,28)},{'name':'ED','r':'C','p':(52,30)},{'name':'ATT','r':'F','p':(30,55)}],
            "4-3-1": [{'name':'P','r':'P','p':(30,4)},{'name':'DS','r':'D','p':(8,15)},{'name':'DCS','r':'D','p':(22,12)},{'name':'DCD','r':'D','p':(38,12)},{'name':'DD','r':'D','p':(52,15)},{'name':'ES','r':'C','p':(12,30)},{'name':'CCS','r':'C','p':(30,28)},{'name':'ED','r':'C','p':(48,30)},{'name':'ATT','r':'F','p':(30,55)}]
        }
    },
    "Calcio a 11": {
        "dims": (68, 105),
        "formations": {
            "4-3-3": [{'name':'P','r':'P','p':(34,4)},{'name':'TS','r':'D','p':(8,20)},{'name':'DCS','r':'D','p':(25,16)},{'name':'DCD','r':'D','p':(43,16)},{'name':'TD','r':'D','p':(60,20)},{'name':'CC','r':'C','p':(34,35)},{'name':'CS','r':'C','p':(20,45)},{'name':'CD','r':'C','p':(48,45)},{'name':'AS','r':'F','p':(10,80)},{'name':'ATT','r':'F','p':(34,85)},{'name':'AD','r':'F','p':(58,80)}],
            "4-4-2": [{'name':'P','r':'P','p':(34,4)},{'name':'TS','r':'D','p':(10,20)},{'name':'DCS','r':'D','p':(26,16)},{'name':'DCD','r':'D','p':(42,16)},{'name':'TD','r':'D','p':(58,20)},{'name':'ES','r':'C','p':(10,50)},{'name':'CCS','r':'C','p':(26,45)},{'name':'CCD','r':'C','p':(42,45)},{'name':'ED','r':'C','p':(58,50)},{'name':'PS','r':'F','p':(25,75)},{'name':'PD','r':'F','p':(43,75)}]
        }
    }
}

# --- 3. Sidebar ---
st.title("⚽ Tactical Board")

with st.sidebar:
    mode = st.radio("Modalità:", ["Lavagna Tattica", "Match Analysis"], horizontal=True)
    st.divider()

    game_type = st.selectbox("Tipo di campo", list(tactics_db.keys()))
    dims = tactics_db[game_type]["dims"]
    formations_list = list(tactics_db[game_type]["formations"].keys())
    
    home_players = []
    away_players = None
    colors_h = (None, None)
    colors_a = (None, None)

    # --- INPUT DATI ---
    if mode == "Lavagna Tattica":
        st.subheader("La tua Formazione")
        f_name = st.selectbox("Modulo", formations_list)
        col_c1, col_c2 = st.columns(2)
        c_fill = col_c1.color_picker("Maglia", "#D92027") 
        c_gk = col_c2.color_picker("Portiere", "#FFD700")
        colors_h = (c_fill, c_gk)
        
        st.caption("Giocatori")
        raw_data = tactics_db[game_type]["formations"][f_name]
        for i, p in enumerate(raw_data):
            col1, col2 = st.columns([1, 3])
            col1.markdown(f"<div style='margin-top:5px;font-weight:bold'>{p['r']}</div>", unsafe_allow_html=True)
            val = col2.text_input(f"n_{i}", p['name'], key=f"s_{i}", label_visibility="collapsed")
            p_copy = p.copy()
            p_copy['name'] = val
            home_players.append(p_copy)

    else: # Match Analysis
        tab_home, tab_away = st.tabs(["🏠 NOI", "✈️ LORO"])
        
        with tab_home:
            f_home_name = st.selectbox("Modulo Noi", formations_list, key="fh")
            col_h1, col_h2 = st.columns(2)
            ch_f = col_h1.color_picker("Maglia", "#D92027", key="chf")
            ch_g = col_h2.color_picker("Portiere", "#FFD700", key="chg")
            colors_h = (ch_f, ch_g)
            
            raw_home = tactics_db[game_type]["formations"][f_home_name]
            for i, p in enumerate(raw_home):
                col1, col2 = st.columns([1,3])
                col1.caption(f"**{p['r']}**")
                val = col2.text_input("n", p['name'], key=f"h_{i}", label_visibility="collapsed")
                p_copy = p.copy()
                p_copy['name'] = val
                home_players.append(p_copy)
        
        with tab_away:
            f_away_name = st.selectbox("Modulo Loro", formations_list, key="fa")
            col_a1, col_a2 = st.columns(2)
            ca_f = col_a1.color_picker("Maglia", "#1E90FF", key="caf")
            ca_g = col_a2.color_picker("Portiere", "#000000", key="cag")
            colors_a = (ca_f, ca_g)
            
            raw_away = tactics_db[game_type]["formations"][f_away_name]
            away_players = []
            for i, p in enumerate(raw_away):
                col1, col2 = st.columns([1,3])
                col1.caption(f"**{p['r']}**")
                val = col2.text_input("n", p['name'], key=f"a_{i}", label_visibility="collapsed")
                p_copy = p.copy()
                p_copy['name'] = val
                away_players.append(p_copy)

    st.divider()
    c_border = st.color_picker("Bordo Pedine", "#FFFFFF")
    f_color = st.color_picker("Sfondo Campo", "#2E8B57")

# --- 4. Funzione Disegno ---
def draw_board(mode, dim, team_home, team_away, col_home, col_away, border, field_bg):
    W, L = dim
    
    # Setup Figura
    if mode == "Lavagna Tattica":
        fig, ax = plt.subplots(figsize=(8, 7))
        ylim_max = L / 2 + 2 
    else:
        fig, ax = plt.subplots(figsize=(8, 11))
        ylim_max = L + 2

    fig.patch.set_facecolor(field_bg)
    ax.set_facecolor(field_bg)
    ax.set_aspect('equal')
    
    lc = "white"
    lw = 2
    
    # Campo
    ax.add_patch(patches.Rectangle((0, 0), W, L, edgecolor=lc, facecolor='none', linewidth=lw))
    ax.plot([0, W], [L/2, L/2], color=lc, linewidth=lw)
    r_circle = 9.15 if W > 50 else 3.0
    ax.add_patch(patches.Circle((W/2, L/2), r_circle, edgecolor=lc, facecolor='none', linewidth=lw))
    ax.add_patch(patches.Circle((W/2, L/2), 0.4, color=lc))
    
    # Aree
    if W > 50:
        bw, bh, sbw, sbh, py, gw = 40.32, 16.5, 18.32, 5.5, 11, 7.32
    else:
        bw, bh, sbw, sbh, py, gw = W*0.7, L*0.15, 0, 0, 6, 3.0
        
    def draw_area(base_y, is_top=False):
        y_box = base_y - bh if is_top else base_y
        y_small = base_y - sbh if is_top else base_y
        y_goal = base_y if is_top else base_y - 1.5
        y_spot = base_y - py if is_top else base_y + py
        
        ax.add_patch(patches.Rectangle(((W-bw)/2, y_box), bw, bh, edgecolor=lc, facecolor='none', linewidth=lw))
        if sbw > 0: ax.add_patch(patches.Rectangle(((W-sbw)/2, y_small), sbw, sbh, edgecolor=lc, facecolor='none', linewidth=1.5))
        ax.scatter(W/2, y_spot, color=lc, s=15)
        ax.add_patch(patches.Rectangle(((W-gw)/2, y_goal), gw, 1.5, edgecolor=lc, facecolor='none', linewidth=2, alpha=0.6))

    draw_area(0, is_top=False)
    if mode == "Match Analysis":
        draw_area(L, is_top=True)
    
    # --- OFFSET ---
    # Impostato esattamente a 0.75 come richiesto
    text_offset = 0.9
    
    # --- DISEGNO SQUADRA 1 (CASA) - Sempre in basso ---
    for p in team_home:
        x, y = p['p']
        
        # COMPRESSIONE 50%: Schiaccia tutto nella metà inferiore
        y = y * 0.48 + 1 
            
        c = col_home[1] if p['r'] == 'P' else col_home[0]
        ax.scatter(x, y, s=600, color=c, edgecolor=border, linewidth=2.5, zorder=10)
        
        ax.text(x, y - text_offset, p['name'], color='white', ha='center', va='top', 
                fontweight='bold', fontsize=8, zorder=11,
                bbox=dict(facecolor='black', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.1'))

    # --- DISEGNO SQUADRA 2 (OSPITI) - Sempre in alto ---
    if mode == "Match Analysis" and team_away is not None:
        for p in team_away:
            x, y = p['p']
            
            y_compressed = y * 0.48 + 1
            y_final = L - y_compressed
            x_final = W - x 
            
            c = col_away[1] if p['r'] == 'P' else col_away[0]
            ax.scatter(x_final, y_final, s=600, color=c, edgecolor=border, linewidth=2.5, zorder=10)
            
            ax.text(x_final, y_final + text_offset, p['name'], color='white', ha='center', va='bottom', 
                    fontweight='bold', fontsize=8, zorder=11,
                    bbox=dict(facecolor='black', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.1'))

    ax.set_xlim(-2, W+2)
    ax.set_ylim(-2, ylim_max)
    ax.axis('off')
    
    return fig

# --- 5. Render ---
fig = draw_board(mode, dims, home_players, away_players, colors_h, colors_a, c_border, f_color)
st.pyplot(fig)

# --- 6. Download ---
fn = "tattica.png"
img = io.BytesIO()
fig.savefig(img, format='png', bbox_inches='tight', facecolor=f_color)
st.download_button("📷 Scarica Immagine", img, fn, "image/png")



