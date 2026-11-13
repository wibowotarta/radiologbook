# === Stage 5: Фильтрация записей ===
# Project: RadioLogbook
def filter_by_band(records, band):
    return [rec for rec in records if rec.get("band") == band]


def filter_by_date_range(records, start_date, end_date):
    return [
        rec
        for rec in records
        if start_date <= rec.get("date") <= end_date
    ]


def filter_records(records, band=None, start_date=None, end_date=None):
    result = records
    if band is not None:
        result = filter_by_band(result, band)
    if start_date is not None:
        result = filter_by_date_range(result, start_date, end_date)
    return result
