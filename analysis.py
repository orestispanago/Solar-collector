import pandas as pd
import datetime
import matplotlib.pyplot as plt

cp = 4200 # J/(Kg*C)
area = 0.84 # m2
pyranometer_constant = 1000 / 10.93 # uV/(W/m2)

colnames = ["sn_code", "year", "julian_day", "hhmm", "Tin", "Tout", "I_mV", 
            "flow_l_min","logger_temp", "battery", "Tamb"]


dateparser = lambda a,b,c: datetime.datetime.strptime(' '.join([a,b,c]), '%Y %j %H%M')

df = pd.read_csv("CR10X_final_storage_1.dat", names=colnames, 
                 usecols=[1,2,3,4,5,6,7,10],
                 parse_dates={"datetime":[0,1,2]},
                 date_parser=dateparser,
                 index_col="datetime")

df = df.tz_localize(tz='Europe/Athens')

# convert l/min to l/sec
df["flow_l_h"] = df["flow_l_min"] / 60
df["I_W_m2"] = df["I_mV"] * pyranometer_constant

df["efficiency"] = df["flow_l_h"] * cp * (df["Tout"] - df["Tin"]) / (df["I_W_m2"] * area)
df["dT_I"] = (df["Tin"] - df["Tamb"]) / df["I_W_m2"]


plt.plot(df["dT_I"], df["efficiency"], ".")
plt.axis([0,0.005,0,1])  #this line does the job
plt.show()