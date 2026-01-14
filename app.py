import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io

# --- 1. Configurazione Pagina ---
st.set_page_config(page_title="Tactical Board", page_icon="⚽", layout="centered")

# --- 1.1 CSS Personalizzato ---
st.markdown("""
<style>
    div[data-baseweb="select"] > div { cursor: pointer !important; }
    div[data-baseweb="select"] input { cursor: pointer !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. Database Formazioni e Dimensioni ---
# Struttura: Tipo Partita -> { 'dimensions': (W, L), 'formations': { ... } }
# Dimensioni approssimative in metri:
# 5v5: 25x40 | 7v7: 40x60 | 9v9: 50x70 | 11v11: 68x105

tactics_db = {
    "Calcio a 5 (Futsal/Calcetto)": {
        "dims": (25, 40), # Larghezza, Lunghezza
        "formations": {
            "1-2-1 (Rombo)": [
                {'name': 'POR', 'role': 'P', 'pos': (12.5, 2)},
                {'name': 'DIF', 'role': 'D', 'pos': (12.5, 10)},
                {'name': 'LS', 'role': 'C', 'pos': (3, 20)},
                {'name': 'LD', 'role': 'C', 'pos': (22, 20)},
                {'name': 'PIV', 'role': 'F', 'pos': (12.5, 32)},
            ],
            "2-2 (Quadrato)": [
                {'name': 'POR', 'role': 'P', 'pos': (12.5, 2)},
                {'name': 'DS', 'role': 'D', 'pos': (6, 12)},
                {'name': 'DD', 'role': 'D', 'pos': (19, 12)},
                {'name': 'AS', 'role': 'F', 'pos': (6, 28)},
                {'name': 'AD', 'role': 'F', 'pos': (19, 28)},
            ]
        }
    },
    "Calcio a 7": {
        "dims": (45, 60),
        "formations": {
            "2-3-1": [
                {'name': 'POR', 'role': 'P', 'pos': (22.5, 4)},
                {'name': 'DS', 'role': 'D', 'pos': (12, 15)},
                {'name': 'DD', 'role': 'D', 'pos': (33, 15)},
                {'name': 'ES', 'role': 'C', 'pos': (5, 30)},
                {'name': 'CC', 'role': 'C', 'pos': (22.5, 28)},
                {'name': 'ED', 'role': 'C', 'pos': (40, 30)},
                {'name': 'ATT', 'role': 'F', 'pos': (22.5, 50)},
            ],
            "3-2-1": [
                {'name': 'POR', 'role': 'P', 'pos': (22.5, 4)},
                {'name': 'DS', 'role': 'D', 'pos': (8, 15)},
                {'name': 'DC', 'role': 'D', 'pos': (22.5, 12)},
                {'name': 'DD', 'role': 'D', 'pos': (37, 15)},
                {'name': 'CS', 'role': 'C', 'pos': (15, 30)},
                {'name': 'CD', 'role': 'C', 'pos': (30, 30)},
                {'name': 'ATT', 'role': 'F', 'pos': (22.5, 48)},
            ]
        }
    },
    "Calcio a 9": {
        "dims": (60, 70),
        "formations": {
            "3-3-2": [
                {'name': 'POR', 'role': 'P', 'pos': (30, 5)},
                {'name': 'DS', 'role': 'D', 'pos': (10, 18)},
                {'name': 'DC', 'role': 'D', 'pos': (30, 15)},
                {'name': 'DD', 'role': 'D', 'pos': (50, 18)},
                {'name': 'CS', 'role': 'C', 'pos': (15, 35)},
                {'name': 'CC', 'role': 'C', 'pos': (30, 32)},
                {'name': 'CD', 'role': 'C', 'pos': (45, 35)},
                {'name': 'AS', 'role': 'F', 'pos': (20, 55)},
                {'name': 'AD', 'role': 'F', 'pos': (40, 55)},
            ],
            "3-4-1": [
                {'name': 'POR', 'role': 'P', 'pos': (30, 5)},
                {'name': 'DS', 'role': 'D', 'pos': (10, 18)},
                {'name': 'DC', 'role': 'D', 'pos': (30, 15)},
                {'name': 'DD', 'role': 'D', 'pos': (50, 18)},
                {'name': 'ES', 'role': 'C', 'pos': (5, 35)},
                {'name': 'CC', 'role': 'C', 'pos': (25, 32)},
                {'name': 'CC', 'role': 'C', 'pos': (35, 32)},
                {'name': 'ED', 'role': 'C', 'pos': (55, 35)},
                {'name': 'ATT', 'role': 'F', 'pos': (30, 55)},
            ]
        }
    },
    "Calcio a 11 (Standard)": {
        "dims": (68, 105),
        "formations": {
            "4-4-2": [
                {'name': 'POR', 'role': 'P', 'pos': (34, 5)},
                {'name': 'TS', 'role': 'D', 'pos': (10, 25)},
                {'name': 'DCS', 'role': 'D', 'pos': (26, 20)},
                {'name': 'DCD', 'role': 'D', 'pos': (42, 20)},
                {'name': 'TD', 'role': 'D', 'pos': (58, 25)},
                {'name': 'ES', 'role': 'C', 'pos': (10, 55)},
                {'name': 'CCS', 'role': 'C', 'pos': (26, 50)},
                {'name': 'CCD', 'role': 'C', 'pos': (42, 50)},
                {'name': 'ED', 'role': 'C', 'pos': (58, 55)},
                {'name': 'PS', 'role': 'F', 'pos': (25, 85)},
                {'name': 'PD', 'role': 'F', 'pos': (43, 85)},
            ],
            "4-3-3": [
                {'name': 'POR', 'role': 'P', 'pos': (34, 5)},
                {'name': 'TS', 'role': 'D', 'pos': (8, 25)},
                {'name': 'DCS', 'role': 'D', 'pos': (25, 20)},
                {'name': 'DCD', 'role': 'D', 'pos': (43, 20)},
                {'name': 'TD', 'role': 'D', 'pos': (60, 25)},
                {'name': 'CC', 'role': 'C', 'pos': (34, 40)},
                {'name': 'CS', 'role': 'C', 'pos': (20, 50)},
                {'name': 'CD', 'role': 'C', 'pos': (48, 50)},
                {'name': 'AS', 'role': 'F', 'pos': (12, 80)},
                {'name': 'ATT', 'role': 'F', 'pos': (34, 90)},
                {'name': 'AD', 'role': 'F', 'pos': (56, 80)},
            ]
        }
    }
}

# --- 3. Sidebar ---
st.title("⚽ Lavagna Tattica")

with st.sidebar:
    st.header("Impostazioni")
    
    # 1. Scelta Tipo Partita
    game_type = st.selectbox("Tipo di partita:", list(tactics_db.keys()))
    
    # Recuperiamo le dimensioni e le formazioni per questo tipo
    current_dims = tactics_db[game_type]["dims"] # (W, L)
    current_formations = tactics_db[game_type]["formations"]
    
    # 2. Scelta Modulo
    chosen_f_name = st.selectbox("Modulo:", list(current_formations.keys()))
    
    st.divider()
    
    st.subheader("Colori")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        c1_fill = st.color_picker("Squadra", "#D92027") 
    with col_c2:
        c_gk_fill = st.color_picker("Portiere", "#FFD700")

    c2_border = st.color_picker("Colore Bordo", "#FFFFFF")
    f_color = st.color_picker("Sfondo Campo", "#2E8B57")
    
    st.divider()
    st.subheader("Nomi Giocatori")
    
    # Lista giocatori modificabile
    current_players = []
    base_players_data = current_formations[chosen_f_name]
    
    for i, p in enumerate(base_players_data):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.caption(f"**{p['role']}**")
        with col2:
            # Usiamo una key univoca che include tipo gioco e formazione
            key_id = f"p_{game_type}_{chosen_f_name}_{i}".replace(" ", "_")
            new_name = st.text_input(f"Pos", value=p['name'], key=key_id, label_visibility="collapsed")
        
        player_copy = p.copy()
        player_copy['name'] = new_name
        current_players.append(player_copy)

# --- 4. Funzione di Disegno Dinamica ---
def draw_dynamic_field(players, dimensions, fill_c, gk_fill_c, border_c, field_c):
    field_w, field_l = dimensions
    
    fig, ax = plt.subplots(figsize=(8, 10)) # Aspect ratio generico
    
    # Sfondo
    fig.patch.set_facecolor(field_c)
    ax.set_facecolor(field_c)
    ax.set_aspect('equal')

    line_c = "white"
    lw = 2
    
    # 1. Perimetro Campo
    ax.add_patch(patches.Rectangle((0, 0), field_w, field_l, edgecolor=line_c, facecolor='none', linewidth=lw))
    
    # 2. Linea di metà campo (Dinamica!)
    half_l = field_l / 2
    ax.plot([0, field_w], [half_l, half_l], color=line_c, linewidth=lw)
    
    # 3. Cerchio di centrocampo
    # Raggio proporzionale: 9.15m è standard su 11v11 (circa 13% della larghezza)
    # Per semplicità usiamo il raggio standard se il campo è grande, ridotto se piccolo
    radius = 9.15 if field_w > 50 else 3.0 # 3m per calcetto
    ax.add_patch(patches.Circle((field_w/2, half_l), radius, edgecolor=line_c, facecolor='none', linewidth=lw))
    ax.add_patch(patches.Circle((field_w/2, half_l), 0.3, color=line_c)) 

    # 4. Aree di rigore (Solo lato basso per tattica offensiva/difensiva singola)
    # Dimensioni standard area: 40.32 x 16.5
    # Adattiamo per campi piccoli
    if field_w > 50: # 9v9 e 11v11 (Standard)
        box_w, box_h = 40.32, 16.5
        small_box_w, small_box_h = 18.32, 5.5
        penalty_spot = 11
    else: # 5v5 e 7v7 (Ridotte)
        box_w = field_w * 0.7
        box_h = field_l * 0.25 # Area profonda il 25% del campo
        small_box_w, small_box_h = 0, 0 # Calcetto spesso non ha area piccola
        penalty_spot = 6 # 6 metri calcetto
        
    # Disegno Area Grande
    ax.add_patch(patches.Rectangle(((field_w - box_w)/2, 0), box_w, box_h, edgecolor=line_c, facecolor='none', linewidth=lw))
    
    # Disegno Area Piccola (se esiste)
    if small_box_w > 0:
        ax.add_patch(patches.Rectangle(((field_w - small_box_w)/2, 0), small_box_w, small_box_h, edgecolor=line_c, facecolor='none', linewidth=1.5))

    # Dischetto
    ax.scatter(field_w/2, penalty_spot, color=line_c, s=15)

    # Porta
    goal_w = 7.32 if field_w > 50 else 3.0 # Porta calcetto 3m
    ax.add_patch(patches.Rectangle(((field_w - goal_w)/2, -1.5), goal_w, 1.5, edgecolor=line_c, facecolor='none', linewidth=2, alpha=0.7))

    # 5. Giocatori
    for p in players:
        # p['pos'] sono coordinate assolute basate sulla dimensione specifica del campo
        x, y = p['pos']
        
        if p['role'] == 'P':
            current_color = gk_fill_c
        else:
            current_color = fill_c
            
        # Dimensione pallino: più piccolo se il campo è enorme (11v11), più grande se calcetto
        dot_size = 600 if field_w > 50 else 800
        
        ax.scatter(x, y, s=dot_size, color=current_color, edgecolor=border_c, linewidth=2.5, zorder=10)
        
        ax.text(x, y - (field_l*0.04), p['name'], color='white', ha='center', va='top', 
                fontweight='bold', fontsize=9, zorder=11,
                bbox=dict(facecolor='black', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.2'))

    # Limiti visuale con un po' di margine
    ax.set_xlim(-2, field_w + 2)
    ax.set_ylim(-2, field_l + 2)
    ax.axis('off')
    
    return fig

# --- 5. Visualizzazione ---
field_fig = draw_dynamic_field(current_players, current_dims, c1_fill, c_gk_fill, c2_border, f_color)

st.pyplot(field_fig)

# --- 6. Download ---
fn = f"tattica_{game_type}_{chosen_f_name}.png"
img = io.BytesIO()
field_fig.savefig(img, format='png', bbox_inches='tight', facecolor=f_color)

st.download_button(
    label="📷 Scarica Immagine",
    data=img,
    file_name=fn,
    mime="image/png"
)
