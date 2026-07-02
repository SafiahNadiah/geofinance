"""
GeoFinance - synthetic seed data generator
==================================================

Generates realistic-but-fake data for local development and demos:
  - branches.csv     18 bank branches across the Klang Valley
  - customers.csv    2,000 customers with home coordinates
  - properties.csv   1,200 properties (linked to customers) with geometry
  - loans.csv        900 loans (linked to customers, properties, branches)
  - risk_zones.geojson   12 synthetic flood/hazard risk polygons

IMPORTANT: All personal data (names, ICs, phone numbers, addresses) is
FAKE, generated with the `Faker` library. Branch coordinates are
approximate real-world locations (for realistic map demos); everything
else — customers, loans, properties, risk zones — is entirely synthetic
and does not represent real people, accounts, or hazard assessments.

Usage:
    python generate_seed_data.py
Output written to ./output/
"""

import csv
import json
import random
from pathlib import Path
from uuid import uuid4

from faker import Faker

random.seed(42)
fake = Faker()
Faker.seed(42)

OUT_DIR = Path(__file__).parent / "output"
OUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Branches — approximate real Klang Valley town centers (illustrative
#    coordinates for demo purposes, not sourced from any bank's actual
#    branch list)
# ---------------------------------------------------------------------------
BRANCH_AREAS = [
    ("KL City Centre", 3.1579, 101.7116),
    ("Bangsar", 3.1290, 101.6710),
    ("Cheras", 3.1073, 101.7440),
    ("Ampang", 3.1487, 101.7620),
    ("Petaling Jaya Old Town", 3.1073, 101.6413),
    ("Damansara Utama", 3.1360, 101.6230),
    ("Subang Jaya", 3.0567, 101.5851),
    ("Shah Alam", 3.0733, 101.5185),
    ("Klang", 3.0449, 101.4455),
    ("Puchong", 3.0219, 101.6183),
    ("Kajang", 2.9931, 101.7874),
    ("Bangi", 2.9161, 101.7861),
    ("Cyberjaya", 2.9213, 101.6559),
    ("Wangsa Maju", 3.2041, 101.7294),
    ("Setapak", 3.1930, 101.7213),
    ("Sungai Buloh", 3.2033, 101.5802),
    ("Semenyih", 2.9497, 101.8434),
    ("Rawang", 3.3175, 101.5764),
]

BRANCH_TYPES = ["main_branch", "retail_branch", "sme_centre", "priority_banking"]


def jitter(lat, lng, radius_km=2.5):
    """Random point within ~radius_km of a center point."""
    dlat = random.uniform(-1, 1) * (radius_km / 111.0)
    dlng = random.uniform(-1, 1) * (radius_km / (111.0 * 0.86))  # approx at this latitude
    return round(lat + dlat, 6), round(lng + dlng, 6)


def point_ewkt(lat, lng):
    return f"SRID=4326;POINT({lng} {lat})"


branches = []
for i, (name, lat, lng) in enumerate(BRANCH_AREAS, start=1):
    branches.append({
        "id": str(uuid4()),
        "code": f"BR{i:03d}",
        "name": f"{name} Branch",
        "type": random.choice(BRANCH_TYPES),
        "address": f"{fake.building_number()}, Jalan {fake.last_name()}, {name}, Selangor",
        "geom": point_ewkt(lat, lng),
        "opened_date": fake.date_between(start_date="-15y", end_date="-1y").isoformat(),
        "staff_count": random.randint(8, 45),
        "_latitude": lat,
        "_longitude": lng,
    })

with open(OUT_DIR / "branches.csv", "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "id",
            "code",
            "name",
            "type",
            "address",
            "geom",
            "opened_date",
            "staff_count",
        ],
        extrasaction="ignore",
    )
    writer.writeheader()
    writer.writerows(branches)

# ---------------------------------------------------------------------------
# 2. Customers — fake identities clustered near branches
# ---------------------------------------------------------------------------
MALAY_FIRST = ["Ahmad", "Muhammad", "Siti", "Nur", "Aiman", "Farah", "Amir", "Aina",
               "Hafiz", "Zulaikha", "Iskandar", "Nabila", "Danish", "Alya", "Haziq"]
MALAY_LAST = ["Abdullah", "Rahman", "Ismail", "Hassan", "Yusof", "Kamal", "Ibrahim", "Bakar"]
CHINESE_FIRST = ["Wei Ling", "Jia Hao", "Mei Chen", "Zhi Hao", "Xin Yi", "Kai Xuan",
                  "Yi Xuan", "Cheng Wei", "Hui Min", "Jun Wei"]
CHINESE_LAST = ["Tan", "Lim", "Lee", "Wong", "Ng", "Chong", "Ong", "Chan", "Goh", "Teh"]
INDIAN_FIRST = ["Kumar", "Priya", "Ravi", "Deepa", "Suresh", "Anitha", "Vikram",
                 "Kavitha", "Naveen", "Shalini"]
INDIAN_LAST = ["a/l Muthu", "a/p Raman", "a/l Krishnan", "a/p Suppiah", "a/l Naidu",
               "a/p Govindasamy"]

NAME_POOLS = [
    (MALAY_FIRST, MALAY_LAST),
    (CHINESE_FIRST, CHINESE_LAST),
    (INDIAN_FIRST, INDIAN_LAST),
]

OCCUPATIONS = ["Software Engineer", "Teacher", "Nurse", "Accountant", "Business Owner",
               "Sales Executive", "Civil Servant", "Architect", "Doctor", "Lawyer",
               "Freelancer", "Retail Manager", "Engineer", "Consultant"]

N_CUSTOMERS = 2000
customers = []
for i in range(1, N_CUSTOMERS + 1):
    first_pool, last_pool = random.choice(NAME_POOLS)
    name = f"{random.choice(first_pool)} {random.choice(last_pool)}"
    branch = random.choice(branches)
    lat, lng = jitter(branch["_latitude"], branch["_longitude"], radius_km=6)
    dob = fake.date_of_birth(minimum_age=21, maximum_age=70)
    customers.append({
        "id": str(uuid4()),
        "code": f"CUST{i:05d}",
        "full_name": name,
        "email": fake.unique.email(),
        "phone": f"+601{random.randint(0,9)}-{random.randint(1000000,9999999)}",
        "occupation": random.choice(OCCUPATIONS),
        "monthly_income_myr": random.choice([
            round(random.uniform(2500, 4500), 2),
            round(random.uniform(4500, 8000), 2),
            round(random.uniform(8000, 20000), 2),
        ]),
        "home_geom": point_ewkt(lat, lng),
        "nearest_branch_id": branch["id"],
        "customer_since": fake.date_between(start_date="-10y", end_date="today").isoformat(),
        "_home_latitude": lat,
        "_home_longitude": lng,
    })

with open(OUT_DIR / "customers.csv", "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "id",
            "code",
            "full_name",
            "email",
            "phone",
            "occupation",
            "monthly_income_myr",
            "home_geom",
            "nearest_branch_id",
            "customer_since",
        ],
        extrasaction="ignore",
    )
    writer.writeheader()
    writer.writerows(customers)

# ---------------------------------------------------------------------------
# 3. Properties — linked to a subset of customers
# ---------------------------------------------------------------------------
PROPERTY_TYPES = ["terrace_house", "condominium", "apartment", "semi_detached", "bungalow", "shop_lot"]

N_PROPERTIES = 1200
property_customers = random.sample(customers, N_PROPERTIES)
properties = []
for i, cust in enumerate(property_customers, start=1):
    lat, lng = jitter(cust["_home_latitude"], cust["_home_longitude"], radius_km=1.5)
    ptype = random.choice(PROPERTY_TYPES)
    base_value = {
        "terrace_house": (350000, 750000),
        "condominium": (300000, 900000),
        "apartment": (180000, 450000),
        "semi_detached": (700000, 1600000),
        "bungalow": (1200000, 3500000),
        "shop_lot": (500000, 2000000),
    }[ptype]
    properties.append({
        "id": str(uuid4()),
        "code": f"PROP{i:05d}",
        "owner_customer_id": cust["id"],
        "type": ptype,
        "address": f"{fake.building_number()}, Jalan {fake.street_name()}, {fake.city()}, Selangor",
        "geom": point_ewkt(lat, lng),
        "market_value_myr": round(random.uniform(*base_value), 2),
        "floor_area_sqft": random.randint(600, 4500),
        "year_built": random.randint(1985, 2023),
        "_latitude": lat,
        "_longitude": lng,
    })

with open(OUT_DIR / "properties.csv", "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "id",
            "code",
            "owner_customer_id",
            "type",
            "address",
            "geom",
            "market_value_myr",
            "floor_area_sqft",
            "year_built",
        ],
        extrasaction="ignore",
    )
    writer.writeheader()
    writer.writerows(properties)

# ---------------------------------------------------------------------------
# 4. Risk zones (synthetic flood/hazard polygons) — for spatial risk demo
#    These are illustrative shapes only, NOT sourced from any real hazard
#    map or NAHRIM/DID flood data.
# ---------------------------------------------------------------------------
RISK_ZONE_CENTERS = [
    ("Klang riverside", 3.0449, 101.4455, "flood", "high"),
    ("Shah Alam lowland", 3.0733, 101.5100, "flood", "medium"),
    ("Kajang stream basin", 2.9931, 101.7900, "flood", "medium"),
    ("Cheras drainage basin", 3.0980, 101.7500, "flood", "low"),
    ("Puchong industrial zone", 3.0150, 101.6100, "landslide", "low"),
    ("Ampang hillside", 3.1550, 101.7700, "landslide", "high"),
    ("Sungai Buloh floodplain", 3.2000, 101.5700, "flood", "medium"),
    ("Rawang lowland", 3.3175, 101.5764, "flood", "low"),
    ("Semenyih catchment", 2.9497, 101.8434, "flood", "medium"),
    ("Subang Jaya urban drain", 3.0567, 101.5851, "flood", "low"),
    ("Bangi highland", 2.9161, 101.7861, "landslide", "low"),
    ("Wangsa Maju basin", 3.2041, 101.7294, "flood", "medium"),
]


def square_polygon(lat, lng, size_km=1.2):
    d = size_km / 111.0
    return [
        [lng - d, lat - d],
        [lng + d, lat - d],
        [lng + d, lat + d],
        [lng - d, lat + d],
        [lng - d, lat - d],
    ]


features = []
for i, (name, lat, lng, hazard, severity) in enumerate(RISK_ZONE_CENTERS, start=1):
    features.append({
        "type": "Feature",
        "properties": {
            "id": str(uuid4()),
            "code": f"RZ{i:03d}",
            "name": name,
            "hazard_type": hazard,
            "severity": severity,
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [square_polygon(lat, lng)],
        },
    })

risk_geojson = {"type": "FeatureCollection", "features": features}
with open(OUT_DIR / "risk_zones.geojson", "w") as f:
    json.dump(risk_geojson, f, indent=2)

# ---------------------------------------------------------------------------
# 5. Loans — linked to customers, a subset of their properties, and branch
# ---------------------------------------------------------------------------
LOAN_TYPES = ["home_loan", "personal_loan", "sme_business_loan", "auto_loan", "renovation_loan"]
LOAN_STATUS = ["active", "active", "active", "pending_approval", "closed", "defaulted"]


def haversine_km(lat1, lng1, lat2, lng2):
    from math import radians, sin, cos, sqrt, atan2
    r = 6371
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
    return 2 * r * atan2(sqrt(a), sqrt(1 - a))


def nearest_risk_zone(lat, lng):
    best, best_d = None, 999
    for name, zlat, zlng, hazard, severity in RISK_ZONE_CENTERS:
        d = haversine_km(lat, lng, zlat, zlng)
        if d < best_d:
            best, best_d = (name, hazard, severity), d
    return best, best_d


N_LOANS = 900
loan_properties = random.sample(properties, N_LOANS)
loans = []
customers_by_id = {customer["id"]: customer for customer in customers}
for i, prop in enumerate(loan_properties, start=1):
    cust = customers_by_id[prop["owner_customer_id"]]
    branch_id = cust["nearest_branch_id"]
    (_, _, severity), dist_km = nearest_risk_zone(prop["_latitude"], prop["_longitude"])

    # simple synthetic risk score: closer to a risk zone + higher severity + lower income => higher risk
    severity_weight = {"low": 1, "medium": 2, "high": 3}[severity]
    proximity_score = max(0, 5 - dist_km) * severity_weight
    income_score = max(0, 3 - (cust["monthly_income_myr"] / 5000))
    risk_score = round(min(100, proximity_score * 8 + income_score * 10 + random.uniform(0, 15)), 1)
    risk_tier = "high" if risk_score >= 55 else "medium" if risk_score >= 30 else "low"

    loans.append({
        "id": str(uuid4()),
        "code": f"LN{i:05d}",
        "customer_id": cust["id"],
        "property_id": prop["id"],
        "branch_id": branch_id,
        "loan_type": random.choice(LOAN_TYPES),
        "principal_amount_myr": round(prop["market_value_myr"] * random.uniform(0.5, 0.9), 2),
        "interest_rate_pct": round(random.uniform(3.5, 7.5), 2),
        "tenure_years": random.choice([5, 10, 15, 20, 25, 30]),
        "status": random.choice(LOAN_STATUS),
        "application_date": fake.date_between(start_date="-6y", end_date="today").isoformat(),
        "_distance_to_risk_zone_km": round(dist_km, 2),
        "_risk_score": risk_score,
        "_risk_tier": risk_tier,
    })

with open(OUT_DIR / "loans.csv", "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "id",
            "code",
            "customer_id",
            "property_id",
            "branch_id",
            "loan_type",
            "principal_amount_myr",
            "interest_rate_pct",
            "tenure_years",
            "status",
            "application_date",
        ],
        extrasaction="ignore",
    )
    writer.writeheader()
    writer.writerows(loans)

print(f"Generated {len(branches)} branches, {len(customers)} customers, "
      f"{len(properties)} properties, {len(loans)} loans, "
      f"{len(features)} risk zones -> {OUT_DIR}")
