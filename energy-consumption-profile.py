#Define a 30day timeline

import pandas as pd
import requests

start_date = "2026-08-01"
periods = 30 * 24  # 30 days of hourly data
end_date = (
    pd.Timestamp(start_date)
    + pd.Timedelta(hours=periods - 1)
).strftime("%Y-%m-%d")

df = pd.DataFrame({
    'timestamp': pd.date_range(start=start_date, periods=periods, freq='h'),
})

df["hour"] = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.dayofweek
df["is_weekend"] = df["day_of_week"] >= 5

# print(len(df))

url = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": 38.72,
    "longitude": -9.14,
    "start_date": start_date,
    "end_date": end_date,
    "hourly": [
        "temperature_2m",
        "relative_humidity_2m",
        "cloud_cover",
        "shortwave_radiation"
    ],
    "timezone": "Europe/Lisbon"
}

response = requests.get(url, params=params)
data = response.json()

weather_df = pd.DataFrame({
    "timestamp": pd.to_datetime(data["hourly"]["time"]),
    "temperature": data["hourly"]["temperature_2m"],
    "humidity": data["hourly"]["relative_humidity_2m"],
    "cloud_cover": data["hourly"]["cloud_cover"],
    "solar_radiation": data["hourly"]["shortwave_radiation"]
})

# print(weather_df.head())

# merge the weather with your household data
df = df.merge(
    weather_df,
    on="timestamp",
    how="left"
)

print(df.head())

# check there are no missing values
# print(df.isnull().sum())
print(df.shape)

# visualize the temperature data to make sure it looks reasonable

import matplotlib.pyplot as plt

plt.figure(figsize=(14, 5))

plt.plot(
    df["timestamp"],
    df["temperature"]
)

plt.xlabel("Date")
plt.ylabel("Outdoor temperature (°C)")
plt.title("Historical Outdoor Temperature - Lisbon")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
