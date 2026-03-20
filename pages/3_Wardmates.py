import altair as alt
import polars as pl
import streamlit as st


@st.cache_data
def load_data():
    df = pl.read_parquet(
        r"data.parquet"
    )
    return (
        df.group_by("ward", "last_name")
        .agg(pl.col("n").sum())
        .with_columns(
            f=pl.col("n") / pl.col("n").sum().over("ward"),
            rank=pl.col("n").rank().over("ward"),
            minv=1 / pl.count().over("ward"),
        )
    )


df = load_data()

# normalized herfindahl index
df = (
    df.with_columns(hhi=pl.col("f").pow(2).sum().over("ward"))
    .with_columns(hhin=(pl.col("hhi") - pl.col("minv")) / (1 - pl.col("minv")))
    .with_columns(hhin_rank=pl.col("hhin").rank(method="min"))
)

bars = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X(
            "ward:N",
            sort=alt.SortField(field="hhin_rank", order="ascending"),
            title=None,
        ),
        y=alt.Y("f:Q", title=None),
        color=alt.Color("rank:N", scale=alt.Scale(scheme="greens"), legend=None),
    )
)

labels = (
    alt.Chart(df)
    .mark_text(dy=0, color="black")  # vertical offset
    .encode(
        x=alt.X("ward:N", sort=alt.SortField(field="hhin_rank", order="ascending")),
        y=alt.Y("f:Q", stack="zero"),
        text="last_name:N",
    )
)


ch1 = bars + labels

st.title("Split of iCasework cases between ward's councillors")

st.write("Wards sorted from the most 'equal' split to the most 'unequal' split")
st.write("(Normalized Herfindahl-Hirschman index used as measure of inequality).")

st.altair_chart(ch1)

st.dataframe(df.sort(["hhin", "rank"]).drop("rank", "minv", "hhi", "hhin_rank"))

st.write("Note: Cllr Fosten (Belvedere Ward) elected in October 2024.")
