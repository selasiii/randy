# Randy Bot 🐍💸
**Randy** is an experimental Forex scalping bot built in Python that executes a dual trade (Buy + Sell) at the open of every 1-minute candle. It uses a tight stop loss to catch sharp directional moves, and if one trade wins, it enters a series of anti-martingale trades in the winning direction using exponential lot sizes.

```


---

# Randy Bot 🐍💸
---

## ⚙️ Core Features

- Executes Buy & Sell orders on every new M1 candle
- Applies tight stop losses to both trades
- On SL trigger: launches anti-martingale in the winning direction
- Supports breakeven and trailing stop loss logic
- Closes profitable trades by largest lot size first
- Modular, toggleable filters:
  - Directional bias (e.g., EMA-based)
  - Multiple Timeframe confluence
  - Pause during choppy conditions

---

## 📁 Project Structure

```

randy\_bot/
│
├── main.py               # Entry point for running Randy
├── config.py             # Strategy settings and toggles
│
├── core/                 # Core bot logic
│   ├── candle\_handler.py       # Detects new candles
│   ├── order\_executor.py       # Places and manages trades
│   ├── trade\_manager.py        # Anti-martingale execution logic
│   ├── risk\_manager.py         # Daily limits and trade halts
│   ├── filters.py              # Optional strategy filters
│
├── utils/                # Helper modules
│   ├── mt5\_utils.py             # MT5 helpers (points, symbols, ticks)
│   ├── logger.py                # Logging and file output
│
├── logs/                 # Log files and trade outputs
│   └── trade\_log.txt
│
└── README.md             # This file

```
### 📂 Module Responsibilities

| **File**            | **Purpose**                                                                 |
| ------------------- | --------------------------------------------------------------------------- |
| `main.py`           | Runs the infinite loop, calls other modules                                 |
| `config.py`         | Stores all adjustable parameters and strategy toggles                       |
| `candle_handler.py` | Detects new M1 candles, notifies `main.py`                                  |
| `order_executor.py` | Places Buy/Sell orders with SL, handles MT5 order API                       |
| `trade_manager.py`  | Handles anti-martingale entries, SL triggers, breakeven, trailing SL, exits |
| `risk_manager.py`   | Checks if daily loss/profit exceeded; halts trading if so                   |
| `filters.py`        | Contains toggleable features like directional bias, MTF, chop filter        |
| `mt5_utils.py`      | Point calculation, price fetching, order checking, etc                      |
| `logger.py`         | Logs all trades and important events                                        |



---

## 📌 Dependencies

- Python 3.8+
- MetaTrader5 (`pip install MetaTrader5`)
- pytz (`pip install pytz`)

---

## 🚀 Getting Started

1. Clone the repo or create the folder manually:
```

mkdir randy\_bot && cd randy\_bot

````

2. Create the file structure above.

3. Add your MT5 login/account details to the environment if needed.

4. Run the bot:
```bash
python main.py
````

---

## 🧪 Roadmap

* [ ] Implement anti-martingale spacing & lot sizing
* [ ] Breakeven & trailing stop logic
* [ ] Toggleable strategy filters
* [ ] MT5 trading statistics logging
* [ ] GUI frontend (optional)

---

## ⚠️ Disclaimer

Randy is an experimental bot for educational purposes. Trading leveraged instruments involves risk. Use it at your own discretion and always backtest thoroughly.

---

```
