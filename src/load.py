"""load data for the given ticker and date range"""

from data.loader import load, load_history

df = load('aapl')

df_change_history = load_history('aapl', 'change', 5)
change_future = (df['close'].shift(-5) - df['close']) / df['close'] * 100.0
change_future.name = 'change+5'

dataset = df_change_history.join(change_future).dropna()
print dataset

y = dataset.pop('change+5')
X = dataset
