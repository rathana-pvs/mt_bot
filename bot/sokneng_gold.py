
import time
from bot.logic import start_bot_threads


sokneng_gold = {"login": 257293722,
                "password": "M@12919953m",
                "server": "Exness-MT5Real36",
                "terminal_path": r"D:\bot\sokneng_bot\mt5_gold\terminal64.exe"}

start_bot_threads("sn-gold", sokneng_gold)

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print("Stopping bot")