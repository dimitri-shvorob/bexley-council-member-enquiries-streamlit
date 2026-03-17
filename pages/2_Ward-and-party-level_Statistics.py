import altair as alt
import pandas as pd
import streamlit as st


@st.cache_data
def load_ward_level_data():
    df = pd.read_parquet(
        r"C:\Users\dimit\Documents\GitHub\bexley-member-enquiries-streamlit\data\data.parquet"
    )
    df["ward_party"] = df["ward"] + " | " + df["party"]
    return df


df = load_ward_level_data()

# n
dw1 = df.groupby(["ward_party", "party"])["n"].sum()
bars = (
    alt.Chart(dw1, title="Total")
    .mark_bar()
    .encode(
        x=alt.X("n", axis=alt.Axis(title=None)),
        y=alt.Y(
            "ward_party",
            sort=alt.EncodingSortField(field="n", order="descending"),
            axis=alt.Axis(title=None),
        ),
        color=alt.Color("party"),
    )
)
labels = (
    alt.Chart(dw1)
    .mark_text(align="left", baseline="middle", dx=5)  # moves text slightly above bars
    .encode(
        x="n",
        y=alt.Y(
            "ward_party",
            sort=alt.EncodingSortField(field="n", order="descending"),
            axis=alt.Axis(title=None),
        ),
        text="n",
    )
)
ch1 = bars + labels

# n - per councillor
dw2 = df.groupby(["ward_party", "party"])["n"].sum()
bars = (
    alt.Chart(dw2, title="Average (per councillor)")
    .mark_bar()
    .encode(
        x=alt.X("n_scaled", axis=alt.Axis(title=None)),
        y=alt.Y(
            "ward_party",
            sort=alt.EncodingSortField(field="n_scaled", order="descending"),
            axis=alt.Axis(title=None),
        ),
        color=alt.Color("party", legend=None),
    )
)
labels = (
    alt.Chart(dw2)
    .mark_text(align="left", baseline="middle", dx=5)  # moves text slightly above bars
    .encode(
        x="n_scaled",
        y=alt.Y(
            "ward_party",
            sort=alt.EncodingSortField(field="n_scaled", order="descending"),
            axis=alt.Axis(title=None),
        ),
        text=alt.Text("n_scaled", format=".1f"),
    )
)
ch2 = bars + labels

st.altair_chart(ch1, use_container_width=True)
st.altair_chart(ch2, use_container_width=True)

st.write("Cllr Fosten (Belvedere Ward) elected in October 2024")
