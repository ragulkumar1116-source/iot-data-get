import requests
import random
import time

DATABASE_URL = "https://esp32-projects-9bf7a-default-rtdb.firebaseio.com"

while True:
    data = {
        "temperature": round(random.uniform(25, 35), 2),
        "humidity": round(random.uniform(50, 80), 2),
        "distance": random.randint(10, 200)
    }

    response = requests.patch(f"{DATABASE_URL}/esp32.json", json=data)

    if response.status_code == 200:
        print("Uploaded:", data)
    else:
        print("Upload failed!")
        print(response.text)

    time.sleep(5)
