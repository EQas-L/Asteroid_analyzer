

class LogError(Exception):
    pass


class FatalLogError(LogError):
    pass


class RecoverableLogError(LogError):
    pass


class UnsupportedVersionError(FatalLogError):
    def __init__(self, line: int, found: object, supported: int) -> None:
        self.line = line
        self.found = found
        self.supported = supported
        super().__init__(
            f"строка {line}: версия схемы {found!r}, поддерживается {supported}"
        )

class MalformedLineError(RecoverableLogError):
    def __init__(self, line: int, reason: str) -> None:
        self.line = line
        self.reason = reason
        super().__init__(f"строка {line}: не разбирается как JSON ({reason})")


class IncompleteRecordError(RecoverableLogError):
    def __init__(self, line: int, field: str) -> None:
        self.line = line
        self.field = field
        super().__init__(f"строка {line}: нет обязательного поля {field!r}")


class UnknownSpriteTypeError(RecoverableLogError):
    def __init__(self, line: int, raw_type: object) -> None:
        self.line = line
        self.raw_type = raw_type
        super().__init__(f"строка {line}: неизвестный тип спрайта {raw_type!r}")

