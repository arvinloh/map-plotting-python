"""
This file is part of Assignment 2 of FIT1045, S1 2023.

It contains the abstract class Vehicle and other classes that
inherit from it.

@file vehicles.py
"""
import math
from abc import ABC, abstractmethod
from city import City, get_city_by_id
from country import find_country_of_city, create_example_countries
from itinerary import Itinerary

class Vehicle(ABC):
    """
    A Vehicle defined by a mode of transportation, which results in a specific duration.
    """

    @abstractmethod
    def compute_travel_time(self, departure: City, arrival: City) -> float:
        """
        Returns the travel duration of a direct trip from one city
        to another, in hours, rounded up to an integer.
        Returns math.inf if the travel is not possible.

        :param departure: the departure city.
        :param arrival: the arrival city.
        :return: the travel time in hours, rounded up to an integer,
                 or math.inf if the travel is not possible.
        """

    def compute_itinerary_time(self, itinerary: Itinerary) -> float:
        """
        Returns a travel duration for the entire itinerary for a given vehicle.
        Returns math.inf if any leg (i.e. part) of the trip is not possible.

        :param itinerary: The itinerary.
        :return: the travel time in hours (an integer),
                 or math.inf if the travel is not possible.
        """
        total_time = 0
        for i in range(len(itinerary.cities) - 1):
            travel_time = self.compute_travel_time(itinerary.cities[i], itinerary.cities[i + 1])
            if travel_time == math.inf:
                return math.inf
            total_time += travel_time
        return total_time

    @abstractmethod
    def __str__(self) -> str:
        """
        Returns the class name and the parameters of the vehicle in parentheses.

        :return: the string representation of the vehicle.
        """

class CrappyCrepeCar(Vehicle):
    """
    A type of vehicle that:
        - Can go from any city to any other at a given speed.
    """

    def __init__(self, speed: int) -> None:
        """
        Creates a CrappyCrepeCar with a given speed in km/h.

        :param speed: the speed in km/h.
        """
        self.speed = speed

    def compute_travel_time(self, departure: City, arrival: City) -> float:
        """
        Returns the travel duration of a direct trip from one city
        to another, in hours, rounded up to an integer.

        :param departure: the departure city.
        :param arrival: the arrival city.
        :return: the travel time in hours, rounded up to an integer,
                 or math.inf if the travel is not possible.
        """
        distance = departure.distance(arrival)
        return math.ceil(distance / self.speed)

    def __str__(self) -> str:
        """
        Returns the class name and the parameters of the vehicle in parentheses.
        For example "CrappyCrepeCar (100 km/h)"

        :return: the string representation of the vehicle.
        """
        return f"CrappyCrepeCar ({self.speed} km/h)"

class DiplomacyDonutDinghy(Vehicle):
    """
    A type of vehicle that:
        - Can travel between any two cities in the same country.
        - Can travel between two cities in different countries.
        - Has different speed for the two cases.
    """

    def __init__(self, in_country_speed: int, between_primary_speed: int) -> None:
        self.in_country_speed = in_country_speed
        self.between_primary_speed = between_primary_speed

    def compute_travel_time(self, departure: City, arrival: City) -> float:
        """
        Returns the travel duration of a direct trip from one city
        to another, in hours, rounded up to an integer.
        Returns math.inf if the travel is not possible.

        :param departure: the departure city.
        :param arrival: the arrival city.
        :return: the travel time in hours, rounded up to an integer,
                 or math.inf if the travel is not possible.
        """
        departure_country = find_country_of_city(departure)
        arrival_country = find_country_of_city(arrival)

        if departure_country is None or arrival_country is None:
            return math.inf

        if departure_country == arrival_country:
            speed = self.in_country_speed
        elif departure.city_type != "primary" or arrival.city_type != "primary":
            return math.inf
        else:
            speed = self.between_primary_speed
        #Make sure that it is traveling between capitals of the country, if not print math.inf
        

        distance = departure.distance(arrival)
        
        travel_time = math.ceil(distance / speed)
        if travel_time == math.inf:
            return math.inf

        return travel_time

    def __str__(self) -> str:
        return f"DiplomacyDonutDinghy ({self.in_country_speed} km/h | {self.between_primary_speed} km/h)"

class TeleportingTarteTrolley(Vehicle):
    """
    A type of vehicle that:
    - Can travel between any two cities if the distance is less than a given maximum distance.
    - Travels in fixed time between two cities within the maximum distance.
    """
    def __init__(self, travel_time:int, max_distance: int) -> None:
        """
        Creates a TeleportingTarteTrolley with a distance limit in km.

        :param travel_time: the time it takes to travel.
        :param max_distance: the maximum distance it can travel.
        """
        self.travel_time = travel_time
        self.max_distance = max_distance

    def compute_travel_time(self, departure: City, arrival: City) -> float:
        """
        Returns the travel duration of a direct trip from one city
        to another, in hours, rounded up to an integer.
        Returns math.inf if the travel is not possible.

        :param departure: the departure city.
        :param arrival: the arrival city.
        :return: the travel time in hours, rounded up to an integer,
                or math.inf if the travel is not possible.
        """
        distance = departure.distance(arrival)
        if distance <= self.max_distance:
            return math.ceil(self.travel_time)
        else:
            return math.inf

    def __str__(self) -> str:
        """
        Returns the class name and the parameters of the vehicle in parentheses.
        For example "TeleportingTarteTrolley (5 h | 1000 km)"

        :return: the string representation of the vehicle.
        """
        return f"TeleportingTarteTrolley ({self.travel_time} h | {self.max_distance} km)"

def create_example_vehicles() -> list[Vehicle]:
    """
    Creates 3 examples of vehicles.

    :return: a list of 3 vehicles.
    """
    return [CrappyCrepeCar(200), DiplomacyDonutDinghy(100, 500), TeleportingTarteTrolley(3, 2000)]

if __name__ == "__main__":
    #we create some example cities
    create_example_countries()

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
            for vehicle in vehicles:
                print(f"\t{vehicle.compute_travel_time(from_city, to_city)} hours with {vehicle}.")