import csv
import datetime

def load_metro_stations():
    """Load metro station data from a CSV file."""
    with open('metro_stations.csv', mode='r') as file:
        reader = csv.reader(file)
        data = {rows[1]: (rows[0], rows[2], list(map(int, rows[3].split('-')))) for rows in reader}
    return data

def load_tourism():
    """Load tourism data from a CSV file."""
    with open('tourism.csv', mode='r') as file:
        reader = csv.reader(file)
        data = {rows[0]: (rows[1], rows[2], float(rows[3])) for rows in reader}
    return data

def load_transportation():
    """Load transportation data from a CSV file."""
    with open('transportation.csv', mode='r') as file:
        reader = csv.reader(file)
        data = {rows[0]: (rows[1], rows[2], float(rows[3])) for rows in reader}
    return data

def write_tourism(data):
    """Write tourism data to a CSV file."""
    with open('tourism.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for key, value in data.items():
            writer.writerow([key] + list(value))

def write_transportation(data):
    """Write transportation data to a CSV file."""
    with open('transportation.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for key, value in data.items():
            writer.writerow([key] + list(value))

def interchanges():
    stations_data = load_metro_stations()
    data = {}
    stations_connections = {}
    lines = {}
    interchanges = {}

    for station_id, (station_name, line, connections) in stations_data.items():
        if station_name in stations_connections:
            if station_name not in interchanges:
                interchanges[station_name] = station_id
            stations_connections[station_name] = stations_connections[station_name] + connections
            lines[station_name] = lines[station_name] + "-" + line
        else:
            lines[station_name] = line
            stations_connections[station_name] = connections
        data[station_id] = (station_name, line, connections)

    dict_stations_connections = {}
    for station_name, connections in stations_connections.items():
        dict_stations_connections[station_name] = {data[str(conn)][0]: 1 for conn in connections}

    return interchanges, lines, dict_stations_connections

def shortest(start, goal):
    interchange_stations, data, nodes = interchanges()
    shortest_distance = {}
    track_predecessor = {}
    unseen_nodes = nodes
    infinity = 999999
    track_path = []

    for node in unseen_nodes:
        shortest_distance[node] = infinity
    shortest_distance[start] = 0

    while unseen_nodes:
        min_distance_node = None
        for node in unseen_nodes:
            if min_distance_node is None:
                min_distance_node = node
            elif shortest_distance[node] < shortest_distance[min_distance_node]:
                min_distance_node = node

        path_options = nodes[min_distance_node].items()

        for child_node, weight in path_options:
            if weight + shortest_distance[min_distance_node] < shortest_distance[child_node]:
                shortest_distance[child_node] = weight + shortest_distance[min_distance_node]
                track_predecessor[child_node] = min_distance_node

        unseen_nodes.pop(min_distance_node)

    current_node = goal
    while current_node != start:
        try:
            track_path.insert(0, current_node)
            current_node = track_predecessor[current_node]
        except KeyError:
            print("Path is not reachable")
            break
    track_path.insert(0, start)
    cost = shortest_distance[goal]
    path = track_path

    no_of_interchanges, route = printing_path(path, interchange_stations, data)
    return path, interchange_stations, data, no_of_interchanges, route

def printing_path(path, interchange_stations, data):
    no_of_interchanges = 0
    route = ''
    for j in range(len(path)):
        if path[j] in interchange_stations and j != 0 and j != len(path) - 1:
            if data[path[j + 1]] != data[path[j - 1]]:
                route += (str(path[j]) + f'  "[INTERCHANGE] FROM {data[path[j - 1]]} TO {data[path[j + 1]]}"  ----->')
                no_of_interchanges += 1
            else:
                route += (str(path[j]) + '----->')
        else:
            if j != len(path) - 1:
                route += (str(path[j]) + '----->')
            else:
                route += (str(path[j]) + ' [DESTINATION]\n')
    return no_of_interchanges, route

def tourism(start, location):
    tourism_data = load_tourism()
    goal = tourism_data[location][0]
    print_info(location, tourism_data[location])
    track_path, interchange_stations, data, no_of_interchanges, route = shortest(start, goal)
    print(route)
    print("Cost Of Journey :", cost_calc(start, goal), "RUPEES")
    print("Estimated Time Of Journey :", time_calc(len(track_path) - 1, no_of_interchanges), "MINUTES\n")

def transportation(start, location):
    transportation_data = load_transportation()
    goal = transportation_data[location][0]
    print_info(location, transportation_data[location])
    track_path, interchange_stations, data, no_of_interchanges, route = shortest(start, goal)
    print(route)
    print("Cost Of Journey :", cost_calc(start, goal), "RUPEES")
    print("Estimated Time Of Journey :", time_calc(len(track_path) - 1, no_of_interchanges), "MINUTES\n")

def print_info(name, tup):
    station, line, dist = tup
    print(f"\n------  {name}  ------")
    print(f'CLOSEST STATION : {station}')
    print(f'CLOSEST METRO LINE : {line}')
    print(f'DISTANCE FROM {station.upper()} STATION : {dist} Km\n ')
    print(f'------  METRO ROUTE TO {name}  ------\n')

def update_tourism():
    tourism_data = load_tourism()
    n = 1
    print("------- The Tourist Locations Located Near Metro Stations -------\n")
    for location in tourism_data.keys():
        print(str(n) + ".", location)
        n += 1
    locations = tuple(tourism_data.keys())
    
    location = locations[int(input("Which One Would You Like To Update (Enter Number) : ")) - 1]
    name = input("Enter New Name :").title()
    closest_station = station_input("Closest")
    line = input("Enter Line Of Closest Station :")
    dist = float(input(f"Enter Distance Of {name} From The Closest Station :"))
    tourism_data[name] = (closest_station, line, dist)
    write_tourism(tourism_data)
    print("Record Updated Successfully !!!! ")

def add_new_tourism():
    tourism_data = load_tourism()
    name = input("Enter New Name :").title()
    if name not in tourism_data:
        closest_station = station_input("Closest")
        line = input("Enter Line Of Closest Station :")
        dist = float(input(f"Enter Distance Of {name} From The Closest Station :"))
        tourism_data[name] = (closest_station, line, dist)
        write_tourism(tourism_data)
        print("Record Added Successfully !!!! ")
    else:
        print(f"{name} Already Exists In The Database")

def delete_tourism():
    tourism_data = load_tourism()
    n = 1
    print("------- The Tourist Locations Located Near Metro Stations -------\n")
    for location in tourism_data.keys():
        print(str(n) + ".", location)
        n += 1
    locations = tuple(tourism_data.keys())
    
    location = locations[int(input("Which One Would You Like To Delete (Enter Number) : ")) - 1]
    del tourism_data[location]
    write_tourism(tourism_data)
    print("Record Deleted Successfully")

def station_input(type):
    lst = linelst()
    lineslist = tuple(lst.keys())
    n = 1
    print(f"\nSelect a line for the {type} station:")
    for i in lineslist:
        print(str(n) + ".", i)
        n += 1
    line = int(input(f"Enter Number Of The Line On Which The {type} Station Is Located: "))
    stations = lst[lineslist[line - 1]]
    n = 1
    print(f"\nSelect the {type} station:")
    for i in stations:
        print(str(n) + ".", i)
        n += 1
    station = int(input(f"Enter Number Of The {type} Station: "))
    return stations[station - 1]

def linelst():
    metro_data = load_metro_stations()
    data = {}
    for station_id, (station_name, line, connections) in metro_data.items():
        if line not in data:
            data[line] = [station_name]
        else:
            data[line].append(station_name)
    return data

def time_calc(no_of_stations, no_of_interchanges):
    return int(3.5 * no_of_stations + 5 * no_of_interchanges)

def cost_calc(start, goal):
    path, interchange_stations, data, no_of_interchanges, route = shortest(start, goal)
    stations = len(path) - 1
    dist = int(stations * 1.25)

    if datetime.datetime.today().weekday() == 5 or datetime.datetime.today().weekday() == 6:
        if dist == 0:
            return 0
        elif dist <= 2:
            return 10
        elif dist <= 5:
            return 20
        elif dist <= 12:
            return 30
        elif dist <= 21:
            return 40
        elif dist <= 32:
            return 50
        else:
            return 60
    else:
        if dist == 0:
            return 0
        elif dist <= 2:
            return 10
        elif dist <= 5:
            return 20
        elif dist <= 12:
            return 30
        elif dist <= 21:
            return 40
        elif dist <= 32:
            return 50
        else:
            return 60

if __name__ == "__main__":
    while True:
        print("Welcome to the Metro Navigation System")
        print("1. Find Shortest Route")
        print("2. Find Tourism Location")
        print("3. Find Transportation Location")
        print("4. Update Tourism Data")
        print("5. Add New Tourism Location")
        print("6. Delete Tourism Location")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            start = station_input("Starting")
            goal = station_input("Destination")
            path, interchange_stations, data, no_of_interchanges, route = shortest(start, goal)
            print(route)
            print("Cost Of Journey :", cost_calc(start, goal), "RUPEES")
            print("Estimated Time Of Journey :", time_calc(len(path) - 1, no_of_interchanges), "MINUTES\n")

        elif choice == '2':
            start = station_input("Starting")
            location = input("Enter the tourism location: ")
            tourism(start, location)

        elif choice == '3':
            start = station_input("Starting")
            location = input("Enter the transportation location: ")
            transportation(start, location)

        elif choice == '4':
            update_tourism()

        elif choice == '5':
            add_new_tourism()

        elif choice == '6':
            delete_tourism()

        elif choice == '7':
            print("Thank you for using the Metro Navigation System!")
            break

        else:
            print("Invalid choice! Please try again.")
