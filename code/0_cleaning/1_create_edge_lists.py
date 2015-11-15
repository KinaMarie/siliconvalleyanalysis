import pandas as pd
import datetime as dt

#---------
# Settings
#---------
input = 'corrected_investments.csv'
checkpoint1 = "checkpoint_full_investment_edges.csv"
def format_date(x):
	# Choose the right delimiter
	if "/" in x:
		x = x.split('/')
	else:
		x = x.split('-')

	# Put the data in the correct order and return a DT object
	if int(x[2]) > 1000:
		return dt.datetime(int(x[2]), int(x[0]), int(x[1]))
	else:
		return dt.datetime(int(x[0]), int(x[1]), int(x[2]))

# Currently, we return ZERO if we have no details on a transaction
def format_raised(x):
	if not pd.isnull(x):
		return int(x)  
	else:
		return 0

#----------
# Procedure
#----------
df = pd.read_csv(input, low_memory=False) # Load Data

# Put the edges in the correct direction (investor --> company)
edge_list = df[["investor_permalink", "company_permalink"]]

# Process Meta Information
edge_list.loc[:, "raised_amount_usd"] = df["raised_amount_usd"].apply(format_raised)
edge_list.loc[:, "invest_date"] = df["funded_at"].apply(format_date)

# ADD ADDITIONAL DATA HERE
# If we wanted to add additional meta-information, we can just continue to build
# the edge_list datafarme by cleaning columns from "df" to "edge_list".

#------Checkpoint 1-----------------------------
# For convenience, we save the full set of edges
edge_list.to_csv(checkpoint1, index='false')
#-----------------------------------------------

# Keep only investments that occured post 2005
post_2005_edges = edge_list[edge_list["invest_date"] > dt.datetime(2004,12,31)]
post_2005_edges.to_csv("post_2005_edges.csv")


