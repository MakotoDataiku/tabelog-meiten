# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
import dataiku
from dataiku import pandasutils as pdu
import pandas as pd
import numpy as np
import os

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
my_dataset = dataiku.Dataset("tabelog_w_stars_embedded_cleaned")
df = my_dataset.get_dataframe()
reviews = df['review_cleaned'].tolist()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
max_text_length = dataiku.get_custom_variables(typed=True)['max_text_length']

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
folder_path = dataiku.Folder("CwbeZ55S").get_path()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
files = os.listdir(folder_path)
if '0_BERTJapanese' in files:
    model_path = folder_path + '/0_BERTJapanese'
else:
    print("モデルが見つかりません")

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
tokenizer = AutoTokenizer.from_pretrained("daigo/bert-base-japanese-sentiment")

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
model = AutoModelForSequenceClassification.from_pretrained("daigo/bert-base-japanese-sentiment")

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# handling NaN values
reviews_truncated = []
for r in reviews:
    try:
        r = r[:int(max_text_length)]
        reviews_truncated.append(r)
    except:
        reviews_truncated.append("")

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
sentiment_analyzer = pipeline("sentiment-analysis",model=model,tokenizer=tokenizer)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
list_sentiments = list(map(sentiment_analyzer, reviews_truncated))

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
dict_sentiments = [d[0] for d in list_sentiments]

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df = df.join(pd.DataFrame(dict_sentiments).rename(columns={"label":"sentiment_label", "score":"sentiment_score"}))

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
py_recipe_output = dataiku.Dataset("sentiment")
py_recipe_output.write_with_schema(df)