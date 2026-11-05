# === Stage 2: Проверка полей ===
# Project: RadioLogbook
from datetime import datetime


RANGE_PATTERN = "80m/40m/20m/10m/6m/2m/1.25m/160m"
DATE_FORMAT = "%Y-%m-%d"
CALL_PATTERN = r"[A-Z0-9]{1,3}"
REPORT_PATTERN = r"\d{2}/\d{2}$"


def normalize_call(call):
    return call.strip().upper()


def normalize_range(value):
    parts = [part.strip().lower() for part in value.split(",")]
    valid = [part for part in parts if part in RANGE_PATTERN.split("/")]
    return "/".join(valid)


def normalize_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value.strip(), DATE_FORMAT).date()
    except ValueError:
        return None


def normalize_report(value):
    report = value.strip()
    if not report:
        return None
    parts = report.split("/")
    if len(parts) != 2:
        return None
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        return None


def validate_date(value):
    if not value:
        return "Дата обязательна", None
    date = normalize_date(value)
    if date is None:
        return "Неверный формат даты. Ожидается YYYY-MM-DD", None
    return None, date


def validate_range(value):
    if not value:
        return "Диапазон обязателен", None
    range_ = normalize_range(value)
    if not range_:
        return "Неверный диапазон. Используйте 160m/80m/40m/20m/10m/6m/2m/1.25m", None
    return None, range_


def validate_call(value):
    if not value:
        return "Позывной обязателен", None
    call = normalize_call(value)
    if not call or len(call) > 3 or not call.isalnum():
        return "Неверный позывной. Используйте до 3 символов (буквы и цифры)", None
    return None, call


def validate_report(value):
    if not value:
        return "Рапорт обязателен", None
    report = normalize_report(value)
    if report is None:
        return "Рапорт должен быть в формате XX/XX (например, 59/99)", None
    return None, report


def validate_link(date, range_, call, report):
    errors = []
    date_error, date_value = validate_date(date)
    range_error, range_value = validate_range(range_)
    call_error, call_value = validate_call(call)
    report_error, report_value = validate_report(report)

    if date_error:
        errors.append(date_error)
    if range_error:
        errors.append(range_error)
    if call_error:
        errors.append(call_error)
    if report_error:
        errors.append(report_error)

    return errors, {
        "date": date_value,
        "range": range_value,
        "call": call_value,
        "report": report_value,
    }
