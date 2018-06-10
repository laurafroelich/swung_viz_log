import pandas as pd
import json

file = "well_log_data.txt"

with open(file, 'r') as f:
    j_data = json.load(f)

for i, item in enumerate(j_data):
    if i == 0:
        p_data = pd.DataFrame(item)
    else:
        p_data = p_data.append(pd.DataFrame(item), sort=True)
