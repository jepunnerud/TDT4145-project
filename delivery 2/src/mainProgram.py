import sqlite3
from datetime import datetime

con = sqlite3.connect("trainDB.db")
cursor = con.cursor()


def get_train_route(railway_station, weekday):
    weekdays = ['Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday', 'Sunday']

    valid_routes = []
    cleaned_info = []

    train_routes = cursor.execute(
        """SELECT TrainRoute.TrainRouteID, TrainRoute.Direction, TrainOccurence.RouteDate, TrackSection.StartStation, TrackSection.EndStation FROM TrainRoute
        LEFT JOIN TrainOccurence ON TrainOccurence.RouteID = TrainRoute.TrainRouteID
        LEFT JOIN TrackSection ON TrainRoute.TrackID = TrackSection.TrackID 
        LEFT JOIN HasSubsection ON TrackSection.TrackID = HasSubsection.TrackID
        LEFT JOIN Subsection ON HasSubsection.SubsectionID = Subsection.SubsectionID
        WHERE Subsection.StartStation = ? OR TrackSection.EndStation = ?""", (railway_station, railway_station))

    for route in train_routes:
        date = datetime.strptime(route[2], "%Y-%m-%d")
        if date.weekday() == weekdays.index(weekday):
            valid_routes.append(route)
    
    for route in valid_routes:
        if route[1] == 1:
            list_route = list(route)
            cleaned_reversed_direction = (list_route[0], list_route[2], list_route[4], list_route[3])
            cleaned_info.append(cleaned_reversed_direction)
        else:
            list_route = list(route)
            cleaned = (list_route[0], list_route[2], list_route[3], list_route[4])
            cleaned_info.append(cleaned)
        
    print(cleaned_info)
    return cleaned_info

#get_train_route("Steinkjer", "Monday")