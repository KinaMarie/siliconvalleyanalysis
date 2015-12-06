import pandas as pd
import datetime as dt
import networkx as nx

# Load Data
G = nx.read_edgelist("../0_cleaning/max_wcc_graph.edgelist", 
                     create_using=nx.DiGraph(), 
                     delimiter="\t", 
                     data=True)

def dfToGraph(df):
    g = nx.DiGraph()
    edge_list = map(lambda x: list(x[0:2]) + 
                              [dict(zip(df.columns[2:], x[2:]))], 
                    df.values)
    g.add_edges_from(edge_list)

    return g

def writeEdgelist(g, filename):
    # Convert date to string
    temp = map(lambda (x, y): (x, y.strftime('%Y-%m-%d')), 
               nx.get_edge_attributes(g, "date").items())
    nx.set_edge_attributes(g, "date", dict(temp))
    
    # Write to file
    nx.write_edgelist(g,filename, delimiter="\t", data=True)

#------------------------------
# Extract Attributes From Graph
#------------------------------
dates = nx.get_edge_attributes(G, 'date')
weights = nx.get_edge_attributes(G, 'weight')

# Store Attribute Dictionaries  As A DataFrame
flat_table = map(lambda x: [x[0], x[1], weights[x], dates[x]], dates)
wcc_df = pd.DataFrame(flat_table)
wcc_df.columns = ["investor", "company", "weight", "date"]
wcc_df["date"] = wcc_df["date"].apply(pd.to_datetime)
wcc_df.sort_values(by="date", inplace=True)

#-------------------------
#Create A Set Of Snapshots
#-------------------------
# Settings
num_months = 132
months_per_period = 3
num_periods = num_months/months_per_period

# Set the time range
rng = pd.date_range(start='12/1/2004',
                    end='12/1/2015',
                    freq='M')


# Iterate through periods
for i in range(1,num_periods):
    # Set period start and end for both cumulative and difference snapshots
    period = i * months_per_period

    #--------------------
    # Cumulative Snapshot
    #--------------------
    # Set Date Restriction For Cumulative Snapshot
    (cum_start, cum_end) = (rng[0], rng[period-1])

    mask_cum = ((wcc_df['date'] > cum_start) & 
                (wcc_df['date'] <= cum_end))

    cum_snapshot = wcc_df[mask_cum]         # Gen Snapshot

    g = dfToGraph(cum_snapshot)
    filename = "./cumulative_snapshots/enddate_" + cum_end.strftime('%Y%m%d') + ".edgelist"
    writeEdgelist(g, filename)


    #--------------
    # Diff Snapshot
    #--------------
    # Set Date Restriction For Diff Snapshot
    (diff_start, diff_end) = (rng[period-months_per_period-1], rng[period-1])

    mask_diff = ((wcc_df['date'] > diff_start) & 
                 (wcc_df['date'] <= diff_end))

    diff_snapshot = wcc_df[mask_diff]     # Gen Snapshot

    # Construct Filename
    file_name = ("./diff_snapshots/diff_" +
                 diff_start.strftime('%Y%m%d') + 
                 '_' +
                 diff_end.strftime('%Y%m%d') + 
                 ".csv")

    # Save Diff
    diff_snapshot.to_csv(file_name, 
                         index=False, 
                         encoding='utf-8')



