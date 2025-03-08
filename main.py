import csv


def load_metro_stations(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        stations_data = {}
        for row in reader:
            station_id = int(row['StationID'])
            station_name = row['StationName']
            metro_line = row['MetroLine']
            connections = [int(x) for x in row['Connections'].split('-')]
            stations_data[station_id] = {
                'station_name': station_name,
                'metro_line': metro_line,
                'connections': connections
            }
        return stations_data

def load_tourism_data(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        tourism_data = {}
        for row in reader:
            location_name = row['LocationName']
            closest_station = int(row['ClosestStation'])
            line = row['Line']
            distance = float(row['Distance'])
            tourism_data[location_name] = {
                'closest_station': closest_station,
                'line': line,
                'distance': distance
            }
        return tourism_data

def load_transportation_data(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        transportation_data = {}
        for row in reader:
            facility_name = row['FacilityName']
            closest_station = int(row['ClosestStation'])
            line = row['Line']
            distance = float(row['Distance'])
            transportation_data[facility_name] = {
                'closest_station': closest_station,
                'line': line,
                'distance': distance
            }
        return transportation_data

# Initialize the data
metro_stations = load_metro_stations('metro_stations.csv')
tourism_data = load_tourism_data('tourism.csv')
transportation_data = load_transportation_data('transportation.csv')

# Update the rest of the functions to use these dictionaries instead of SQL queries

def shortest_path(start_station, goal_station):
    interchange_stations, station_lines, station_connections = get_interchange_stations()
    shortest_distance = {}
    track_predecessor = {}
    unseen_nodes = station_connections
    infinity = float('inf')
    track_path = []

    for node in unseen_nodes:
        shortest_distance[node] = infinity
    shortest_distance[start_station] = 0

    while unseen_nodes:
        min_distance_node = None
        for node in unseen_nodes:
            if min_distance_node is None:
                min_distance_node = node
            elif shortest_distance[node] < shortest_distance[min_distance_node]:
                min_distance_node = node

        path_options = station_connections[min_distance_node].items()

        for child_node, weight in path_options:
            if weight + shortest_distance[min_distance_node] < shortest_distance[child_node]:
                shortest_distance[child_node] = weight + shortest_distance[min_distance_node]
                track_predecessor[child_node] = min_distance_node

        unseen_nodes.pop(min_distance_node)

    current_node = goal_station
    while current_node != start_station:
        try:
            track_path.insert(0, current_node)
            current_node = track_predecessor[current_node]
        except KeyError:
            print("Path is not reachable")
            break

    track_path.insert(0, start_station)
    total_cost = shortest_distance[goal_station]
    path = track_path

    num_interchanges, route_description = describe_path(path, interchange_stations, station_lines)
    return path, interchange_stations, station_lines, num_interchanges, route_description

# The rest of the functions will be similarly refactored...

