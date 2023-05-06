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

# method folder
for method in methods:
    if os.path.exists(method):
        # env folder
        for env in envs:
            env_folder = os.path.join(method, env)
            if os.path.exists(env_folder):
                table_name = method+"_"+env
                tables[table_name] = []
                header = [" "]
                tables[table_name].append(header)
                # dog folder
                for n_dog in n_dogs:
                    dog_folder = os.path.join(env_folder, n_dog)
                    if os.path.exists(dog_folder):
                        row = [n_dog]
                        # vr folder
                        for vr in dog_vrs:
                            vr_folder = os.path.join(dog_folder, vr)
                            if os.path.exists(vr_folder):
                                if vr not in header:
                                    tables[table_name][0].append(vr)
                                summary = os.path.join(vr_folder, "metrics_summary.csv")
                                if os.path.exists(summary):
                                    # print(summary)
                                    #* read csv
                                    data = pd.read_csv(summary)
                                    row.append(data["success_rate"].iloc[0])
                                
                                
                        tables[table_name].append(row)
                                
                
                            
      
      
# print(tables)

# for line in tables["fit_empty"]:
#     print(line)
      
pyexcel.save_book_as(bookdict=tables, dest_file_name="metrics_summary.xlsx")