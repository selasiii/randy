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


## TASK LIST

Here's a **clear and actionable developer task list** to build out the full Randy forex trading bot in stages. We'll follow a modular development roadmap so each step is focused, testable, and builds on the last.

---

### ✅ PHASE 1: Basic Trade Execution

**Goal:** Set up Randy to detect new 1-minute candles and place Buy + Sell orders.

* [x] **Initialize MT5 connection**
* [x] **Detect new M1 candles**
* [x] **Place Buy + Sell orders with tight SL**
* [x] **Log trade actions to console/log file**
* [x] ✅ Finalize `main.py`, `candle_handler.py`, `order_executor.py`

---

### 🔁 PHASE 2: Anti-Martingale Logic

**Goal:** Add reaction logic once SL is hit to scale into the winning direction.

* [x] Detect which initial trade was stopped out
* [x] Begin placing exponentially larger trades in the winning direction
* [x] Implement pip-based spacing between anti-martingale entries
* [x] Limit number of anti-martingale trades (`max_trades`)
* [x] Finalize `trade_manager.py`

---

### 🛡 PHASE 3: Breakeven and Trailing SL

**Goal:** Lock in profits intelligently and exit safely.

* [ ] Move SL to breakeven after `X` pips
* [ ] Enable trailing SL after `Y` pips
* [ ] Finalize dynamic SL logic inside `trade_manager.py`

---

### 📊 PHASE 4: Risk Management

**Goal:** Protect capital and control exposure.

* [ ] Implement max daily loss / profit logic
* [ ] Halt trading after hitting limits
* [ ] SL-based trade invalidation logic (if gap or slippage exceeds tolerance)
* [ ] Finalize `risk_manager.py`

---

### 🎯 PHASE 5: Optional Strategy Filters

**Goal:** Add toggleable confluence checks to improve signal quality.

* [ ] Directional bias filter (e.g., EMA 20 > EMA 50 = bullish bias)
* [ ] Multi-timeframe trend alignment (M1 aligned with M5 or M15)
* [ ] Choppy market filter using ATR or Bollinger Band width
* [ ] Add all strategy toggles to `config.py`
* [ ] Finalize `filters.py`

---

### 📁 PHASE 6: Logging & Utilities

**Goal:** Ensure logging, tracking, and reusable MT5 helpers.

* [ ] Log trades, SL/TP, and bot events to `logs/trade_log.txt`
* [ ] Create helper functions in `mt5_utils.py` (e.g., get\_price, get\_point, check\_open\_orders)
* [ ] Finalize `logger.py` and `mt5_utils.py`

---

### 🖥 PHASE 7: Optional GUI / Dashboard (stretch goal)

**Goal:** Add a visual dashboard or control panel.

* [ ] Show open trades, lot progression, current P/L
* [ ] Manual toggle to pause/resume bot
* [ ] Export trade history

---

### 🧪 PHASE 8: Testing & Optimization

**Goal:** Backtest and optimize the bot under various conditions.

* [ ] Backtest core logic on historical data
* [ ] Optimize SL, pip spacing, breakeven, trailing SL
* [ ] Stress test with volatile pairs
* [ ] Prepare checklist for going live

---

### 🔚 FINAL PHASE: Deployment

**Goal:** Package and deploy the bot for daily execution.

* [ ] Create `.env` or secure config for credentials
* [ ] Add startup and restart logic
* [ ] (Optional) Integrate Telegram alerts or error notifications

---

Let me know when you want to tackle **PHASE 1** step-by-step — I’ll start generating the actual code for `main.py`, `config.py`, and `core/candle_handler.py`.

