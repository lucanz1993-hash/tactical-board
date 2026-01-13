import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io

# --- 1. Configurazione Pagina (MUST BE FIRST) ---
st.set_page_config(page_title="Tactical Board", page_icon="⚽", layout="centered")

# --- 2. Dimensioni Campo ---
field_length = 64
field_width = 68

# --- 3. Dati Formazioni (9 vs 9) ---
formations_data = {
    '3-4-1': [
        {'name': 'POR', 'role': 'P', 'position':(field_width /2, 5)},
        {'name': 'TS', 'role': 'D', 'position':(field_width *0.2, 20)},
        {'name': 'DC', 'role': 'D', 'position':(field_width *0.5, 17)},
        {'name': 'TD', 'role': 'D', 'position':(field_width *0.8, 17)},
        {'name': 'CCS', 'role': 'C', 'position':(field_width *0.35, 35)},
        {'name': 'CCD', 'role': 'C', 'position':(field_width *0.65, 35)},
        {'name': 'ES', 'role': 'C', 'position':(field_width *0.15, 40)},
        {'name': 'ED', 'role': 'C', 'position':(field_width *0.85, 40)},
        {'name': 'ATT', 'role': 'F', 'position':(field_width *0.5, 50)},
    ],
    '3-3-2': [
        {'name': 'POR', 'role': 'P', 'position':(field_width /2, 5)},
        {'name': 'TS', 'role': 'D', 'position':(field_width *0.2, 20)},
        {'name': 'DC', 'role': 'D', 'position':(field_width *0.5, 17)},
        {'name': 'TD', 'role': 'D', 'position':(field_width *0.8, 17)},
        {'name': 'CS', 'role': 'C', 'position':(field_width *0.2, 35)},
        {'name': 'CC', 'role': 'C', 'position':(field_width *0.5, 30)},
        {'name': 'CD', 'role': 'C', 'position':(field_width *0.8, 35)},
        {'name': 'ATS', 'role': 'F', 'position':(field_width *0.4, 50)},
        {'name': 'ATD', 'role': 'F', 'position':(field_width *0.6, 50)},
    ],
    '4-3-1': [
        {'name': 'POR', 'role': 'P', 'position':(field_width /2, 5)},
        {'name': 'TS', 'role': 'D', 'position':(field_width *0.15, 20)},
        {'name': 'DCS', 'role': 'D', 'position':(field_width *0.38, 17)},
        {'name': 'DCD', 'role': 'D', 'position':(field_width *0.62, 17)},
        {'name': 'TD', 'role': 'D', 'position':(field_width *0.85, 20)},
        {'name': 'CS', 'role': 'C', 'position':(field_width *0.25, 35)},
        {'name': 'CC', 'role': 'C', 'position':(field_width *0.5, 30)},
        {'name': 'CD', 'role': 'C', 'position':(field_width *0.75, 35)},
        {'name': 'ATT', 'role': 'F', 'position':(field_width *0.5, 50)},
    ],
    '3-3-1-1': [
        {'name': 'POR', 'role': 'P', 'position':(field_width /2, 5)},
        {'name': 'TS', 'role': 'D', 'position':(field_width *0.2, 20)},
        {'name': 'DC', 'role': 'D', 'position':(field_width *0.5, 17)},
        {'name': 'TD', 'role': 'D', 'position':(field_width *0.8, 17)},
        {'name': 'CS', 'role': 'C', 'position':(field_width *0.2, 32)},
        {'name': 'CC', 'role': 'C', 'position':(field_width *0.5, 27)},
        {'name': 'CD', 'role': 'C', 'position':(field_width *0.8, 32)},
        {'name': 'COC', 'role': 'C', 'position':(field_width *0.5, 40)},
        {'name': 'ATT', 'role': 'F', 'position':(field_width *0.5, 50)},
    ]
}

# --- 4. Sidebar ---
st.title("⚽ Lavagna Tattica (9 vs 9)")

with st.sidebar:
    st.header("Impostazioni")
    chosen_f = st.selectbox("Formazione:", list(formations_data.keys()))
    
    st.subheader("Colori Pedine")
    
    # --- MODIFICA 1: Aggiunto selettore colore portiere ---
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        c1_fill = st.color_picker("Squadra", "#D92027") 
    with col_c2:
        c_gk_fill = st.color_picker("Portiere", "#FFD700") # Giallo Oro default

    c2_border = st.color_picker("Colore Bordo", "#FFFFFF")
    
    st.subheader("Colore Campo")
    f_color = st.color_picker("Sfondo Campo", "#2E8B57")
    
    st.divider()
    st.subheader("Nomi Giocatori")
    
    current_players = []
    for i, p in enumerate(formations_data[chosen_f]):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.caption(f"**{p['role']}**")
        with col2:
            new_name = st.text_input(f"Pos. {p['name']}", value=p['name'], key=f"p_{chosen_f}_{i}", label_visibility="collapsed")
        
        player_copy = p.copy()
        player_copy['name'] = new_name
        current_players.append(player_copy)

# --- 5. Funzione di Disegno ---
# --- MODIFICA 2: Aggiunto parametro gk_fill_c alla funzione ---
def draw_field(players, fill_c, gk_fill_c, border_c, field_c):
    fig, ax = plt.subplots(figsize=(8, 11))
    
    # Background
    fig.patch.set_facecolor(field_c)
    ax.set_facecolor(field_c)
    ax.set_aspect('equal')

    line_c = "white"
    lw = 2
    
    # 1. Main Rectangle
    ax.add_patch(patches.Rectangle((0, 0), field_width, field_length, edgecolor=line_c, facecolor='none', linewidth=lw))
    
    # 2. Halfway Line
    # Nota: hai impostato field_length a 64, ma la linea di centrocampo a 105/2 (52.5). 
    # Verrà disegnata molto in alto. Se vuoi il centro geometrico del tuo campo usa field_length/2.
    # Lascio il tuo valore 105/2 come da codice originale.
    ax.plot([0, field_width], [105/2, 105/2], color=line_c, linewidth=lw)
    
    # 3. Center Circle
    ax.add_patch(patches.Circle((field_width/2, 105/2), 9.15, edgecolor=line_c, facecolor='none', linewidth=lw))
    ax.add_patch(patches.Circle((field_width/2, 105/2), 0.5, color=line_c)) # Center spot

    # 4. Penalty Areas
    # Bottom (Home)
    ax.add_patch(patches.Rectangle((field_width/2 - 20.16, 0), 40.32, 16.5, edgecolor=line_c, facecolor='none', linewidth=lw))

    # 5. Goal Areas (Small box)
    ax.add_patch(patches.Rectangle((field_width/2 - 9.16, 0), 18.32, 5.5, edgecolor=line_c, facecolor='none', linewidth=1.5))

    # 6. Penalty Spots
    ax.scatter(field_width/2, 11, color=line_c, s=15)

    # 7. Goals (Posts)
    ax.add_patch(patches.Rectangle((field_width/2 - 3.66, -2), 7.32, 2, edgecolor=line_c, facecolor='none', linewidth=2, alpha=0.7))

    # 8. Draw Players
    for p in players:
        x, y = p['position']
        
        # --- MODIFICA 3: Logica scelta colore ---
        if p['role'] == 'P':
            current_color = gk_fill_c
        else:
            current_color = fill_c
            
        # The circle (player)
        ax.scatter(x, y, s=700, color=current_color, edgecolor=border_c, linewidth=2.5, zorder=10)
        
        # The text label (Name)
        ax.text(x, y - 3.5, p['name'], color='white', ha='center', va='top', 
                fontweight='bold', fontsize=9, zorder=11,
                bbox=dict(facecolor='black', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.2'))

    ax.set_xlim(-5, field_width + 5)
    ax.set_ylim(-5, field_length + 5)
    ax.axis('off')
    
    return fig

# --- 6. Visualizzazione ---
# --- MODIFICA 4: Passiamo il nuovo colore alla funzione ---
field_fig = draw_field(current_players, c1_fill, c_gk_fill, c2_border, f_color)

st.pyplot(field_fig)

# --- 7. Download Button ---
fn = f"tattica_{chosen_f}.png"
img = io.BytesIO()
field_fig.savefig(img, format='png', bbox_inches='tight', facecolor=f_color)

st.download_button(
    label="📷 Scarica Immagine",
    data=img,
    file_name=fn,
    mime="image/png"
)
