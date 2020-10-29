#%% JSON to dataframe
import pandas as pd
import json

with open('database.json') as f:
    data = json.load(f)

df = pd.DataFrame(columns=['article', 'source'])

pos = 0

for i, ID in enumerate(data):

    entry = len(data[ID]['Citedby'])

    for j in range(entry):
        df.loc[pos] = [ID, data[ID]['Citedby'][j]]

        pos +=1

# %%
