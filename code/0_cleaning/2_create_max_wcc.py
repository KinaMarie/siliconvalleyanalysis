import networkx as nx

#---------
# Settings
#---------
input_file = "post_2005_edges.csv"
output_file = "max_wcc_graph.edgelist"
attributes = ["weight", "date"] # All additiona attributes, order matters

# Attach a list of the attribute names in the attribute variable in order to
# embed an arbitrary amount of data in the graph.
def customGraphGenerator(filename, attribute_key):
    g = nx.DiGraph()
    
    with open(filename, 'r') as f:
        for line in f.readlines():
            
            # Parse Line
            edge = line.strip().split(",")
            
            # Create Attributes
            attributes = dict(zip(attribute_key, edge[2:]))
            
            # Add Edge
            g.add_edge(edge[0], edge[1], attr_dict=attributes)

    return g

#----------
# Procedure
#----------
# Generate the graph
g = customGraphGenerator(input_file, attribute_key = attributes)

# Ensure bipartiteness
# If a node has both incoming edges and outgoing edges, keep the larger set of edges.
# i.e., 8 in-degree, 4 out-degree --> discard all outgoing edges for the node
in_d = g.in_degree()
out_d = g.out_degree()

for node in g.nodes_iter():
    if in_d[node] != 0 and out_d[node] != 0:
        if in_d[node] > out_d[node]:
        	for destination in g.successors(node):
        		g.remove_edge(node, destination)
        else:
        	for source in g.predecessors(node):
        		g.remove_edge(source, node)

# Calculate the MaxWCC
maxWCCnodes = max(nx.weakly_connected_components(g), key=len)
wcc = g.subgraph(maxWCCnodes)

# Write the edge to a NetworkX format; delimiter='\t'
nx.write_edgelist(wcc, output_file, delimiter="\t", data=True)

## READ IN USING THIS FUNCTION
# g = nx.read_edgelist("max_wcc_graph.edgelist", create_using=nx.DiGraph(), delimiter="\t", data=True)