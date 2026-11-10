# === Stage 3: Хранилище в памяти ===
# Project: RadioLogbook
from datetime import datetime
from typing import List, Dict, Optional


class Connection:
    def __init__(self, date: datetime, band: str, callsign: str, report: str, identifier: Optional[str] = None):
        self.identifier = identifier
        self.date = date
        self.band = band
        self.callsign = callsign
        self.report = report

    def to_dict(self) -> Dict:
        return {
            "identifier": self.identifier,
            "date": self.date.isoformat() if isinstance(self.date, datetime) else self.date,
            "band": self.band,
            "callsign": self.callsign,
            "report": self.report,
        }


class InMemoryConnectionStore:
    def __init__(self) -> None:
        self._connections: Dict[str, Connection] = {}
        self._counter = 0

    def add(self, date: datetime, band: str, callsign: str, report: str) -> Connection:
        self._counter += 1
        identifier = f"conn_{self._counter}"
        connection = Connection(date, band, callsign, report, identifier)
        self._connections[identifier] = connection
        return connection

    def get(self, identifier: str) -> Optional[Connection]:
        return self._connections.get(identifier)

    def list(self) -> List[Connection]:
        return list(self._connections.values())


if __name__ == "__main__":
    store = InMemoryConnectionStore()
    c1 = store.add(datetime(2024, 1, 15, 10, 30), "HF", "UA1ABC", "59")
    c2 = store.add(datetime(2024, 1, 16, 14, 45), "VHF", "RZ3ADX", "57")
    print(store.list())
    print(store.get(c1.identifier))
