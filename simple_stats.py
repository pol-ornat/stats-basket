import pandas as pd
from stats_plots import *
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import streamlit as st
import os

# Streamlit team selection
team_options = {
    "UE Horta": "ue_horta.csv",
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
    df.columns = ["Jugadora", "Jornada","Rival","PTS","MIN","FC","FTM","FTA","2PM","3PM"]
    player_stats_sum = df.groupby("Jugadora").sum()
    player_stats_sum = player_stats_sum.drop(columns=["Jornada", "Rival"])
    player_stats_sum = player_stats_sum.sort_values(by="MIN", ascending=False)
    player_stats_sum["3PAr"] = player_stats_sum["3PM"] / (player_stats_sum["2PM"] + player_stats_sum["3PM"]) * 100
    player_stats_sum["3PAr"] = player_stats_sum["3PAr"].round(1)
    player_stats_sum["PTS/40MIN"] = player_stats_sum["PTS"] / player_stats_sum["MIN"]*40
    player_stats_sum["PTS/40MIN"] = player_stats_sum["PTS/40MIN"].round(1)
    games_played = df.groupby("Jugadora")["Jornada"].count()
    player_stats_sum["PARTITS"] = games_played
    player_stats_sum["PTS/PARTIT"] = player_stats_sum["PTS"] / games_played
    player_stats_sum["PTS/PARTIT"] = player_stats_sum["PTS/PARTIT"].round(1)
    player_stats_sum["MIN/PARTIT"] = player_stats_sum["MIN"] / games_played
    player_stats_sum["MIN/PARTIT"] = player_stats_sum["MIN/PARTIT"].round(1)

else:
    st.error(f"No s'ha trobat l'arxiu per l'equip {selected_team}: {filename}")
    st.stop()

####### Streamlit app ########


# Sidebar navigation
st.sidebar.title("Navegació")
section = st.sidebar.radio("Selecciona una secció", ["Gràfic de dispersió", "Taula de valors"])

if section == "Gràfic de dispersió":
    st.header("Gràfic de dispersió")
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

elif section == "Taula de valors":
    st.header("Taula de valors")
    df_plot = player_stats_sum.reset_index()
    # Reorder columns
    first_cols = ["Jugadora","PARTITS", "PTS", "MIN", "PTS/PARTIT", "MIN/PARTIT","PTS/40MIN"]
    other_cols = [col for col in df_plot.columns if col not in first_cols]
    df_plot = df_plot[first_cols + other_cols]
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