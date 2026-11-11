# === Stage 4: Удаление и восстановление ===
# Project: RadioLogbook
SoftDeleteLogbookModule

from datetime import datetime
from typing import List, Optional, Dict


class SoftDeletedEntry:
    """Модель связи с поддержкой мягкого удаления и восстановления."""

    def __init__(self, date: datetime, band: str, callsign: str, report: str,
                 deleted: bool = False):
        self.id = None
        self.date = date
        self.band = band
        self.callsign = callsign
        self.report = report
        self.deleted = deleted

    def soft_delete(self) -> None:
        """Фиксируем время удаления и помечаем запись как скрытую."""
        self.deleted = True
        self.deleted_at = datetime.now()

    def restore(self) -> None:
        """Восстанавливаем запись из мягко удалённого состояния."""
        self.deleted = False

    def is_visible(self) -> bool:
        return not self.deleted


class SoftDeleteLogbookManager:
    """Рабочий слой: добавление, удаление и восстановление связей."""

    def __init__(self):
        self._entries: List[SoftDeletedEntry] = []

    def add_entry(self, date: datetime, band: str, callsign: str, report: str) -> SoftDeletedEntry:
        entry = SoftDeletedEntry(date, band, callsign, report)
        entry.id = len(self._entries) + 1
        self._entries.append(entry)
        return entry

    def delete_entry(self, entry: SoftDeletedEntry) -> bool:
        """Мягкое удаление: не удаляем из хранилища, а скрываем."""
        if entry in self._entries:
            entry.soft_delete()
            return True
        return False

    def restore_entry(self, entry: SoftDeletedEntry) -> bool:
        if entry in self._entries and entry.deleted:
            entry.restore()
            return True
        return False

    def get_visible_entries(self) -> List[SoftDeletedEntry]:
        return [e for e in self._entries if e.is_visible()]

    def get_deleted_entries(self) -> List[SoftDeletedEntry]:
        return [e for e in self._entries if e.deleted]

    def find_entry(self, callsign: str) -> Optional[SoftDeletedEntry]:
        for entry in self._entries:
            if entry.callsign == callsign:
                return entry
        return None

    def count_visible(self) -> int:
        return len(self.get_visible_entries())

    def to_dict(self) -> Dict:
        result = []
        for entry in self._entries:
            record = {
                "id": entry.id,
                "date": entry.date.isoformat(),
                "band": entry.band,
                "callsign": entry.callsign,
                "report": entry.report,
                "deleted": entry.deleted,
            }
            if entry.deleted_at is not None:
                record["deleted_at"] = entry.deleted_at.isoformat()
            result.append(record)
        return result
