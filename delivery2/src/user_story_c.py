import sqlite3
from datetime import datetime
from constants import con

cursor = con.cursor()

def get_train_route(railway_station: str, weekday: str) -> list:
    weekdays = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    while weekday not in weekdays:
        weekday = input("Please enter a valid weekday or [q]uit: ")
        if weekday == "q":
            return

    valid_stations = [
        "Trondheim",
        "Steinkjer",
        "Mosjøen",
        "Mo i Rana",
        "Fauske",
        "Bodø",
    ]

    while railway_station not in valid_stations:
        railway_station = input("Please enter a valid station or [q]uit: ")
        if railway_station == "q":
            return

    valid_routes = []
    cleaned_info = []

    train_routes = cursor.execute(
        """SELECT DISTINCT TrainRoute.TrainRouteID, TrainRoute.Direction, TrainOccurence.RouteDate, TrackSection.StartStation, TrackSection.EndStation FROM TrainRoute
        LEFT JOIN TrainOccurence ON TrainOccurence.RouteID = TrainRoute.TrainRouteID
        LEFT JOIN TrackSection ON TrainRoute.TrackID = TrackSection.TrackID
        LEFT JOIN HasSubsection ON TrackSection.TrackID = HasSubsection.TrackID
        LEFT JOIN Subsection ON HasSubsection.SubsectionID = Subsection.SubsectionID
        WHERE Subsection.StartStation = ? OR TrackSection.EndStation = ?""",
        (railway_station, railway_station),
    )

    for route in train_routes:
        date = datetime.strptime(route[2], "%Y-%m-%d")
        if date.weekday() == weekdays.index(weekday.capitalize()):
            valid_routes.append(route)

    for route in valid_routes:
        if route[1] == 1:
            list_route = list(route)
            cleaned_reversed_direction = [
                list_route[0],
                list_route[2],
                list_route[4],
                list_route[3],
            ]
            cleaned_info.append(cleaned_reversed_direction)
        else:
            list_route = list(route)
            list_route.remove(list_route[1])
            cleaned_info.append(list_route)

    try:
        date = datetime.strptime(cleaned_info[0][1], "%Y-%m-%d")
    except:
        print("No routes found")
        return
    print(f"{weekdays[date.weekday()]} - {date}")
    for route in cleaned_info:
        print(f"Route {route[0]}: {route[2]} - {route[3]}")
    return cleaned_info
