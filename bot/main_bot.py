import MetaTrader5 as mt5


class GridBot:
    def __init__(self, config):
        # Account Credentials
        self.acc_id = config.get('acc_id')
        self.login = config.get('login')
        self.password = config.get('password')
        self.server = config.get('server')
        self.terminal_path = config.get('terminal_path')
        self.name = config.get('name')

        # # Trading Parameters
        self.symbol = config.get('pair')
        self.lot_size = config.get('lot_size')
        self.grid_step = config.get('grid_step')
        self.tp_distance = config.get('tp')  # distance for Take Profit
        self.magic_number = config.get('magic', 999)
        self.active = config.get('active')
        self.max_position = config.get('max_position')
        self.count = 0
        # Internal State
        self.ath_tracker = 0.0
        self.is_running = False

        # Log Message
        self.log_message = ""

    def update_trade_params(self, config):
        # Trading Parameters
        self.symbol = config.get('pair')
        self.lot_size = config.get('lot_size')
        self.grid_step = config.get('grid_step')
        self.tp_distance = config.get('tp')  # distance for Take Profit
        self.magic_number = config.get('magic', 999)
        self.max_position = config.get('max_position')
        self.active = config.get('active')

    def initialize(self):
        """Connects to MT5 terminal with specific credentials."""
        if not mt5.initialize(
                path=self.terminal_path,
                login=self.login,
                password=self.password,
                server=self.server
        ):
            print(f"[{self.login}] Initialization failed: {mt5.last_error()}")
            return False

        print(f"[{self.login}] Connected to {self.server} for {self.symbol}")
        self.is_running = True
        return True

    def open_buy_with_tp(self, price):
        """Executes a BUY order with a calculated TP."""
        tp_price = round(price + self.tp_distance, 3)
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": self.lot_size,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "tp": tp_price,
            "magic": self.magic_number,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"[{self.login}] Order failed: {result.comment}")
        else:
            print(f"[{self.login}] BUY @ {price} | TP @ {tp_price}")
        return result

    def tick(self):
        self.count += 1
        if self.active == 0:
            self.log_message = f"[{self.active}] bot is disabled"
            return

        """Main logic loop to be called every second."""
        tick_info = mt5.symbol_info_tick(self.symbol)
        if tick_info is None:
            self.log_message = f"[{self.symbol}] is not available"
            return

        current_ask = tick_info.ask
        positions = mt5.positions_get(symbol=self.symbol, magic=self.magic_number)
        if len(positions) >= self.max_position:
            self.log_message = f"[{len(positions)}] is over max position: [{self.max_position}]"
            return

        if not positions:
            # Logic for first entry
            if current_ask > self.ath_tracker:
                self.ath_tracker = current_ask

            target_price = self.ath_tracker - self.grid_step
            self.log_message = f"[{self.name}] | Price: {current_ask:.3f} | Peak: {self.ath_tracker:.3f} | Buy at: {target_price:.3f}"
            print(
                f"[{self.login}] Price: {current_ask:.3f} | Peak: {self.ath_tracker:.3f} | Buy at: {target_price:.3f}",
                end="\r")

            if current_ask <= target_price:
                self.open_buy_with_tp(current_ask)
                self.ath_tracker = 0  # Reset peak after buying
        else:
            # Logic for grid averaging
            lowest_entry = min([p.price_open for p in positions])
            target_grid = lowest_entry - self.grid_step
            self.log_message = f"[{self.name}] | Price: {current_ask:.3f} | Lowest: {lowest_entry:.3f} | Next: {target_grid:.3f}"
            print(f"[{self.login}] Price: {current_ask:.3f} | Lowest: {lowest_entry:.3f} | Next: {target_grid:.3f}",
                  end="\r")


            if current_ask <= target_grid:
                self.open_buy_with_tp(current_ask)

    def stop(self):
        self.is_running = False
        mt5.shutdown()
