import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

df = pd.read_csv('titanic.csv')
df = df.dropna()
df['age_group'] = pd.cut(df['Age'], bins=[0, 18, 30, 50, 100], labels=['<18', '18-30', '30-50', '50+'])
df['fare_group'] = pd.cut(df['Fare'], bins=[0, 10, 20, 30, 1000], labels=['<10', '10-20', '20-30', '30+'])


# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
gender = st.sidebar.multiselect(
    "Select the gender:",
    options=df["Sex"].unique(),
    default=df["Sex"].unique()
)

pclass = st.sidebar.multiselect(
    "Select the pclass:",
    options=df["Pclass"].unique(),
    default=df["Pclass"].unique(),
)

embarked = st.sidebar.multiselect(
    "Select the Embarked:",
    options=df["Embarked"].unique(),
    default=df["Embarked"].unique()
)

df_selection = df.query(
    "Sex == @gender & Pclass ==@pclass & Embarked == @embarked"
)
total_sales = int(df_selection["Survived"].sum())
average_rating = int(df_selection["PassengerId"].count())

average_sale_by_transaction =(df_selection["Fare"].max())

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Survived:")
    st.subheader(f"{total_sales:,}")
with middle_column:
    st.subheader("Total Passengers:")
    st.subheader(f"{average_rating}")
with right_column:
    st.subheader("Max Fare:")
    st.subheader(f"{average_sale_by_transaction}")

st.markdown("""---""")



survival_rate = (
     df_selection.groupby(by=["Sex"]).sum()[["Survived"]].sort_values(by="Survived")
)
age_groups = (
    df_selection.groupby(by=["age_group"]).count()
)

correlation = (
    df[['Pclass', 'Survived', 'Age', 'Fare']].corr()
)

fig_product_sales = px.bar(
    survival_rate,
    x="Survived",
    y=survival_rate.index,
    orientation="h",
    title="<b>Total Survived</b>",
    color_discrete_sequence=["#0083B8"] * len(survival_rate),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
st.plotly_chart(fig_product_sales)
fig_1 = px.bar(
    age_groups,
    x="PassengerId",
    y=age_groups.index,
    orientation="h",
    title="<b>People Age Group wise</b>",
    color_discrete_sequence=["#0083B8"] * len(survival_rate),
    template="plotly_white",
)
fig_1.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
st.plotly_chart(fig_1)
fig_2 = px.imshow(
    correlation,
    
    title="<b>Coorelation</b>",
    
)
fig_2.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
st.plotly_chart(fig_2)
