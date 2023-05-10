# Herding Sheep

## Setup dependencies

`pip install` the following:

- numpy
- pandas
- matplotlib
- pyexcel

## Run simulation

For sheepdog using Centre Tracking method:
`python main_ct.py num_of_dogs dog_vision_range directory num_of_sheep obstacle_type`

For sheepdog using Farthest Individual Tracking method:
`python main_fit.py num_of_dogs dog_vision_range directory num_of_sheep obstacle_type`

Example:
`python main_ct.py 1 400 output 75 empty`
This would run a simualtion with 1 sheepdog using Centre Tracking method and a vision range of 400, herding 75 sheep in an environment with no obstacles.
The data would be exported into the directory 'output'.

## Render simulation

`python render.py directory n`
Renders the nth simulation in the specified directory

Example:
`python render.py output 001`
Render the first simulation in the directory 'output'.
Note that the run number is expected to be padded to 3 digits with zeroes. Hence run number 1 is '001'

## Calculate metrics

`python get_metrics.py directory`
Calculate the metrics for all runs in the specified directory, and summarises them.

### Collate results into .xlsx workbook

`python collect_results.py`
Supplementary script to collect up the metrics for each test set into an Excel workbook.
Note that this file expects the directories to be structured as 'tracking_method/env_type/num_of_dogs/dog_vision_range' as this is how the shell scripts set them up.
For example: 'ct/h/1dog/100vr' or 'fit/empty/4dog/75vr'