
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

st.set_page_config(layout="centered")
st.title("Guía de Diseño - Piso Garage")

# 1. Unidad de medida y entradas
unidad = st.selectbox("Selecciona la unidad de medida", ["metros", "centímetros"], key="unidad")
factor = 1 if unidad == "metros" else 0.01
min_val = 1.0 if unidad == "metros" else 10.0

ancho_input = st.number_input(f"Ancho del espacio ({unidad})", min_value=min_val, value=4.0 if unidad=="metros" else 400.0, step=1.0, key="ancho")
largo_input = st.number_input(f"Largo del espacio ({unidad})", min_value=min_val, value=6.0 if unidad=="metros" else 600.0, step=1.0, key="largo")

ancho_m = ancho_input * factor
largo_m = largo_input * factor
area_m2 = round(ancho_m * largo_m, 2)
st.markdown(f"**Área total:** {area_m2} m²")

# 2. Bordillos y esquineros
incluir_bordillos = st.checkbox("Agregar bordillos", value=True)
incluir_esquineros = st.checkbox("Agregar esquineros", value=True)
pos_bord = st.multiselect("¿Dónde colocar bordillos?", ["Arriba","Abajo","Izquierda","Derecha"], default=["Arriba","Abajo","Izquierda","Derecha"])

# 3. Colores y base
colores = {
    "Blanco":"#FFFFFF","Negro":"#000000","Gris":"#B0B0B0","Gris Oscuro":"#4F4F4F",
    "Azul":"#0070C0","Celeste":"#00B0F0","Amarillo":"#FFFF00","Verde":"#00B050","Rojo":"#FF0000"
}
lista_colores = list(colores.keys())
color_base = st.selectbox("Color base", lista_colores, index=lista_colores.index("Blanco"))
# Inicializar grid en session_state
if 'df' not in st.session_state or 'shape' not in st.session_state:
    cols = math.ceil(ancho_m / 0.4)
    rows = math.ceil(largo_m / 0.4)
    st.session_state.df = pd.DataFrame([[color_base]*cols for _ in range(rows)])
    st.session_state.shape = (rows, cols)
else:
    cols = math.ceil(ancho_m / 0.4)
    rows = math.ceil(largo_m / 0.4)
    if st.session_state.shape != (rows, cols):
        st.session_state.df = pd.DataFrame([[color_base]*cols for _ in range(rows)])
        st.session_state.shape = (rows, cols)

df = st.session_state.df

# Aplicar color base
if st.button("Aplicar color base"):
    df = pd.DataFrame([[color_base]*cols for _ in range(rows)])
    st.session_state.df = df

# 4. Editor manual
st.subheader("Diseño personalizado")
edited = st.data_editor(
    df,
    num_rows="fixed",
    use_container_width=True,
    key="editor",
    column_config={
        col: st.column_config.SelectboxColumn(options=lista_colores)
        for col in df.columns
    }
)
st.session_state.df = edited

# 5. Renderizar vista gráfica
fig, ax = plt.subplots(figsize=(cols/2, rows/2))
for y in range(rows):
    for x in range(cols):
        color = colores.get(edited.iat[y, x], "#FFFFFF")
        ax.add_patch(plt.Rectangle((x, rows-1-y), 1, 1, facecolor=color, edgecolor="black"))

# Bordillos delgados
if incluir_bordillos:
    if "Arriba" in pos_bord:
        ax.add_patch(plt.Rectangle((0, rows), cols, 0.15, facecolor="black"))
    if "Abajo" in pos_bord:
        ax.add_patch(plt.Rectangle((0, -0.15), cols, 0.15, facecolor="black"))
    if "Izquierda" in pos_bord:
        ax.add_patch(plt.Rectangle((-0.15, 0), 0.15, rows, facecolor="black"))
    if "Derecha" in pos_bord:
        ax.add_patch(plt.Rectangle((cols, 0), 0.15, rows, facecolor="black"))

# Esquineros
if incluir_esquineros:
    s = 0.15
    for (x, y) in [(0,0),(0,rows),(cols,0),(cols,rows)]:
        ax.add_patch(plt.Rectangle((x-s/2, y-s/2), s, s, facecolor="black"))

ax.set_xlim(-0.5, cols+0.5)
ax.set_ylim(-0.5, rows+0.5)
ax.set_aspect('equal')
ax.axis('off')
st.pyplot(fig)
