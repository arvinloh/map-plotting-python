"""
This file is part of Assignment 2 of FIT1045, S1 2023.

It contains the class Itinerary.

@file itinerary.py
"""

import math
from city import City, create_example_cities, get_cities_by_name

class Itinerary():
    """
    A sequence of cities.
    """

    def __init__(self, cities: list[City]) -> None:
        """
        Creates an itinerary with the provided sequence of cities,
        conserving order.
        :param cities: a sequence of cities, possibly empty.
        :return: None
        """
        self.cities = cities
        
    def total_distance(self) -> int:
        """
        Returns the total distance (in km) of the itinerary, which is
        the sum of the distances between successive cities.
        :return: the total distance.
        """
        distance = 0
        for i in range(len(self.cities) - 1):
            distance += self.cities[i].distance(self.cities[i + 1])
        return distance

    def append_city(self, city: City) -> None:
        """
        Adds a city at the end of the sequence of cities to visit.
        :param city: the city to append
        :return: None.
        """
        self.cities.append(city)

    def min_distance_insert_city(self, city: City) -> None:
        """
        Inserts a city in the itinerary so that the resulting
        total distance of the itinerary is minimized.
        :param city: the city to insert
        :return: None.
        """
        if not self.cities:
            self.cities.append(city)
        else:
            min_distance = float('inf')
            min_index = 0

            for i in range(len(self.cities) + 1):
                temp_cities = self.cities.copy()
                temp_cities.insert(i, city)
                temp_itinerary = Itinerary(temp_cities)
                temp_distance = temp_itinerary.total_distance()

                if temp_distance < min_distance:
                    min_distance = temp_distance
                    min_index = i

            self.cities.insert(min_index, city)
            
    def __str__(self) -> str:
        """
        Returns the sequence of cities and the distance in parentheses
        For example, "Melbourne -> Kuala Lumpur (6368 km)"

        :return: a string representing the itinerary.
        """
        city_str = ' -> '.join(city.name for city in self.cities)
        return f"{city_str} ({self.total_distance()} km)"

if __name__ == "__main__":
    create_example_cities()
    test_itin = Itinerary([get_cities_by_name("Melbourne")[0],
                           get_cities_by_name("Kuala Lumpur")[0]])
    print(test_itin)

    #we try adding a city
    test_itin.append_city(get_cities_by_name("Baoding")[0])
    print(test_itin)

    #we try inserting a city
    test_itin.min_distance_insert_city(get_cities_by_name("Sydney")[0])
    print(test_itin)

    #we try inserting another city
    test_itin.min_distance_insert_city(get_cities_by_name("Canberra")[0])
    print(test_itin)
