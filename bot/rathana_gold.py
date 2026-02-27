import time

from bot.logic import start_bot_threads

rathana_gold = {"login": 183825419,
                "password": "M@12919953m",
                "server": "Exness-MT5Real25",
                "terminal_path": r"D:\bot\rathana_bot\mt5_gold\terminal64.exe"}
start_bot_threads("rn-gold", rathana_gold)





try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print("Stopping bot")