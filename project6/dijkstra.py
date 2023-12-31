import sys
import json
import math  # If you want to use math.inf for infinity
import netfuncs

def initialize_data_structures(routers, src_ip):
    to_visit = set()
    distance = {}
    parent = {}

    for router in routers:
        to_visit.add(router)
        distance[router] = math.inf
        parent[router] = None
    
    # Set the distance to source ip's router to 0
    src_ip_router = netfuncs.find_router_for_ip(routers, src_ip)
    distance[src_ip_router] = 0

    return to_visit, distance, parent

def min_distance(distance, to_visit):
    min_distance_router = ""
    min_distance = math.inf
    for router in to_visit:
        if distance[router] < min_distance:
            min_distance_router = router
            min_distance = distance[router]
    
    return min_distance_router

def build_shortest_path_tree(to_visit, distance, routers, parent):
    # Find shortest path
    # while to_visit is not empty
    while len(to_visit) != 0:
        # get the node with the shortest distance
        current_node = min_distance(distance, to_visit)

        # remove the node from the set
        to_visit.remove(current_node)

        # Iterate over the neighbor nodes
        for neighbor_router, specs in routers[current_node]["connections"].items():
            distance_to_neighbor = specs["ad"]

            # Calculate the distance to the source
            distance_to_source = distance_to_neighbor + distance[current_node]

            # If the distance is less than the neighbors current distance, relax the distance
            if distance_to_source < distance[neighbor_router]:
                # Update the router's distance
                distance[neighbor_router] = distance_to_source

                # Update the router's parent
                parent[neighbor_router] = current_node

    return parent

def get_shortest_path(dest_ip_router, src_ip_router, parent):
    path = []

    # set the current node as the destination ip's router
    current_node = dest_ip_router

    # Walk the dictionary back to the source
    while current_node != src_ip_router:

        # append nodes to the path
        path.append(current_node)

        # Update the current node
        current_node = parent[current_node]

    # Append the source ip's router to the path
    path.append(src_ip_router)

    # Reverse the path so it is displayed correctly
    path.reverse()

    return path

def dijkstras_shortest_path(routers, src_ip, dest_ip):
    """
    This function takes a dictionary representing the network, a source
    IP, and a destination IP, and returns a list with all the routers
    along the shortest path.

    The source and destination IPs are **not** included in this path.

    Note that the source IP and destination IP will probably not be
    routers! They will be on the same subnet as the router. You'll have
    to search the routers to find the one on the same subnet as the
    source IP. Same for the destination IP. [Hint: make use of your
    find_router_for_ip() function from the last project!]

    The dictionary keys are router IPs, and the values are dictionaries
    with a bunch of information, including the routers that are directly
    connected to the key.

    This partial example shows that router `10.31.98.1` is connected to
    three other routers: `10.34.166.1`, `10.34.194.1`, and `10.34.46.1`:

    {
        "10.34.98.1": {
            "connections": {
                "10.34.166.1": {
                    "netmask": "/24",
                    "interface": "en0",
                    "ad": 70
                },
                "10.34.194.1": {
                    "netmask": "/24",
                    "interface": "en1",
                    "ad": 93
                },
                "10.34.46.1": {
                    "netmask": "/24",
                    "interface": "en2",
                    "ad": 64
                }
            },
            "netmask": "/24",
            "if_count": 3,
            "if_prefix": "en"
        },
        ...

    The "ad" (Administrative Distance) field is the edge weight for that
    connection.

    **Strong recommendation**: make functions to do subtasks within this
    function. Having it all built as a single wall of code is a recipe
    for madness.
    """
    
    # An array to store the shortest path
    path = []

    # If the source IP and destination IP are on the same subnet, return an empty array
    src_ip_router = netfuncs.find_router_for_ip(routers, src_ip)
    dest_ip_router = netfuncs.find_router_for_ip(routers, dest_ip)
    src_ip_slash = routers[src_ip_router]["netmask"]

    if netfuncs.ips_same_subnet(src_ip, dest_ip, src_ip_slash):
        return path

    # Initialize data structures
    to_visit, distance, parent = initialize_data_structures(routers, src_ip)

    # build the shortest path tree
    parent = build_shortest_path_tree(to_visit, distance, routers, parent)

    # Walk the path
    path = get_shortest_path(dest_ip_router, src_ip_router, parent)

    return path

#------------------------------
# DO NOT MODIFY BELOW THIS LINE
#------------------------------
def read_routers(file_name):
    with open(file_name) as fp:
        data = fp.read()

    return json.loads(data)

def find_routes(routers, src_dest_pairs):
    for src_ip, dest_ip in src_dest_pairs:
        path = dijkstras_shortest_path(routers, src_ip, dest_ip)
        print(f"{src_ip:>15s} -> {dest_ip:<15s}  {repr(path)}")

def usage():
    print("usage: dijkstra.py infile.json", file=sys.stderr)

def main(argv):
    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)

    routers = json_data["routers"]
    routes = json_data["src-dest"]

    find_routes(routers, routes)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
