import os
import pandas as pd

df = pd.read_csv(os.path.join("data", "chat_messeges_25000.csv"))
df["len"] = df["text"].apply(lambda x: len(str(x).split()))
df["len_sim"] = df["text"].apply(lambda x: len(list(str(x))))

print(df[["text", "len_sim"]])

print(df.info())
df_sum = df[['discriminator', "len_sim", "len"]].groupby(['discriminator'], as_index=False).sum()
print(df_sum)

df_sum.to_csv(os.path.join("data", "chat_messeges_len_25000.csv"))