import requests
import random
import time
import math
from datetime import datetime

# Updated to your explicit project database URL
DATABASE_URL = "https://hotel-c4382-default-rtdb.firebaseio.com"

# Total targeted uploads parameter (e.g., 8760 hours = 1 year of hourly data)
TOTAL_UPLOADS = 8760 

# Step counter used to calculate smooth continuous angles for the wave graphs
step_angle = 0.0

# Initialize rain accumulation variable
rainToday = 0.0

# -------------------------------------------------------------
# BASELINES SYSTEM REFERENCE VALUES
# -------------------------------------------------------------
baselines = {
    "temperature": 30.0,   # Center temperature is 30°C
    "humidity": 60.0,      # Center humidity is 60%
    "pressure": 990.0,     # Center pressure
    "aqi": 120.0,          # Center AQI
    "co2": 550.0,          # Center CO2 ppm
    "soilMoisture": 50.0   # Center Soil Moisture %
}

print(f"================================================================")
print(f"🚀 Initializing Mathematical Wave Telemetry Engine (HOURLY MODE)")
print(f" Target Total Streams: {TOTAL_UPLOADS} Entries (1 per hour)")
print(f" Pattern Type: 24-Hour Diurnal Cycle Waves")
print(f"================================================================")

for i in range(1, TOTAL_UPLOADS + 1):
    
    # 0.2618 radians per step completes 1 full sine wave cycle every 24 steps (24 hours)
    step_angle += 0.2618  
    
    # Calculate a clean wave coefficient shifting continuously between -1.0 and +1.0
    wave = math.sin(step_angle)
    
    # Introduce a tiny bit of micro-fluctuation so it looks realistic but stays on the curve
    noise = random.uniform(-0.02, 0.02)
    adjusted_wave = wave + noise

    # -------------------------------------------------------------
    # GRADUAL UP / GRADUAL DOWN WAVE CALCULATIONS
    # -------------------------------------------------------------
    temperature = round(baselines["temperature"] + (10.0 * adjusted_wave), 2)
    feelsLike = round(temperature + random.uniform(1.0, 3.0), 2)
    
    humidity = int(round(baselines["humidity"] - (30.0 * adjusted_wave)))
    humidity = max(20, min(100, humidity)) 
    
    pressure = int(round(baselines["pressure"] + (10.0 * math.cos(step_angle))))
    dewPoint = round(temperature - ((100 - humidity) / 5.0), 2)
    
    windSpeed = round(abs(baselines["temperature"] * 1.5 * (wave + 1.1)), 2)
    windGust = round(windSpeed * random.uniform(1.1, 1.4), 2)
    
    aqi = int(round(baselines["aqi"] + (70.0 * adjusted_wave)))
    aqi = max(10, aqi)
    pm1 = round(aqi * 0.15, 2)
    pm25 = round(aqi * 0.35, 2)
    pm10 = round(aqi * 0.65, 2)
    
    co2 = int(round(baselines["co2"] + (200 * wave)))
    co = round(0.1 + (aqi * 0.01), 2)
    voc = int(aqi * 1.5)
    no2 = round(random.uniform(0.1, 0.5), 2)
    so2 = round(random.uniform(0.05, 0.3), 2)
    o3 = round(random.uniform(0.1, 0.4), 2)
    
    soilMoisture = int(round(baselines["soilMoisture"] + (20.0 * wave)))
    soilTemperature = round(temperature * 0.85, 2)
    waterTemperature = round(temperature * 0.80, 2)
    waterLevel = round(200.0 + (50.0 * adjusted_wave), 2)
    
    # Adjusted rain math to accumulate realistically over hours
    rainRate = round(max(0.0, 15.0 * wave) if wave > 0.5 else 0.0, 2)
    rainToday = round(max(0.0, rainToday + rainRate) if i > 1 else 0.0, 2)
    if wave < -0.9: 
        rainToday = 0.0 
    
    cloudCover = int(round(50.0 + (50.0 * wave)))
    visibility = int(round(10000 - (7000 * wave)))
    
    solarVoltage = round(max(0.0, 18.0 * wave), 2)
    solarCurrent = round(max(0.0, 4.0 * wave), 2)
    powerConsumption = round(15.0 + (5.0 * random.uniform(-1, 1)), 2)
    
    batteryVoltage = round(4.1 - (0.00001 * i) + (0.05 * max(0.0, wave)), 2)
    batteryVoltage = max(3.3, min(4.2, batteryVoltage))
    battery = int(((batteryVoltage - 3.3) / (4.2 - 3.3)) * 100)
    
    wifiRSSI = int(-60 + (5 * math.sin(step_angle * 2)))
    gsmSignal = int(20 + (3 * math.cos(step_angle)))
    cpuTemperature = round(35.0 + (15.0 * abs(wave)), 2)
    freeRAM = int(180000 + (20000 * math.sin(step_angle)))

    data = {
        "temperature": temperature,
        "feelsLike": feelsLike,
        "humidity": humidity,
        "pressure": pressure,
        "dewPoint": dewPoint,
        "windSpeed": windSpeed,
        "windDirection": random.choice(["N","NE","E","SE","S","SW","W","NW"]),
        "windGust": windGust,
        "rainToday": rainToday,
        "rainRate": rainRate,
        "uvIndex": round(max(0.0, 10.0 * wave), 1),
        "solarRadiation": int(max(0, 1100 * wave)),
        "lightIntensity": int(max(100, 90000 * wave)),
        "aqi": aqi,
        "pm1": pm1,
        "pm25": pm25,
        "pm10": pm10,
        "co2": co2,
        "co": co,
        "voc": voc,
        "no2": no2,
        "so2": so2,
        "o3": o3,
        "soilMoisture": soilMoisture,
        "soilTemperature": soilTemperature,
        "waterTemperature": waterTemperature,
        "waterLevel": waterLevel,
        "cloudCover": cloudCover,
        "visibility": visibility,
        "battery": battery,
        "batteryVoltage": batteryVoltage,
        "solarVoltage": solarVoltage,
        "solarCurrent": solarCurrent,
        "powerConsumption": powerConsumption,
        "wifiRSSI": wifiRSSI,
        "gsmSignal": gsmSignal,
        "latitude": 13.0827,
        "longitude": 80.2707,
        "altitude": 10.0,
        "gpsSpeed": 0.0,
        "cpuTemperature": cpuTemperature,
        "freeRAM": freeRAM,
        "uptime": i * 60, # Uptime tracked in minutes now (1 hour = 60 mins)
        "restartCount": 0,
        "weather": "Rain" if wave > 0.5 else ("Cloudy" if wave > 0.0 else "Sunny"),
        "alert": "Heavy Rain" if wave > 0.8 else ("Poor Air Quality" if aqi > 170 else "No Alert"),
        "stationName": "Wave Simulation BaseStation Alpha",
        "status": "Online",
        "lastUpdate": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        response = requests.post(
            f"{DATABASE_URL}/weatherStation/logs.json",
            json=data,
            timeout=10
        )

        if response.status_code == 200:
            print(f"📈 [{i}/{TOTAL_UPLOADS}] Hourly Wave Success | Temp: {data['temperature']}°C | Hum: {data['humidity']}% | CO2: {data['co2']}ppm")
        else:
            print(f"❌ [{i}/{TOTAL_UPLOADS}] Sync Failed | Status: {response.status_code}")

    except Exception as e:
        print(f"⚠️ [{i}/{TOTAL_UPLOADS}] Connection Error Instance: {e}")

    # 1 hour spacing interval loop sequence (3600 seconds)
    time.sleep(3600)

print("\n🏁 Wave tracking compilation complete.")
