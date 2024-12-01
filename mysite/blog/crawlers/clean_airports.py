import json
import os


def clean_airports():
    with open(".\\data\\airports2.json") as f:
        airports = json.load(f)

    print(f"Total airports: {len(airports)}")
    clean_airports = []
    for key, airport in airports.items():
        if not airport["iata"]:
            continue
        clean_airports.append(
            {
                "name": airport["name"],
                "city": airport["city"],
                "state": airport["state"],
                "country": airport["country"],
                "iata": airport["iata"],
            }
        )

    print(f"Cleaned airports: {len(clean_airports)}")
    with open("airports_cleaned.json", "w") as f:
        json.dump(clean_airports, f)


clean_airports()
