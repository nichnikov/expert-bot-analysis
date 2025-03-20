import os
import re
import pandas as pd

df = pd.read_csv(os.path.join("data", "first_user_message_analysis", "bss_chats_20250201_20250320.csv"))
print(df.info())

patterns = re.compile(r"\n|\¶|(?P<url>https?://[^\s]+)|<a href=|</a>|/#/document/\d\d/\d+/|\"\s*\">|\s+")
for col in ["chat_id", "text"]:
    df[col] = df[col].apply(lambda x: patterns.sub(" ", str(x)))

df[["id", "chat_id", "created", "text", "discriminator", "user_id", "evaluation"]].to_feather(os.path.join("data", "first_user_message_analysis", "bss_chats_20250201_20250320.feather"))