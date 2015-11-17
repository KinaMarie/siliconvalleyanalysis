import datetime as dt
import networkx as nx

def loadEdgelist(filename):
	# Readin graph
	g = nx.read_edgelist(filename, 
	                     delimiter="\t", 
	                     create_using  = nx.DiGraph(), 
	                     data=True)

	# Convert Weight To Float
	temp = map(lambda (x, y): (x, float(y)), 
			   nx.get_edge_attributes(g, "weight").items())
	nx.set_edge_attributes(g, "weight", dict(temp))

	# Convert Date to datetime
	temp = map(lambda (x, y): (x, dt.datetime.strptime(y, "%Y-%m-%d")), 
			   nx.get_edge_attributes(g, "date").items())
	nx.set_edge_attributes(g, "date", dict(temp))

	return g

def writeEdgelist(g, filename):
    # Convert date to string
    temp = map(lambda (x, y): (x, y.strftime('%Y-%m-%d')), 
               nx.get_edge_attributes(g, "date").items())
    nx.set_edge_attributes(g, "date", dict(temp))
    
    # Write to file
    nx.write_edgelist(g,filename, delimiter="\t", data=True)
