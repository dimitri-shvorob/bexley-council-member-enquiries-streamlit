import altair as alt
import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    return pd.read_parquet(
        r"C:\Users\dimit\Documents\GitHub\bexley-member-enquiries-streamlit\data\data.parquet"
    )


df = load_data()

dg = df.groupby(["last_name", "party"])["n"].sum()
bars = (
    alt.Chart(dg)
    .mark_bar()
    .encode(
        x=alt.X("n", axis=alt.Axis(title=None)),
        y=alt.Y(
            "last_name",
            sort=alt.EncodingSortField(field="n", order="descending"),
            axis=alt.Axis(title=None),
        ),
        color="party",
    )
)
labels = (
    alt.Chart(dg)
    .mark_text(align="left", baseline="middle", dx=5)  # moves text slightly above bars
    .encode(
        x="n",
        y=alt.Y(
            "last_name",
            sort=alt.EncodingSortField(field="n", order="descending"),
            axis=alt.Axis(title=None),
        ),
        text="n",
    )
)
ch = bars + labels

st.altair_chart(ch, use_container_width=True)

st.write("Cllr Fosten (Belvedere Ward) elected in October 2024")
