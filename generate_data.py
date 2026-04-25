import pandas as pd
import numpy as np

np.random.seed(42)

n = 500

data = pd.DataFrame({
    "income": np.random.randint(30000, 100000, n),
    "rent": np.random.randint(8000, 25000, n),
    "food": np.random.randint(2000, 10000, n),
    "transport": np.random.randint(1000, 5000, n),
    "entertainment": np.random.randint(1000, 8000, n),
    "shopping": np.random.randint(1000, 10000, n),
})

data["savings"] = data["income"] - data.drop(columns=["income"]).sum(axis=1)

data.to_csv("data/finance_data.csv", index=False)

print("✅ Dataset created successfully!")