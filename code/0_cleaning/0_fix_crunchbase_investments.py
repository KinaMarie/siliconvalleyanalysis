import pandas as pd
import numpy as np

#----------
# Settings
#----------
input_file = "../../rawData/crunchbase_export_investments.csv"
output_file = "corrected_investments.csv"

# Function for cleaning
def clean_mixed_string(x):
	if pd.notnull(x):
		stripped_string = x.replace(",", "").replace("-", "NaN")
		return float(stripped_string)
	else:
		return float(x)

#----------
# Procedure
#----------
inv = pd.read_csv(input_file, low_memory=False)  # Load Raw Data
grouped = inv.groupby("funding_round_permalink", # Group By Funding Round
					  as_index=False, 
					  axis=0)

# In exploratory analysis, we confirmed that Crunchbase assigned every
# investor in a round the same investment size (i.e., raised_amount_usd
# was set to the size of the round. We assign each investor the average
# so our aggregates are correct.

# Find the total number of investor and the amount of funding raised.
agg = pd.concat([grouped["company_permalink"].count(), 
                 grouped["raised_amount_usd"].first()["raised_amount_usd"]], 
                 axis = 1)
agg.columns = ["funding_round_permalink", "count", "raised_amount_usd"]

# Calculate Avg. Per Round
avg_investment = agg["raised_amount_usd"].apply(clean_mixed_string)/agg["count"]

# Associate with funding round key
correction = pd.concat([agg["funding_round_permalink"], avg_investment], axis=1)
correction.columns = ["funding_round_permalink", "raised_amount_usd"]

# Merge Correction Into Original Dataset
output = pd.merge(inv.drop(["raised_amount_usd"], axis=1), 
				  correction, 
				  how='inner', 
				  on ="funding_round_permalink")

# Write Corrected File
output.to_csv(output_file, index=False)
