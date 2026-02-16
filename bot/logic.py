from main_bot import GridBot  # The class above
import threading
import time
from db import find_by_acc_id

def run_trading_ticks(bot_instance):
    """Thread 1: High-speed trading logic (0.1s)"""
    print(f"[{bot_instance.login}] Trading thread started.")
    while bot_instance.is_running:
        bot_instance.tick()
        time.sleep(0.1)
    print(f"[{bot_instance.login}] Trading thread stopped.")


def run_param_sync(bot_instance, acc_id):
    """Thread 2: Low-speed database sync (5.0s)"""
    print(f"[{bot_instance.login}] Sync thread started.")
    while bot_instance.is_running:
        time.sleep(5.0)  # Wait first
        new_settings = find_by_acc_id(acc_id)
        if new_settings:
            bot_instance.update_trade_params(new_settings)
            print(f"[{acc_id}] Parameters updated from DB.")
    print(f"[{bot_instance.login}] Sync thread stopped.")


def start_bot_threads(acc_id, credential):
    """Launcher: Sets up both threads for one account"""
    settings = find_by_acc_id(acc_id)
    if not settings: return

    settings['password'] = credential["password"]  # "M@12919953m"
    settings['server'] = credential["server"]  # "Exness-MT5Real20"
    settings['terminal_path'] = credential["meta_path"]  # "/path/to/terminal64.exe"
    bot_instance = GridBot(settings)

    if bot_instance.initialize():
        # Define the threads
        t1 = threading.Thread(target=run_trading_ticks, args=(bot_instance,), daemon=True)
        t2 = threading.Thread(target=run_param_sync, args=(bot_instance, acc_id), daemon=True)

        # Start them
        t1.start()
        t2.start()