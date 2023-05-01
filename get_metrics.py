import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import math
import os
import sys


""" helper functions """
# format string into np array of floats
def format(row):
  row = row[1:]
  row = row[:-1]
  row = row.split()
  row = [float(x) for x in row]
  # print(type(row))
  # print(row)
  return np.array(row)


""" metrics calculations """

""" whole directory """
# overall success rate
def success_rate(outcomes):
    # outcomes is list of True/False values 
    true_count = 0
    false_count = 0
    for x in outcomes:
        if x == True:
            true_count += 1
        else:
            false_count += 1
    print(true_count, false_count)
    success_rate = true_count /(true_count + false_count)
    return success_rate, true_count, false_count


# average time taken for success
def average_time(times):
    # times is array of runtimes of successful tests
    if len(times) > 0:
        avg_time = sum(times)/len(times)
        return avg_time
    else:
        return "DNF"


# avg dist travelled by dog
def avg_dog_dist_travelled(dists):
    avg_dist = sum(dists)/len(dists)
    return avg_dist


""" file by file"""

# flock gcm per timestep
def flock_gcm(x_positions, y_positions):
    avg_x = sum(x_positions)/len(x_positions)
    avg_y = sum(y_positions)/len(y_positions)
    gcm = [avg_x, avg_y]
    return gcm

# average distance of sheep from flock gcm per timestep
def avg_dist_from_gcm(gcm, x_positions, y_positions):
    total_dist = 0
    for i in range(0, len(x_positions)):
        d = math.dist(gcm, [x_positions[i], y_positions[i]])
        total_dist += d
    avg_dist = total_dist/len(x_positions)
    return avg_dist

# furthest sheep from flock gcm per timestep
def furthest_sheep_from_gcm(gcm, x_positions, y_positions):
    furthest_dist = 0
    for i in range(0, len(x_positions)):
        d = math.dist(gcm, [x_positions[i], y_positions[i]])
        if d > furthest_dist:
            furthest_dist = d
    return furthest_dist

# total distance travelled by dog
def dog_dist_travelled(x_pos, y_pos):
    total_dist = 0
    for i in range(1, len(x_pos)):
        d = math.dist([x_pos[1], y_pos[i]], [x_pos[i-1], y_pos[i-1]])
        total_dist += 1
    return total_dist


# load dir

directory = sys.argv[1]
print(f"metrics: {directory}")

# make metrics dir
try:
   os.makedirs(directory+"/metrics")
except FileExistsError:
   # directory already exists
   pass

# collect data

test_outcomes = []
success_times = []


# loop through files in dir
file_num = 1
file_exists = True
while file_exists:
    n =  str(file_num).zfill(3)
    DATA_CSV = directory+"/results/data"+n+".csv"
    ENV_CSV = directory+"/results/env_data"+n+".csv"
    OBS_CSV = directory+"/results/obstacle_data"+n+".csv"
    
    # read files
    if os.path.exists(DATA_CSV):
        data = pd.read_csv(DATA_CSV, sep="|", index_col=0)
        env_data = pd.read_csv(ENV_CSV, sep=",", index_col=0)
        if os.path.exists(OBS_CSV): 
            obs_data = pd.read_csv(OBS_CSV, sep=",", index_col=0)
            
        ENV_HEIGHT = int(env_data.loc[0]['height'])
        ENV_WIDTH = int(env_data.loc[0]['width'])
        
        target = [float(env_data.loc[0]['target_x']), float(env_data.loc[0]['target_y'])]
        target_range = float(env_data.loc[0]['target_range'])
        target_endzone = float(env_data.loc[0]['endzone'])

        success = env_data.loc[0]['success']

        T_LIMIT = len(data.index) - 1
        # print(T_LIMIT)
        
        test_outcomes.append(success)
        if success :
            success_times.append(T_LIMIT)
            
        gcm_list = []
        avg_from_gcm_list = []
        furthest_from_gcm_list = []
                    
        # loop through rows in files
        for row in range(0, T_LIMIT):
            # load row
            sheep_x = format(data.loc[row]["sheep_x_positions"])
            sheep_y = format(data.loc[row]["sheep_y_positions"])
            dog_x = format(data.loc[row]["dog_x_positions"])
            dog_y = format(data.loc[row]["dog_y_positions"])
            
            # calc metrics
            gcm = flock_gcm(sheep_x, sheep_y)
            avg_from_gcm = avg_dist_from_gcm(gcm, sheep_x, sheep_y)
            furthest_from_gcm = furthest_sheep_from_gcm(gcm, sheep_x, sheep_y)
            
            # store metrics
            gcm_list.append(gcm)
            avg_from_gcm_list.append(avg_from_gcm)
            furthest_from_gcm_list.append(furthest_from_gcm)
        
        # output metrics
        m = {'flock_gcm':gcm_list, 'avg_sheep_dist_from_gcm':avg_from_gcm_list, 'furthest_sheep_from_gcm':furthest_from_gcm_list}
        df = pd.DataFrame(data=m)
        df.to_csv(directory+"/metrics/metrics"+n+".csv", encoding='utf-8')
        
        file_num += 1
        
    
    # reached end of files       
    else:
        file_exists = False


print(f"success rate: {success_rate(test_outcomes)}")

print(f"avg success time: {average_time(success_times)}")

sr, tc, fc = success_rate(test_outcomes)

summary = pd.DataFrame(columns=['success_rate', "success_avg_time", 'success_count', 'fail_count', 'total_runs'])
summary.loc[0] = [sr, average_time(success_times), tc, fc, file_num-1]
summary.to_csv(directory+"/metrics_summary.csv", encoding='utf-8', index=False)









