import pandas as pd
import pickle as pkl

results_raw = pkl.load(open("results.pkl", "rb"))
results = []

print(results_raw)

for entry in results_raw:
	results.append({"Univ. Name": entry["name"], "City": entry["location"].split(",")[0], "State": entry["location"].split(",")[1]})

pd.DataFrame(results).sort_values(by="State").to_csv("results3.csv")
