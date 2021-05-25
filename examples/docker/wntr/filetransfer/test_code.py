# %% IMPORTS

import argparse
import time
import pandas as pd

# %%

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--node_name', type=str, required=True)
    args = parser.parse_args()

    csv_filename = './' + args.node_name + '.csv'
    pressure_data = pd.read_csv(csv_filename)
    cols = list(pressure_data.columns)
    pressure_data.rename(columns={cols[0]: 'time', cols[1]: 'P'}, inplace=True)
    for i, sensor_reading in pressure_data.iterrows():
        print('Pressure at timestamp ' + str(sensor_reading.time) + ' with processing time ' + str(
            time.localtime()) + ' is ' + str(sensor_reading.P) + '.')
        time_to_next_reading = pressure_data.iloc[i + 1] - sensor_reading.between_time
        time.sleep(time_to_next_reading)
