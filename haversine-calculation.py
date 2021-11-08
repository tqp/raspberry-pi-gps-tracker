from math import radians, cos, sin, asin, sqrt


def distance(lat1, lat2, lon1, lon2):
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles. Use 6371 for kilometers
    r = 3956

    # calculate the result
    return (c * r)


# driver code
latitude_start = 25.02106526335856
longitude_start = -77.27413545925718

latitude_end = 24.172735304154518
longitude_end = -76.44529962197409

print(distance(latitude_start, latitude_end, longitude_start, longitude_end), "mi")
