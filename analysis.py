import pandas as pd

colnames = ["sn_code", "year", "julian_day", "hhmm", "Tin", "Tout", "I_mV", 
            "flow","logger_temp", "battery", "Tamb"]

df = pd.read_csv("CR10X_final_storage_1.dat", names=colnames, 
                 usecols=[1,2,3,4,5,6,7,10],
                 parse_dates=True)

