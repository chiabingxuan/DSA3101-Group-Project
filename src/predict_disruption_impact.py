import pandas as pd
import os
from prefixspan import PrefixSpan
from collections import deque


# Parameters for the prediction of impacts of bus disruptions
DECAY_FACTOR = 0.8
BFS_MAX_DEPTH = 3

BUS_STOP_COORDINATES = {
    "Kent Ridge MRT / Opp Kent Ridge MRT": (1.2949169774094218, 103.78450347558939),
    "LT27 / S17": (1.2974629302644196, 103.78085273302771),
    "UHC / Opp UHC": (1.2988678848068846, 103.7759206887556),
    "UTown": (1.3035493102220883, 103.7745363670092),
    "COM3": (1.2949516906131686, 103.77494690050855),
    "BIZ2 / Opp HSSML": (1.2931431812053542, 103.7750819279268),
    "LT13 / Ventus": (1.2952473123850663, 103.77060867365277),
    "IT / CLB": (1.296984108396615, 103.77264737349888),
    "PGP": (1.2914385089186413, 103.78047445708181)
}

BUS_STOP_NAMES = list(BUS_STOP_COORDINATES.keys())

BUS_NUM_ROUTES = {
    "A1": ["LT13 / Ventus", "BIZ2 / Opp HSSML", "PGP", "Kent Ridge MRT / Opp Kent Ridge MRT", "LT27 / S17", "UHC / Opp UHC", "IT / CLB", "LT13 / Ventus"],
    "A2": ["IT / CLB", "UHC / Opp UHC", "LT27 / S17", "Kent Ridge MRT / Opp Kent Ridge MRT", "PGP", "BIZ2 / Opp HSSML", "LT13 / Ventus", "IT / CLB"],
    "D1": ["COM3", "BIZ2 / Opp HSSML", "LT13 / Ventus", "IT / CLB", "UTown", "IT / CLB", "LT13 / Ventus", "BIZ2 / Opp HSSML", "COM3"],
    "D2": ["COM3", "PGP", "Kent Ridge MRT / Opp Kent Ridge MRT", "LT27 / S17", "UHC / Opp UHC", "UTown", "UHC / Opp UHC", "LT27 / S17", "Kent Ridge MRT / Opp Kent Ridge MRT", "PGP", "COM3"]
}

def find_distance(start_index, end_index, length_of_list):
    # Finds distance travelled from start to end (distance measured in terms of number of bus stops visited along the way)
    # If start is to the left of end in the list, then simply find the distance from start ... end
    if start_index <= end_index:
        return end_index - start_index

    # Else, find the distance travelled when we "loop around" the list, moving from start to end
    return length_of_list - (start_index - end_index)


def find_bus_stops_visited(bus_num, start, end):
    # Remove last bus stop since it is the same as the first bus stop
    route_for_bus_num = BUS_NUM_ROUTES[bus_num][:-1]

    length_of_route = len(route_for_bus_num)

    # Bus stops can appear more than once in the route. We need to determine the shortest route from starting to ending bus stops, based on the given route

    # Smallest index in the route, for starting bus stop
    start_first_occurrence_index = route_for_bus_num.index(start)

    # Next index in the route (if any), for starting bus stop
    if start in route_for_bus_num[start_first_occurrence_index + 1:]:
        start_second_occurrence_index = route_for_bus_num[start_first_occurrence_index + 1:].index(start) + start_first_occurrence_index + 1
    else:
        start_second_occurrence_index = -1

    # Smallest index in the route, for ending bus stop
    end_first_occurrence_index = route_for_bus_num.index(end)

    # Next index in the route (if any), for ending bus stop
    if end in route_for_bus_num[end_first_occurrence_index + 1:]:
        end_second_occurrence_index = route_for_bus_num[end_first_occurrence_index + 1:].index(end) + end_first_occurrence_index + 1
    else:
        end_second_occurrence_index = -1

    # Finding shortest route from start to end
    # Smallest indices of start and end definitely exist
    correct_start_index, correct_end_index = start_first_occurrence_index, end_first_occurrence_index
    min_distance = find_distance(correct_start_index, correct_end_index, length_of_route)

    # List of possible routes between start and end
    remaining_possible_pairs_of_bus_stop_indices = [(start_first_occurrence_index, end_second_occurrence_index), (start_second_occurrence_index, end_first_occurrence_index), (start_second_occurrence_index, end_second_occurrence_index)]
    for pair in remaining_possible_pairs_of_bus_stop_indices:
        start_index, end_index = pair[0], pair[1]
        if start_index != -1 and end_index != -1:   # ensure that both start and ending indices must exist
            distance = find_distance(start_index, end_index, length_of_route)
            if distance < min_distance:
                correct_start_index = start_index
                correct_end_index = end_index

    # Record the desired route (in the correct order)
    bus_stops_visited = list()
    index = correct_start_index
    while index != ((correct_end_index + 1) % length_of_route):
        new_bus_stop_visited = route_for_bus_num[index]
        bus_stops_visited.append(new_bus_stop_visited)
        index = (index + 1) % length_of_route
    return bus_stops_visited


def get_support(sequences_supports, sequence):
    return sequences_supports[sequence]


def get_confidence(sequences_supports, antecedent, antecedent_and_consequent):
    return get_support(sequences_supports, antecedent_and_consequent) / get_support(sequences_supports, antecedent)


def conduct_prefixspan(trip_data):
    num_of_rows = trip_data.shape[0]    # number of transactions

    # Get the ordered sequence of bus stops visited for each transaction
    sequences_of_bus_stops = list(trip_data.apply(lambda row: find_bus_stops_visited(row["bus_num"], row["start"], row["end"]), axis=1))

    # Carry out PrefixSpan algorithm to determine the supports of sequences
    ps = PrefixSpan(sequences_of_bus_stops)

    # Get sequences and its associated supports. Use minsup = 1 because we want to consider all sequences
    sequences = ps.frequent(minsup=1)
    sequences_support = {tuple(sequence[1]): sequence[0] / num_of_rows for sequence in sequences}
    return sequences_support


def get_rules(sequences_supports):
    rules = list()
    for sequence in sequences_supports:
        for i in range(len(sequence)):
            for j in range(i + 1, len(sequence)):
                # For each sequence, consider each X -> Y such that X and Y are individual bus stops, and X comes before Y in the sequence
                antecedent = (sequence[i],)
                consequent = (sequence[j],)
                antecedent_and_consequent = antecedent + consequent

                # Get confidence for the rule antecedent (X) -> consequent (Y)
                confidence = get_confidence(sequences_supports, antecedent, antecedent_and_consequent)

                # Get rule. Also, we extract names of bus stops
                rule = (antecedent[0], consequent[0], confidence)
                if rule not in rules:
                    rules.append(rule)  # ensures rules are unique

    # Sort rules by decreasing confidence
    rules.sort(key=lambda x: x[2], reverse=True)
    return rules


def make_weighted_graph_from_rules(rules):
    # Graph will be in the form of {A: [(B: 0.67), (C: 0.5), ...], ...}, where the letters are the bus stops and the floats are the confidence values
    graph = dict()
    for antecedent, consequent, metric in rules:
        if antecedent not in graph:
            graph[antecedent] = list()
        graph[antecedent].append((consequent, metric))

    # In case there are some bus stops that do not appear in any of the rules - add them to graph as well
    for bus_stop in BUS_STOP_NAMES:
        if bus_stop not in graph:
            graph[bus_stop] = list()
    return graph


def bfs_disruption_propagation(graph, start_node, initial_delay, decay_factor, max_depth):
    """
    Perform BFS to propagate disruption from the start node.

    Parameters:
    - graph: A dictionary where keys are nodes and values are lists of (neighbour, weight) tuples.
    - start_node: The initial disrupted bus stop.
    - initial_delay: The delay at the start node.
    - decay_factor: Factor by which delay reduces as it propagates.
    - max_depth: Maximum number of hops to propagate.

    Returns:
    - delays: A dictionary with each node and its propagated delay.
    """
    delays = {start_node: initial_delay}
    queue = deque([(start_node, initial_delay, 0)])  # (node, delay, depth)

    while queue:
        current_node, current_delay, depth = queue.popleft()

        # Stop if max depth is reached
        if depth >= max_depth:
            continue

        # Propagate to neighbours
        for neighbour, weight in graph.get(current_node, []):
            # Calculate new delay for the neighbour
            propagated_delay = current_delay * weight * decay_factor

            # Update the delay for the neighbour if it's higher than an existing one
            if neighbour not in delays or propagated_delay > delays[neighbour]:
                delays[neighbour] = propagated_delay
                queue.append((neighbour, propagated_delay, depth + 1))

    return delays


def main(start_node="COM3", initial_delay=30, decay_factor=DECAY_FACTOR, max_depth=BFS_MAX_DEPTH):   # the default arguments correspond to a sample scenario (delay of 30 minutes starting from COM3)
    # Read trip_data
    trip_data = pd.read_csv(os.path.join(os.path.dirname( __file__), "../data/train_trip_data_after_sdv.csv"), keep_default_na=False)

    # Use PrefixSpan algorithm to get sequences of bus stops, along with their supports
    sequences_supports = conduct_prefixspan(trip_data)

    # Obtain association rules. For our case we consider ordered rules X -> Y, where X and Y are individual bus stops. This rule says that if bus stop X is visited, then it is likely that bus stop Y will subsequently be visited
    rules = get_rules(sequences_supports)

    # Make weighted directed graph. Nodes are bus stops. Each edge A -> B has a weight equal to the confidence value of the rule A -> B
    graph = make_weighted_graph_from_rules(rules)

    # Carry out a modified version of BFS to estimate delays that are caused by a single source of disruption
    delays = bfs_disruption_propagation(graph, start_node=start_node, initial_delay=initial_delay, decay_factor=decay_factor, max_depth=max_depth)
    delays = [(bus_stop, round(est_delay, 2)) for bus_stop, est_delay in delays.items()]
    delays.sort(key=lambda pair: pair[1], reverse=True)
    print(delays)

    return delays


if __name__ == "__main__":
    main()
