#metropolitan engineering competition 16/11/2024
#anthony golubev

import pandas as pd, numpy as np, math
dataset_pd = pd.read_excel("Anthony-G-2024\MEC2024 Dataset.xlsx", sheet_name="Data")
data = np.array(dataset_pd)

for i in data:
    # change comma separated lat/long coords to array form
    i[4] = i[4].split(",")
    i[5] = i[5].split(",")

drivers = []
riders = []
for i in data:
    if i[3].lower() == "driver":
        drivers.append(i)
    else:
        riders.append(i)
del data




        
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
    return person[11]

def get_riders(gender, smoking, gender_preference):
    out = []
    gender=gender.lower()
    if gender_preference:
        for i in riders:
            if i[2].lower() == gender:
                if i[8] == smoking:
                    out.append(i)
                else:
                    continue
            continue
    else:
        for i in riders:
            if i[8] == smoking:
                if i[9]:
                    if i[2].lower == gender:
                        out.append(i)
                    else:
                        continue
                else:
                    out.append(i)
            else:
                continue
    return out

def get_det_dist(a, b):
    r = 6371 #kilometers
    p = (math.pi)/180
    x1, y1, x2, y2 = float(a[0])*p, float(a[1])*p, float(b[0])*p, float(b[1])*p
    return 2*r*math.asin(math.sqrt(0.5-math.cos(x2-x1)/2+math.cos(x1)*math.cos(x2)*(1-math.cos((y2-y1)))/2))
