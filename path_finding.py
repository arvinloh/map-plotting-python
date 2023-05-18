import networkx as nx
import math
from city import City, get_city_by_id
from itinerary import Itinerary
from vehicles import Vehicle, create_example_vehicles
from csv_parsing import create_cities_countries_from_csv

def find_shortest_path(vehicle: Vehicle, from_city: City, to_city: City) -> Itinerary | None:
    """
    Returns a shortest path between two cities for a given vehicle as an Itinerary,
    or None if there is no path.

    :param vehicle: The vehicle to use.
    :param from_city: The departure city.
    :param to_city: The arrival city.
    :return: A shortest path from departure to arrival, or None if there is none.
    """
    graph = nx.DiGraph()

    cities = list(City.id_to_cities.values())
    for city_obj in cities:
        graph.add_node(city_obj.city_id, city=city_obj)

    for i in range(len(cities)):
        for j in range(len(cities)):
            if i != j:
                travel_time = vehicle.compute_travel_time(cities[i], cities[j])
                if travel_time != math.inf:
                    graph.add_edge(cities[i].city_id, cities[j].city_id, weight=travel_time)

    try:
        shortest_path = nx.shortest_path(graph, source=from_city.city_id, target=to_city.city_id, weight="weight")
        return Itinerary([City.id_to_cities[city_id] for city_id in shortest_path])
    except nx.NetworkXNoPath:
        return None

if __name__ == "__main__":
    create_cities_countries_from_csv("worldcities_truncated.csv")
    vehicles = create_example_vehicles()

    from_cities = set()
    for city_id in [1036533631, 1036142029, 1458988644]:
        from_cities.add(get_city_by_id(city_id))

    #we create some vehicles
    vehicles = create_example_vehicles()

    to_cities = set(from_cities)
    for from_city in from_cities:
        to_cities -= {from_city}
        for to_city in to_cities:
            print(f"{from_city} to {to_city}:")
            for test_vehicle in vehicles:
                shortest_path = find_shortest_path(test_vehicle, from_city, to_city)
                print(f"\t{test_vehicle.compute_itinerary_time(shortest_path)}"
                      f" hours with {test_vehicle} with path {shortest_path}.")
