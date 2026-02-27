import time

from bot.logic import start_bot_threads

rathana_silver = {"login": 159877428,
                "password": "M@12919953m",
                "server": "Exness-MT5Real20",
                "terminal_path": r"D:\bot\rathana_bot\MetaTrader 5\terminal64.exe"}
start_bot_threads("rn-silver", rathana_silver)





try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print("Stopping bot")