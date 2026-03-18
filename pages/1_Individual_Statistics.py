import altair as alt
import polars as pl
import streamlit as st


@st.cache_data
def load_data():
    return pl.read_parquet("data.parquet")


df = load_data()

dg = df.group_by(["last_name", "party"]).agg(pl.col("n").sum())
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
