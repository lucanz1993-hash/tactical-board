import streamlit as st
st.set_page_config(page_title="Tactical Board", page_icon="⚽", layout="centered")
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- 1. Configurazione Pagina ---
st.set_page_config(page_title="Tactical Board", layout="centered")

# --- 2. Dimensioni Campo ---
field_length = 105
field_width = 68

# --- 3. Dati Formazioni ---
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
      {'name': 'ATT', 'role': 'F', 'position':(field_width *0.5, 48)},
  ],
  '3-3-2': [
      {'name': 'POR', 'role': 'P', 'position':(field_width /2, 5)},
      {'name': 'TS', 'role': 'D', 'position':(field_width *0.2, 20)},
      {'name': 'DC', 'role': 'D', 'position':(field_width *0.5, 17)},
      {'name': 'TD', 'role': 'D', 'position':(field_width *0.8, 17)},
      {'name': 'CS', 'role': 'C', 'position':(field_width *0.2, 35)},
      {'name': 'CC', 'role': 'C', 'position':(field_width *0.5, 30)},
      {'name': 'CD', 'role': 'C', 'position':(field_width *0.8, 35)},
      {'name': 'ATS', 'role': 'F', 'position':(field_width *0.4, 48)},
      {'name': 'ATD', 'role': 'F', 'position':(field_width *0.6, 48)},
  ],
  '4-3-1': [
      {'name': 'POR', 'role': 'P', 'position':(field_width /2, 5)},
      {'name': 'TS', 'role': 'D', 'position':(field_width *0.2, 20)},
      {'name': 'DCS', 'role': 'D', 'position':(field_width *0.4, 17)},
      {'name': 'DCD', 'role': 'D', 'position':(field_width *0.6, 17)},
      {'name': 'TD', 'role': 'D', 'position':(field_width *0.8, 20)},
      {'name': 'CS', 'role': 'C', 'position':(field_width *0.2, 35)},
      {'name': 'CC', 'role': 'C', 'position':(field_width *0.5, 30)},
      {'name': 'CD', 'role': 'C', 'position':(field_width *0.8, 35)},
      {'name': 'ATT', 'role': 'F', 'position':(field_width *0.5, 48)},
  ],
  '3-3-1-1': [
      {'name': 'POR', 'role': 'P', 'position':(field_width /2, 5)},
      {'name': 'TS', 'role': 'D', 'position':(field_width *0.2, 20)},
      {'name': 'DC', 'role': 'D', 'position':(field_width *0.5, 17)},
      {'name': 'TD', 'role': 'D', 'position':(field_width *0.8, 17)},
      {'name': 'CS', 'role': 'C', 'position':(field_width *0.2, 32)},
      {'name': 'CC', 'role': 'C', 'position':(field_width *0.5, 27)},
      {'name': 'CD', 'role': 'C', 'position':(field_width *0.8, 32)},
      {'name': 'COC', 'role': 'C', 'position':(field_width *0.5, 38)},
      {'name': 'ATD', 'role': 'F', 'position':(field_width *0.6, 48)},
  ]
}

# --- 4. Sidebar ---
st.title("⚽ Tactical Board")

with st.sidebar:
    st.header("Impostazioni")
    chosen_f = st.selectbox("Formazione:", list(formations_data.keys()))
    
    st.subheader("Colori Pedine")
    c1_fill = st.color_picker("Colore 1 (Riempimento)", "#FF0000")
    c2_border = st.color_picker("Colore 2 (Bordo)", "#FFFFFF")
    
    st.subheader("Colore Campo")
    f_color = st.color_picker("Sfondo Campo", "#2E8B57")
    
    st.divider()
    st.subheader("Nomi Giocatori")
    current_players = []
    for i, p in enumerate(formations_data[chosen_f]):
        new_name = st.text_input(f"{p['name']} ({p['role']})", value=p['name'], key=f"p_{i}")
        player_copy = p.copy()
        player_copy['name'] = new_name
        current_players.append(player_copy)

# --- 5. Funzione di Disegno ---
def draw_field(players, fill_c, border_c, field_c):
    fig, ax = plt.subplots(figsize=(8, 11))
    
    # Colore sfondo campo
    fig.patch.set_facecolor(field_c)
    ax.set_facecolor(field_c)
    ax.set_aspect('equal')

    line_c = "white"
    lw = 2.5
    
    # Linee campo
    ax.add_patch(patches.Rectangle((0, 0), field_width, field_length, edgecolor=line_c, facecolor='none', linewidth=lw))
    ax.plot([0, field_width], [field_length/2, field_length/2], color=line_c, linewidth=lw)
    ax.add_patch(patches.Circle((field_width/2, field_length/2), 9.15, edgecolor=line_c, facecolor='none', linewidth=lw))
    
    # Aree
    ax.add_patch(patches.Rectangle((field_width/2 - 20.16, 0), 40.32, 16.5, edgecolor=line_c, facecolor='none', linewidth=lw))
    ax.add_patch(patches.Rectangle((field_width/2 - 20.16, field_length - 16.5), 40.32, 16.5, edgecolor=line_c, facecolor='none', linewidth=lw))

    # Pedine
    for p in players:
        x, y = p['position']
        ax.scatter(x, y, s=600, color=fill_c, edgecolor=border_c, linewidth=3.5, zorder=10)
        ax.text(x, y - 4, p['name'], color='white', ha='center', va='top', 
                fontweight='bold', fontsize=10, zorder=11,
                bbox=dict(facecolor='black', alpha=0.4, edgecolor='none', boxstyle='round,pad=0.2'))

    ax.set_xlim(-5, field_width + 5)
    ax.set_ylim(-5, field_length + 5)
    ax.axis('off')
    return fig

# --- 6. Lancio ---
field_fig = draw_field(current_players, c1_fill, c2_border, f_color)

st.pyplot(field_fig)


