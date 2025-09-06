# core/antimartingale_manager.py

def reset_antimartingale_state(state):
    """Completely reset antimartingale state."""
    state["antimartingale_active"] = False
    state["open_positions"].clear()
    state["pending_orders"].clear()
    state["last_direction"] = None
    print("[Antimartingale] State reset.")
