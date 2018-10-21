
execfile(u'/Users/joe/Rcl-topology-cleaner/sGraph/clean_tool.py'.encode('utf-8'))
execfile(u'/Users/joe/Rcl-topology-cleaner/sGraph/sNode.py'.encode('utf-8'))
execfile(u'/Users/joe/Rcl-topology-cleaner/sGraph/sEdge.py'.encode('utf-8'))
execfile(u'/Users/joe/Rcl-topology-cleaner/sGraph/utilityFunctions.py'.encode('utf-8'))

#execfile(u'/Users/I.Kolovou/Documents/GitHub/Road-network-cleaner/sGraph/clean_tool.py'.encode('utf-8'))

# SETTINGS _______________________________________________________________________
import time
start_time = time.time()

# input settings
layer_name = 'road_small2'
#layer_name = 'madagascar'
#layer_name = 'comp_model_cr_cl_simpl10'
layer = getLayerByName(layer_name)

# cleaning settings
Snap = 1
Break = True
#Merge = 'between intersections'
Merge = ['collinear', 10]
Orphans = True

Errors = True
Unlinks = True

# output settings
path = None

# RUN____________________________________________________________________________

clean_tool = cleanTool(Snap, Break, Merge, Errors, Unlinks, Orphans)

"""0.LOAD"""
res = map(lambda f:clean_tool.sEdgesSpIndex.insertFeature(f), clean_tool.features_iter(layer))

"""1.BREAK"""
# TODO: speed up
broken_edges = map(lambda (sedge, vertices): clean_tool.breakAtVertices(sedge, vertices), clean_tool.breakFeaturesIter())
res = map(lambda edge_id: clean_tool.del_edge(edge_id), filter(lambda edge_id: edge_id is not None, broken_edges))

# create topology
res = map(lambda (edgeid, qgspoint): clean_tool.createTopology(qgspoint, edgeid), clean_tool.endpointsIter())

# 2. SNAP # errors: snapped
res = map(lambda (edgeid, qgspoint): clean_tool.createTopology(qgspoint, edgeid), clean_tool.endpointsIter())
# group based on distance - create subgraph
subgraph_nodes = clean_tool.subgraph_nodes()
collapsed_edges = map(lambda nodes: clean_tool.mergeNodes(nodes),
                      clean_tool.con_comp_iter(subgraph_nodes))
res = map(lambda edge_id: clean_tool.del_edge(edge_id),
          set(list(itertools.chain.from_iterable(collapsed_edges))))

# 3. MERGE # errors merged

subgraph_nodes = clean_tool.subgraph_con2_nodes()
res = map(lambda group_edges: clean_tool.merge_edges(group_edges),
          clean_tool.con_comp_iter(subgraph_nodes))


# 4. ORPHANS
# errors orphans, closed polylines
res = map(
lambda sedge: clean_tool.del_edge_w_nodes(sedge.id, sedge.getStartNode(), sedge.getEndNode()),
filter(lambda edge: clean_tool.sNodes[edge.getStartNode()].getConnectivity() ==
                    clean_tool.sNodes[edge.getEndNode()].getConnectivity() == 1,
       clean_tool.sEdges.values()))










all_errors = []

all_errors += zip(clean_tool.multiparts, ['multipart'] * len(clean_tool.multiparts))
all_errors += zip(clean_tool.points, ['point'] * len(clean_tool.points))
all_errors += zip(clean_tool.orphans, ['orphan'] * len(clean_tool.orphans))
all_errors += zip(clean_tool.closed_polylines, ['closed polyline'] * len(clean_tool.closed_polylines))
all_errors += zip(clean_tool.duplicates, ['duplicate'] * len(clean_tool.duplicates))
all_errors += zip(clean_tool.broken, ['broken'] * len(clean_tool.broken))
all_errors += zip(clean_tool.merged, ['pseudo'] * len(clean_tool.merged))
all_errors += zip(clean_tool.self_intersecting, ['self intersection'] * len(clean_tool.self_intersecting))
all_errors += zip(clean_tool.snapped, ['snapped'] * len(clean_tool.snapped))


all_errors2 = dict([k, set([i[1] for i in list(g)])] for k, g in itertools.groupby(sorted(all_errors), operator.itemgetter(0)))
errors_feats = [self.create_error_feat(p, errors) for p, errors in all_errors2.items()]










print 'na'
