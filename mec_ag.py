#metropolitan engineering competition 16/11/2024
#anthony golubev

import pandas as pd, numpy as np, math, datetime
dataset_pd = pd.read_excel("Anthony-G-2024\MEC2024 Dataset.xlsx", sheet_name="Data")
data = np.array(dataset_pd)

for person in data:
    # Change comma separated lat/long coords to array form
    person[4] = person[4].split(",")
    person[5] = person[5].split(",")
    obj = person[6]
    person[6] = datetime.datetime(1, 1, 1, obj.hour, obj.minute, obj.second)

# Separate the drivers and riders
drivers = []
riders = []
for person in data:
    if person[3].lower() == "driver":
        drivers.append(person)
    else:
        riders.append(person)
del data


# Create getters to retrieve a person's attributes
def get_user_id(person):
    return person[0]
def get_user_name(person):
    return person[1]
def get_gender(person):
    return person[2]
def get_start_lat(person):
    return person[4][0]
def get_start_long(person):
    return person[4][1]
def get_end_lat(person):
    return person[5][0]
def get_end_long(person):
    return person[5][1]
def get_start_time(person):
    return person[6]
def get_detour_dist(person):
    return person[7]
def get_smoking(person):
    return person[8]
def get_gender_pref(person):
    return person[9]
def get_group_size(person):
    return person[10]
def get_seat_num(person):
    return int(person[11])


# Filter riders by driver's constraints
def get_riders(gender, smoking, gender_preference, leave_time):
    out = []
    gender=gender.lower()
    
    if gender_preference:
        for rider in riders:
            if not abs((get_start_time(rider)-leave_time).total_seconds()) <= 20*60:
                continue
            if not get_gender(rider).lower() == gender:
                continue
            if not get_smoking(rider) == smoking:
                continue
            out.append(rider)
    else:
        for rider in riders:
            if not abs((get_start_time(rider)-leave_time).total_seconds()) <= 20*60:
                continue
            if not get_smoking(rider) == smoking:
                continue
            if get_gender_pref(rider):
                if get_gender(rider).lower == gender:
                    out.append(rider)
            else:
                out.append(rider)
    return out


# Calculate distance between two locations based on lat/long
def get_dist(a, b):
    r = 6371 #kilometers
    p = (math.pi)/180
    x1, y1, x2, y2 = float(a[0])*p, float(a[1])*p, float(b[0])*p, float(b[1])*p
    return 2*r*math.asin(math.sqrt(0.5-math.cos(x2-x1)/2+math.cos(x1)*math.cos(x2)*(1-math.cos((y2-y1)))/2))

# Calculate the deviation between two journeys
def GetDeviation(initial, secondary):
    start_1 = initial[4]
    start_2 = secondary[4]
    end_1 = initial[5]
    end_2 = secondary[5]
    return (get_dist(start_1, start_2)+get_dist(start_2, end_2)+get_dist(end_2, end_1)-get_dist(start_1, end_1))


# Compute the route for a driver given the possible riders
def ComputeDriverGrouping(driver, riders, totalVisited):
    route = [driver]
    capacity = get_seat_num(driver)
   
    visited = set()
   
    # Find N people to ride in the driver's car
    for i in range(capacity):
        # Find the rider with minimum deviation
        minDev = float('inf')
        minRider = -1
        for j in range(len(riders)):
            if j in visited or j in totalVisited:
                continue
            dev = GetDeviation(route[-1], riders[j])
            if dev < minDev:
                minDev = dev
                minRider = j
            if minRider == -1:
                break
        if minRider == -1:
            break


        # Add the rider with minimum deviation to the route
        visited.add(minRider)
        route.append(riders[minRider])
   
    # Route goes s1, s2, s3 ... e3, e2, e1
    # Check if the route satisfies max deviation constraints
    # If it fails, remove riders from the route until it succeeds
    totalDev = 0
    for i in range(len(route)-1):
        totalDev += GetDeviation(route[i], route[i+1])
        if totalDev > get_detour_dist(route[i]):
            route = route[:i+1]
            break
   
    totalVisited = totalVisited.union(visited)
    return(route[:], totalVisited)


# Find groupings for each driver, minimizing deviation for each rider
def ComputeGroupings(drivers, riders):
    totalVisited = set()
    routes = []
    for driver in drivers:
        # Filter the riders and calculate the best route for each driver
        filteredRiders = get_riders(get_gender(driver), get_smoking(driver), get_gender_pref(driver), get_start_time(driver))
        route, totalVisited = ComputeDriverGrouping(driver, filteredRiders, totalVisited)
        routes.append(route)
    return routes

user_id = "Juan Lewis"
groupings = ComputeGroupings(drivers, riders)
out = "No group found"
for group in groupings:
    for person in group:
        if get_user_name(person) == user_id:
            output = group[:]
print(output)
