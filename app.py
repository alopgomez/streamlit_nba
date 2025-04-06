import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("./nba_all_elo.csv")

years = df["year_id"].unique().tolist()
teams = df["team_id"].unique().tolist()

with st.sidebar:
    st.write("Seleccionar un año y equipo:")

    # caja de seleccion para el año
    year = st.selectbox('Año', years, 0)

    # caja de seleccion para el equipo
    team = st.selectbox('Equipo', teams, 0)

    playoff = st.pills("Temporada Regular, Playoffs o Ambos:", ["Regular", "Playoffs"],
                       selection_mode="multi", default=["Regular", "Playoffs"])

# filtro para año y equipo
reg = 1 if "Regular" in playoff else 0
play = 1 if "Playoffs" in playoff else 0

if reg and play:
    filter_year_team = (df["year_id"] == year) & (df["team_id"] == team)
elif reg:
    filter_year_team = (df["year_id"] == year) & (df["team_id"] == team) & (~df["is_playoffs"])
elif play:
    filter_year_team = (df["year_id"] == year) & (df["team_id"] == team) & (df["is_playoffs"])
else:
    filter_year_team = [False]*len(df.index)


with st.container():
    df_year_team = df[filter_year_team]
    
    if len(df_year_team.index):

        w = df_year_team.replace({"game_result":{'W':1, 'L':0}})
        l = df_year_team.replace({"game_result":{'W':0, 'L':1}})
        
        w = w["game_result"].cumsum()
        l = l["game_result"].cumsum()

        df_year_team["date_game"] = pd.to_datetime(df_year_team["date_game"], format="%m/%d/%Y")

        dfw = pd.DataFrame({"Fecha":df_year_team["date_game"], "W":w, "L":l})
        # dfl = pd.DataFrame({"Fecha":df["date_game"], "l":l})


        col1, col2 = st.columns(2)
        with col1:
            st.line_chart(dfw, x="Fecha", y=["W","L"], color=["#0343DF","#FC5A50"])
        
        with col2:
            pw = w.iloc[-1] / (w.iloc[-1]+l.iloc[-1]) * 100
            pl = l.iloc[-1] / (w.iloc[-1]+l.iloc[-1]) * 100

            fig, ax = plt.subplots()

            explode = (0.1, 0)
            ax.pie([pw,pl], explode=explode, labels=["W","L"], autopct='%1.1f%%',
                    shadow=True, startangle=90)
            ax.axis('equal')
            st.pyplot(fig)
    else:
        st.write("No hay datos para este año y equipo")
