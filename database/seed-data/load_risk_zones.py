"""Load risk zone GeoJSON features into PostgreSQL/PostGIS without GDAL."""

from __future__ import annotations

import json
import os
from pathlib import Path

import psycopg2


def main() -> None:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is required.")

    data_path = Path(__file__).parent / "output" / "risk_zones.geojson"
    payload = json.loads(data_path.read_text(encoding="utf-8"))
    features = payload.get("features", [])

    inserted_count = 0

    with psycopg2.connect(database_url) as connection:
        with connection.cursor() as cursor:
            for feature in features:
                properties = feature["properties"]
                geometry_json = json.dumps(feature["geometry"])

                cursor.execute(
                    """
                    INSERT INTO risk_zones (id, code, name, hazard_type, severity, geom)
                    VALUES (
                        %s::uuid,
                        %s,
                        %s,
                        %s,
                        %s,
                        ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326)
                    )
                    ON CONFLICT (id) DO NOTHING
                    """,
                    (
                        properties["id"],
                        properties["code"],
                        properties["name"],
                        properties["hazard_type"],
                        properties["severity"],
                        geometry_json,
                    ),
                )
                inserted_count += cursor.rowcount

    print(f"Inserted {inserted_count} risk_zones rows.")


if __name__ == "__main__":
    main()
