from abc import ABC
from rich.console import Text
from enum import Enum, auto


class Terminals(Enum):
    TERMINAL = auto()
    TELEGRAM = auto()


class ConsoleOutputAbstract(ABC):
    service: Enum

    def output(self, text: str, *args) -> str:
        ...


class TerminalClearRichOutputConsole:

    def get_clear_text(self, text: str) -> str:
        r_text = Text.from_markup(text)
        for segment in r_text:
            if segment.style:
                segment.style.bold = False
        text = r_text.plain
        return text


class TerminalOutput(ConsoleOutputAbstract, TerminalClearRichOutputConsole):
    service = Terminals.TERMINAL

    def output(self, text: str, *args) -> None:
        text = self.get_clear_text(text)
        print(f"Send to TerminalOutput: {text}")


class Telegram:
    def __init__(self, token):
        self.token = token

    def send_message(self, text):
        print(f"Send {text} to Telegram")


class TelegramOutput(ConsoleOutputAbstract, TerminalClearRichOutputConsole):
    service = Terminals.TELEGRAM

    def __init__(self, token) -> None:
        self.telegram_client = Telegram(token)
        super().__init__()

    def output(self, text: str, *args) -> None:
        text = self.get_clear_text(text)
        self.telegram_client.send_message(text)
