import networkx
import matplotlib.pyplot as plt

G = networkx.Graph()
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_edge(1,2)
G.add_edge(3,4)
G.add_edge(1,4)
G.add_edge(1,3)
networkx.draw(G,with_labels=1)
plt.show()
