from fx_api import FX

FX_df = FX(source_currency=['GBP','USD','EUR']).get_FX_date_range(start_at="2019-01-01", end_at="2020-01-01")

print(FX_df.head(5))