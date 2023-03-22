import sqlite3
from datetime import datetime

con = sqlite3.connect("trainDB.db")
cursor = con.cursor()


def get_train_route(railway_station, weekday):
    weekdays = ['Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday', 'Sunday']

    valid_routes = []

    train_routes = cursor.execute(
        """SELECT TrainRoute.TrainRouteID, TrainOccurence.RouteDate FROM TrainRoute
        OUTER JOIN TrainOccurence ON TrainOccurence.RouteID = TrainRoute.TrainRouteID
        LEFT JOIN TrackSection ON TrainRoute.TrackID = TrackSection.TrackID 
        LEFT JOIN HasSubsection ON TrackSection.TrackID = HasSubsection.TrackID
        LEFT JOIN Subsection ON HasSubsection.SubsectionID = Subsection.SubsectionID
        WHERE Subsection.StartStation = ? OR TrackSection.EndStation = ?""", (railway_station, railway_station))

    for route in train_routes:
        date = datetime.strptime(route[1], "%Y-%m-%d")
        if date.weekday() == weekdays.index(weekday):
            valid_routes.append(route)

    return valid_routes
