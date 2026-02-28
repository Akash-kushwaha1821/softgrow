import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Covid Dashboard", layout="wide")
st.title("India Covid-19 Analysis Dashboard")

@st.cache_data
def load():
    d = pd.read_csv(r"C:\Users\lenovo\OneDrive\Desktop\softgrow_tech\covid_19_india dataset.csv")
    d["Date"] = pd.to_datetime(d["Date"], dayfirst=True)
    d = d.drop(["Sno","Time","ConfirmedIndianNational","ConfirmedForeignNational"], axis=1)
    return d

df = load()

states = st.sidebar.multiselect(
    "Select State",
    df["State/UnionTerritory"].unique(),
    default=df["State/UnionTerritory"].unique()
)

df = df[df["State/UnionTerritory"].isin(states)]
latest = df[df["Date"] == df["Date"].max()]

c1, c2, c3 = st.columns(3)
c1.metric("Confirmed", int(latest["Confirmed"].sum()))
c2.metric("Recovered", int(latest["Cured"].sum()))
c3.metric("Deaths", int(latest["Deaths"].sum()))

st.subheader("Cases Trend")
daily = df.groupby("Date")[["Confirmed","Cured","Deaths"]].sum().reset_index()

fig, ax = plt.subplots(figsize=(10,5))
sns.lineplot(data=daily, x="Date", y="Confirmed", ax=ax)
sns.lineplot(data=daily, x="Date", y="Cured", ax=ax)
sns.lineplot(data=daily, x="Date", y="Deaths", ax=ax)
st.pyplot(fig)

st.subheader("Top States by Cases")
top = latest.sort_values("Confirmed", ascending=False).head(10)
fig2, ax2 = plt.subplots(figsize=(10,5))
sns.barplot(data=top, x="Confirmed", y="State/UnionTerritory", ax=ax2)
st.pyplot(fig2)

st.subheader("India Map Visualization")

state_map = latest.groupby("State/UnionTerritory")[["Confirmed"]].sum().reset_index()
state_map.columns = ["State","Cases"]

fig_map = px.choropleth(
    state_map,
    geojson="https://raw.githubusercontent.com/geohacker/india/master/state/india_telengana.geojson",
    featureidkey="properties.NAME_1",
    locations="State",
    color="Cases",
    color_continuous_scale="Reds"
)

fig_map.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig_map, use_container_width=True)

st.subheader("Correlation Heatmap")
corr = df[["Confirmed","Cured","Deaths"]].corr()
fig3, ax3 = plt.subplots(figsize=(6,4))
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax3)
st.pyplot(fig3)

if st.checkbox("Show Raw Data"):
    st.dataframe(df)