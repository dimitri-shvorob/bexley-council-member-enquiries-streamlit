from pathlib import Path

import polars as pl

PATH = Path(r"C:\Users\dimit\Documents\GitHub\bexley-council-member-enquiries-streamlit")

x = pl.read_csv(PATH / "councillors.csv")

# get num councillors per ward
g = x.group_by("ward").len().rename({"len": "n_councillors"})
x = x.join(g, on = "ward", how = "left")

y0 = pl.read_csv(PATH / "raw data" / "foi 2022-23.csv", try_parse_dates=True)
y1 = pl.read_csv(PATH / "raw data" / "foi 2024.csv", try_parse_dates=True)
y2 = pl.read_csv(PATH / "raw data" / "foi 2025.csv", try_parse_dates=True)

mapping = {
    "James, Hunt": "Hunt, James",
    "Gower MBE, Sue": "Gower, Sue",
    "O'Neill OBE, Teresa": "O'Neill, Teresa",
    "Taylor, Nicola": "Taylor N",
    "Taylor, Christopher": "Taylor C",
    "Taylor, Chris": "Taylor C",
}
# combine data for multiplke years
# clean up names
# replace dates with months
y = (
    pl.concat([y0, y1, y2], how="diagonal")
    .rename(lambda col_name: col_name.lower())
    .with_columns(
        last_name=pl.col("councillor").replace(mapping).str.split(by=",").list.get(0)
    )
    .with_columns(month=pl.col("date received").dt.truncate("1mo"))
    .drop("date received")
)

# link up ward data, add a scaling factor to address varying ward sizes (2 councillors vs 3)
z = (
     x
     .join(y, on="last_name", how="left").drop("councillor")
     .with_columns(n = pl.lit(1), n_scaled = 1/pl.col.n_councillors)
    )

z.write_parquet(PATH / "data" / "data.parquet")

