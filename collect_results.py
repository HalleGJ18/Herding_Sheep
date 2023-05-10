import os
import pathlib
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import pyexcel

methods = ["ct", "fit"]
envs = ["empty", "m", "f", "h"]
n_dogs = ["1dog", "2dog", "3dog", "4dog", "5dog"]
dog_vrs = ["50vr", "75vr", "100vr", "125vr", "150vr", "175vr","200vr", "250vr", "300vr", "350vr", "400vr"]

tables = dict()

try:
    root = sys.argv[1]
except:
    root = ""

# tables_times = dict()

# method folder
for method in methods:
    if len(root) > 0:
        folder = os.path.join(root, method)
    else:
        folder = method
    if os.path.exists(folder):
        # env folder
        for env in envs:
            env_folder = os.path.join(folder, env)
            if os.path.exists(env_folder):
                table_name = method+"_"+env+"_rate"
                table_name2 = method+"_"+env+"_time"
                table_name3 = method+"_"+env+"_dist_from_gcm"
                
                tables[table_name] = []
                tables[table_name2] = []
                tables[table_name3] = []
                
                tables[table_name].append([" "])
                tables[table_name][0] += dog_vrs
                
                tables[table_name2].append([" "])
                tables[table_name2][0] += dog_vrs
                
                tables[table_name3].append([" "])
                tables[table_name3][0] += dog_vrs
                # dog folder
                for n_dog in n_dogs:
                    dog_folder = os.path.join(env_folder, n_dog)
                    if os.path.exists(dog_folder):
                        row = [n_dog]
                        row2 = [n_dog]
                        row3 = [n_dog]
                        # vr folder
                        for vr in dog_vrs:
                            vr_folder = os.path.join(dog_folder, vr)
                            if os.path.exists(vr_folder):
                                # if vr not in tables[table_name][0]:
                                #     tables[table_name][0].append(vr)
                                #     tables[table_name2][0].append(vr)
                                summary = os.path.join(vr_folder, "metrics_summary.csv")
                                if os.path.exists(summary):
                                    print(summary)
                                    #* read csv
                                    data = pd.read_csv(summary)
                                    row.append(data["success_rate"].iloc[0])
                                    row2.append(data["success_avg_time"].iloc[0])
                                    row3.append(data['avg_from_gcm'].iloc[0])
                                else:
                                    row.append(" ")
                                    row2.append(" ")
                                    row3.append(" ")
                            else:
                                row.append(" ")
                                row2.append(" ")
                                row3.append(" ")
                                
                                
                        tables[table_name].append(row)
                        tables[table_name2].append(row2)
                        tables[table_name3].append(row3)
                                
                
                            
      
      
# print(tables)

# for line in tables["fit_empty"]:
#     print(line)
if len(root) > 0:
    pyexcel.save_book_as(bookdict=tables, dest_file_name="metrics_summary_"+root+".xlsx")
else:
    pyexcel.save_book_as(bookdict=tables, dest_file_name="metrics_summary.xlsx")
# pyexcel.save_book_as(bookdict=tables_times, dest_file_name="success_times_summary.xlsx")