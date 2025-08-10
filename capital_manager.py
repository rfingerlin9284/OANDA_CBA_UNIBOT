import os

CAPITAL_FILE = "capital.txt"
INITIAL_CAPITAL = 3000.0

class CapitalManager:

    def __init__(self):
        self.capital = INITIAL_CAPITAL
        self._load()

    def _load(self):
        if os.path.exists(CAPITAL_FILE):
            with open(CAPITAL_FILE, 'r') as f:
                try:
                    self.capital = float(f.read().strip())
                except Exception:
                    self.capital = INITIAL_CAPITAL
        else:
            self._save()

    def _save(self):
        with open(CAPITAL_FILE, 'w') as f:
            f.write(f"{self.capital:.2f}")

    def update(self, pnl):
        self.capital += pnl
        # Enforce floor and ceiling
        if self.capital < 0:
            self.capital = 0
        if self.capital > self.MAX_CAPITAL:
            self.capital = self.MAX_CAPITAL
        self._save()

    def get(self):
        return self.capital

    def reset(self):
        self.capital = INITIAL_CAPITAL
        self._save()

capital_manager = CapitalManager()
