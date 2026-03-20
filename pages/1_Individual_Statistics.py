import altair as alt
import polars as pl
import streamlit as st


@st.cache_data
def load_data():
    df = pl.read_parquet(
        r"data.parquet"
    )
    return df.group_by(["last_name", "party"]).agg(pl.col("n").sum())


df = load_data()

bars = (
    alt.Chart(df)
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
    alt.Chart(df)
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

st.title("Statistics for individual councillors")

st.altair_chart(ch, use_container_width=True)

st.dataframe(df.sort(["n"], reverse = True))

st.write("Note: Cllr Fosten (Belvedere Ward) elected in October 2024")
