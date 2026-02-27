
import time
from bot.logic import start_bot_threads


marady_silver = {"login": 159858707,
                "password": "t8b1@1Li!L9bVAQ",
                "server": "Exness-MT5Real20",
                "terminal_path": r"D:\bot\marady_bot\MetaTrader 5\terminal64.exe"}
print(marady_silver)
start_bot_threads("md-silver", marady_silver)

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print("Stopping bot")