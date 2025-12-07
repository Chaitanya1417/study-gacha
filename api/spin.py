import json
import math
import random

HYDERABAD = (17.3850, 78.4867)
CRUISE_SPEED_KMH = 900.0

CITIES = {
    "New York, USA": [40.7128, -74.0060],
    "London, UK": [51.5074, -0.1278],
    "Paris, France": [48.8566, 2.3522],
    "Tokyo, Japan": [35.6762, 139.6503],
    "Sydney, Australia": [-33.8688, 151.2093],
    "Dubai, UAE": [25.2048, 55.2708],
    "Singapore": [1.3521, 103.8198],
    "Los Angeles, USA": [34.0522, -118.2437],
    "Toronto, Canada": [43.6532, -79.3832],
    "Beijing, China": [39.9042, 116.4074],
    "Seoul, South Korea": [37.5665, 126.9780],
    "Bangkok, Thailand": [13.7563, 100.5018],
    "Istanbul, Turkey": [41.0082, 28.9784],
    "Cairo, Egypt": [30.0444, 31.2357],
    "Johannesburg, South Africa": [-26.2041, 28.0473],
    "Nairobi, Kenya": [-1.2921, 36.8219],
    "Moscow, Russia": [55.7558, 37.6173],
    "Berlin, Germany": [52.52, 13.405],
    "Madrid, Spain": [40.4168, -3.7038],
    "Rome, Italy": [41.9028, 12.4964],
    "Amsterdam, Netherlands": [52.3676, 4.9041],
    "Lisbon, Portugal": [38.7223, -9.1393],
    "Zurich, Switzerland": [47.3769, 8.5417],
    "Vienna, Austria": [48.2082, 16.3738],
    "Melbourne, Australia": [-37.8136, 144.9631],
    "Vancouver, Canada": [49.2827, -123.1207],
    "Mexico City, Mexico": [19.4326, -99.1332],
    "São Paulo, Brazil": [-23.5505, -46.6333],
    "Buenos Aires, Argentina": [-34.6037, -58.3816],
    "Honolulu, USA": [21.3069, -157.8583],
    "Reykjavik, Iceland": [64.1466, -21.9426],
    "Athens, Greece": [37.9838, 23.7275],
    "Prague, Czechia": [50.0755, 14.4378],
    "Kuala Lumpur, Malaysia": [3.1390, 101.6869],
    "Manila, Philippines": [14.5995, 120.9842],
    "Casablanca, Morocco": [33.5731, -7.5898],
    "Lagos, Nigeria": [6.5244, 3.3792],
}


# Haversine formula: distance between 2 lat/lon points
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# Required by Vercel → this function runs when /api/spin is called
def handler(request):
    # pick a random city
    name = random.choice(list(CITIES.keys()))
    lat, lon = CITIES[name]

    # compute distance
    dist = haversine_km(HYDERABAD[0], HYDERABAD[1], lat, lon)

    # compute time estimate
    est_hours = dist / CRUISE_SPEED_KMH
    hrs = int(est_hours)
    mins = int(round((est_hours - hrs) * 60))

    response = {
        "city": name,
        "distance_km": round(dist, 1),
        "flight_time": f"{hrs}h {mins}m",
    }

    # Vercel requires body as a JSON string
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(response),
    }
