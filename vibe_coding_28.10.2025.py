import pandas as pd
df = pd.DataFrame({"cat": ["A", "B", "C", "A", "B"]})
df["cat_encoded"] = df["cat"].astype("category").cat.codes
print(df)