import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


cp = 4200 # J/(Kg*C)
area = 0.84 # m2
pyranometer_constant = 1000 / 10.93 # uV/(W/m2)

colnames = ["sn_code", "year", "julian_day", "hhmm", "Tin", "Tout", "I_mV", 
            "flow_l_min","logger_temp", "battery", "Tamb"]


dateparser = lambda a,b,c: pd.to_datetime(''.join([a,b,c]), format='%Y%j%H%M')

df = pd.read_csv("CR10X_final_storage_1.dat", names=colnames, 
                 usecols=[1,2,3,4,5,6,7,10],
                 parse_dates={"datetime":[0,1,2]},
                 date_parser=dateparser,
                 index_col="datetime")

# df = df.tz_localize(tz='Europe/Athens')

# Add 30 sec to duplicate timestamps CHECK if logger can save seconds
df.index = df.index + \
    pd.to_timedelta(df.groupby('datetime').cumcount()*30, unit='s')

df["flow_l_sec"] = df["flow_l_min"] / 60 # convert l/min to l/sec
df["flow_l_h"] = df["flow_l_min"] * 60 # convert l/min to l/hour (for plot)
df["I_W_m2"] = df["I_mV"] * pyranometer_constant
df["Tout_Tin"] = df["Tout"] - df["Tin"]

df["efficiency"] = df["flow_l_sec"] * cp * df["Tout_Tin"] / (df["I_W_m2"] * area)
df["DT_I"] = (df["Tin"] - df["Tamb"]) / df["I_W_m2"]


def plot_efficiency_dt_i():
    plt.plot(df["DT_I"], df["efficiency"], ".")
    plt.axis([0,0.01,0,1])
    plt.ylabel("Efficiency")
    plt.xlabel("(Tin - Tamb) / I")
    plt.show()


def plot_timeseries(cols=[], ylabel=""):
    # If df is timezone-aware converts to UTC
    fig, ax = plt.subplots(figsize=(8,4))
    for col in cols:
        ax.plot(df.index, col, data=df)
    xfmt = mdates.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(xfmt)
    ax.xaxis.set_tick_params(rotation=45)
    plt.xlabel("Local time")
    plt.ylabel(ylabel)
    plt.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0.)
    plt.show()

plot_timeseries(cols=["Tout_Tin"], ylabel="Temperature (°C)")
plot_timeseries(cols=["flow_l_h"], ylabel="Flow (L/hour)")
plot_timeseries(cols=["I_W_m2"], ylabel="Irradiance (W/m2)")
plot_timeseries(cols=["Tin", "Tout", "Tamb"], ylabel="Temperature (°C)")

plot_efficiency_dt_i()