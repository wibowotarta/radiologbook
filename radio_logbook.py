# === Stage 1: Каркас модуля ===
# Project: RadioLogbook
from dataclasses import dataclass, field
from datetime import date


@dataclass
class QSO:
    """Одна радиосвязь в журнале."""

    date: date
    band: str
    call: str
    report: str


def make_demo_records() -> list[QSO]:
    """Создаёт несколько демонстрационных записей о связях."""

    records = [
        QSO(date=date(2024, 1, 15), band="20m", call="UA1ABC", report="59"),
        QSO(date=date(2024, 2, 3), band="40m", call="DL2XYZ", report="57"),
        QSO(date=date(2024, 3, 21), band="15m", call="SP9QRS", report="59"),
        QSO(date=date(2024, 4, 10), band="80m", call="G3HIJ", report="55"),
    ]
    return records


def main() -> None:
    """Краткий вывод о содержимом журнала."""

    records = make_demo_records()
    print("Радиолюбительский журнал RadioLogbook")
    print(f"Всего связей: {len(records)}")
    for record in records:
        print(record.date, record.band, record.call, record.report)


if __name__ == "__main__":
    main()
