import glob
import pandas as pd
from stats_plots import *
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import streamlit as st
import os
import sys
sys.path.append('mapa_calor_py')
from mapa_calor_py.heat_map_shots import plot_heat_map_shots

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    password = st.text_input("Enter password:", type="password")
    if password == "onepiece":  # Replace with your password
        st.session_state["authenticated"] = True
        st.rerun()
    else:
        st.stop()

# Streamlit team selection
team_options = {
    "UE Horta": "equips_primera/ue_horta.csv",
    "CBF Cerdanyola": "cerdanyola.csv",
    "CB Prat": "prat.csv",
    "Sant Just": "sant_just.csv",
    "Manresa CBF": "manresa.csv"
}
selected_team = st.sidebar.selectbox("Selecciona l'equip", list(team_options.keys()), index=0)
filename = team_options[selected_team]

# Load the CSV file for the selected team
if os.path.exists(filename):
    df = pd.read_csv(filename)
    df.columns = ["Jugadora", "Jornada","Rival","PTS","MIN","FC","FTM","FTA","2PM","2PA","3PM","3PA"]
    player_stats_sum = df.groupby("Jugadora").sum()
    player_stats_sum = player_stats_sum.drop(columns=["Jornada", "Rival"])
    player_stats_sum = player_stats_sum.sort_values(by="MIN", ascending=False)
   
    # Field goals
    player_stats_sum["FGM"] = player_stats_sum["2PM"] + player_stats_sum["3PM"]
    player_stats_sum["FGA"] = player_stats_sum["2PA"] + player_stats_sum["3PA"]

    # 2PT stats
    player_stats_sum["2P%"] = (player_stats_sum["2PM"] / player_stats_sum["2PA"]) * 100
    player_stats_sum["2P%"] = player_stats_sum["2P%"].round(1)

    # 3PT stats
    player_stats_sum["3P%"] = (player_stats_sum["3PM"] / player_stats_sum["3PA"]) * 100
    player_stats_sum["3P%"] = player_stats_sum["3P%"].round(1)
    player_stats_sum["3PAr"] = player_stats_sum["3PM"] / (player_stats_sum["2PM"] + player_stats_sum["3PM"]) * 100
    player_stats_sum["3PAr"] = player_stats_sum["3PAr"].round(1)

    player_stats_sum["FG%"] = (player_stats_sum["FGM"] / player_stats_sum["FGA"]) * 100
    player_stats_sum["FG%"] = player_stats_sum["FG%"].round(1)
    player_stats_sum["eFG%"] = (player_stats_sum['3PM'] + player_stats_sum['2PM'] + 0.5*player_stats_sum['3PM']) / (player_stats_sum['3PA'] + player_stats_sum['2PA'] ) * 100
    player_stats_sum["eFG%"] = player_stats_sum["eFG%"].round(1)

    # FT stats
    player_stats_sum["FT%"] = (player_stats_sum["FTM"] / player_stats_sum["FTA"]) * 100
    player_stats_sum["FT%"] = player_stats_sum["FT%"].round(1)

    player_stats_sum["Aggr"] = player_stats_sum['FTA'] / (player_stats_sum['2PA']+player_stats_sum['3PA'])
    player_stats_sum["Aggr"] = player_stats_sum["Aggr"].round(1)

    # game stats   
    games_played = df.groupby("Jugadora")["Jornada"].count()
    player_stats_sum["PARTITS"] = games_played
    
    player_stats_sum["PTS/PARTIT"] = player_stats_sum["PTS"] / games_played
    player_stats_sum["PTS/PARTIT"] = player_stats_sum["PTS/PARTIT"].round(1)

    player_stats_sum["MIN/PARTIT"] = player_stats_sum["MIN"] / games_played
    player_stats_sum["MIN/PARTIT"] = player_stats_sum["MIN/PARTIT"].round(1)

    player_stats_sum["2PA/PARTIT"] = player_stats_sum["2PA"] / games_played
    player_stats_sum["2PA/PARTIT"] = player_stats_sum["2PA/PARTIT"].round(1)
    player_stats_sum["2PM/PARTIT"] = player_stats_sum["2PM"] / games_played
    player_stats_sum["2PM/PARTIT"] = player_stats_sum["2PM/PARTIT"].round(1)

    player_stats_sum["3PA/PARTIT"] = player_stats_sum["3PA"] / games_played
    player_stats_sum["3PA/PARTIT"] = player_stats_sum["3PA/PARTIT"].round(1)
    player_stats_sum["3PM/PARTIT"] = player_stats_sum["3PM"] / games_played
    player_stats_sum["3PM/PARTIT"] = player_stats_sum["3PM/PARTIT"].round(1)

    player_stats_sum["FTA/PARTIT"] = player_stats_sum["FTA"] / games_played
    player_stats_sum["FTA/PARTIT"] = player_stats_sum["FTA/PARTIT"].round(1)
    player_stats_sum["FTM/PARTIT"] = player_stats_sum["FTM"] / games_played
    player_stats_sum["FTM/PARTIT"] = player_stats_sum["FTM/PARTIT"].round(1)

    # Minutes stats
    player_stats_sum["PTS/40MIN"] = player_stats_sum["PTS"] / player_stats_sum["MIN"]*40
    player_stats_sum["PTS/40MIN"] = player_stats_sum["PTS/40MIN"].round(1)

    player_stats_sum["2PA/40MIN"] = player_stats_sum["2PA"] / player_stats_sum["MIN"]*40
    player_stats_sum["2PA/40MIN"] = player_stats_sum["2PA/40MIN"].round(1)
    player_stats_sum["2PM/40MIN"] = player_stats_sum["2PM"] / player_stats_sum["MIN"]*40
    player_stats_sum["2PM/40MIN"] = player_stats_sum["2PM/40MIN"].round(1)

    player_stats_sum["3PA/40MIN"] = player_stats_sum["3PA"] / player_stats_sum["MIN"]*40
    player_stats_sum["3PA/40MIN"] = player_stats_sum["3PA/40MIN"].round(1)
    player_stats_sum["3PM/40MIN"] = player_stats_sum["3PM"] / player_stats_sum["MIN"]*40
    player_stats_sum["3PM/40MIN"] = player_stats_sum["3PM/40MIN"].round(1)

    player_stats_sum["FTA/40MIN"] = player_stats_sum["FTA"] / player_stats_sum["MIN"]*40
    player_stats_sum["FTA/40MIN"] = player_stats_sum["FTA/40MIN"].round(1)
    player_stats_sum["FTM/40MIN"] = player_stats_sum["FTM"] / player_stats_sum["MIN"]*40
    player_stats_sum["FTM/40MIN"] = player_stats_sum["FTM/40MIN"].round(1)
    
   

else:
    st.error(f"No s'ha trobat l'arxiu per l'equip {selected_team}: {filename}")
    st.stop()

####### Streamlit app ########


# Sidebar navigation
st.sidebar.title("Navegació")
section = st.sidebar.radio("Selecciona una secció", ["Gràfic de dispersió", "Taula de valors","Mapa de calor"])

if section == "Gràfic de dispersió":
    st.header("Gràfic de dispersió")
    st.markdown("""
**Comparatives recomanades:**

| eix X         | eix Y      | Descripció                                                                 |
|---------------|------------|----------------------------------------------------------------------------|
| 2PA           | 2P%        | % de 2 comparat amb els intentats                               |
| 3PA           | 3P%        | % de 3 comparat amb els intentats                               |
| FGA           | eFG%       | % efectiu de tirs de camp comparat amb els intentats                    |
| 3PA           | 3PAr       | Ús del tir de 3 respecte els tirs de 3 intentats. Detecta tiradores de 3   |
| FGA           | Aggr       | Evalúa agressivitat a cistella (Aggr) segons els tirs de camp intentats    |
| MIN           | stat/40MIN | Ús del paràmetre seleccionat per minut segons el total de minuts           |
| MIN/PARTIT    | stat/PARTIT| Ús del paràmetre seleccionat per partit segons els minuts per partit       |

Aquestes són les recomanades, a partir d'aqui es pot provar qualsevol combinació de paràmetres que ens interessi.
""")

    numeric_columns = player_stats_sum.select_dtypes(include='number').columns.tolist()
    x_col = st.selectbox("Selecciona dades eix X", numeric_columns, index=numeric_columns.index("MIN") if "MIN" in numeric_columns else 0)
    y_col = st.selectbox("Selecciona dades eix Y", numeric_columns, index=numeric_columns.index("3PM") if "3PM" in numeric_columns else 1)
    fig = plot_scatter_players(
        player_stats_sum.index.tolist(),
        player_stats_sum[x_col],
        player_stats_sum[y_col],
        x_col,
        y_col,
        f"{y_col} vs {x_col} per Jugadora",
        "dodgerblue"
    )
    st.pyplot(fig)

    st.markdown("""
**Glossari:**
- PARTITS - Nombre de partits jugats              
- PTS - Points (Punts totals)
- MIN - Minutes played (Minuts jugats)
- FC - Faltas comeses (Personal fouls)
- FTM - Free Throws Made (Llançaments lliures encistellats)
- FTA - Free Throws Attempted (Llançaments lliures intentats)
- 3PM - 3PT Made (Triple encistellat)
- 3PA - 3PT Attempted (Triple intentat)
- 2PM - 2PT Made (Tir de dos encistellat)
- 2PA - 2PT Attempted (Tir de dos intentat)
- 2P% - 2PT Percentage (Percentatge d'encert en tirs de dos)
- 3P% - 3PT Percentage (Percentatge d'encert en triples) 
- stat/PARTIT - Estadístiques per partit
- stat/40MIN - Estadístiques per minut ajustades a 40 minuts
- 3PAr - 3PT rate (Percentatge de triples sobre tirs de camp totals )
- FG% - Field goal percentage (Percentatge d'encert en tirs de camp)
- eFG% - Effective FG% (Percentatge d'encert efectiu en tirs de camp, dóna més valor als triples)
- FT% - Free throw percentage (Percentatge d'encert en llançaments lliures)
- Aggr - Aggressivitat (Tirs lliures per tirs de camp intentat)
""")

elif section == "Taula de valors":
    st.header("Taula de valors")
    df_plot = player_stats_sum.reset_index()
    # Reorder columns
    cols_table = ["Jugadora","PARTITS", "PTS", "MIN", "PTS/PARTIT", "MIN/PARTIT","2PM","2PA","2P%","3PM","3PA","3P%","3PAr","FTM","FTA","FT%"]
    df_plot = df_plot[cols_table]
    df_plot = df_plot.fillna(0)
    fig, ax = plt.subplots(figsize=(12, len(df_plot)*0.5))
    ax.axis('tight')
    ax.axis('off')
    numeric_cols = df_plot.select_dtypes(include=[np.number]).columns
    cell_colors = []
    for i, row in df_plot.iterrows():
        cell_row = []
        for col in df_plot.columns:
            if col in numeric_cols:
                col_min = df_plot[col].min()
                col_max = df_plot[col].max()
                norm = mcolors.Normalize(vmin=col_min, vmax=col_max)
                cmap = plt.cm.RdYlGn_r
                color = cmap(norm(row[col]))
            else:
                color = (1,1,1,1)
            cell_row.append(color)
        cell_colors.append(cell_row)

    table = ax.table(cellText=df_plot.values,
                     colLabels=df_plot.columns,
                     cellColours=cell_colors,
                     cellLoc='center',
                     loc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(24)
    table.scale(1,8)
    # Set first column width larger
    first_col = 0
    for key, cell in table.get_celld().items():
        if key[1] == first_col:
            cell.set_width(0.35)  # Increase width (default is ~0.1)
        else:
            cell.set_width(0.25)
    st.pyplot(fig)

elif section == "Mapa de calor":
    st.header("Mapa de calor")
    jugadora_mapa = st.selectbox(
        "Selecciona jugadora",
        player_stats_sum.index.tolist()
    )  

    heatmap_folder = "equips_primera/"+selected_team.lower().replace(" ","_") + "_mapa_calor"
    txt_files = glob.glob(f"{heatmap_folder}/*.txt")
    txt_files = sorted(txt_files)
    file_options = {os.path.basename(f): f for f in txt_files}
    selected_file = jugadora_mapa.lower().replace(" ","_") + ".txt" 
    mapa_calor = 1
    mapfig = plot_heat_map_shots(file_options[selected_file], mapa_calor)
    st.pyplot(mapfig)
