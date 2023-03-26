import sqlite3
from constants import con
from user_story_c import get_train_route
from datetime import datetime
from dateutil import parser

cursor = con.cursor()


def start_after_end(start, end):
    res = cursor.execute(
        f"""SELECT DISTINCt RS.Name, HS.OrderIndex FROM TrackSection as TS
        INNER JOIN HasSubsection as HS ON TS.TrackID == HS.TrackID 
        INNER JOIN Subsection as SS ON HS.SubsectionID == SS.SubsectionID
        INNER JOIN RailwayStation as RS ON RS.Name = SS.StartStation OR RS.Name = SS.EndStation
        WHERE RS.Name = '{start}' OR RS.Name = '{end}'
        GROUP BY RS.name
        ORDER BY OrderIndex DESC;"""
    )
    res = res.fetchall()
    return res[0][0] == start


def get_train_route_between_two_stations(start, end, date, time):
    if start == end:
        print("Start and end station are the same")
        return
    if not (
        get_train_route(start, datetime.fromisoformat(date).strftime("%A"))
        and get_train_route(end, datetime.fromisoformat(date).strftime("%A"))
    ):
        print("No routes found on the given date and stations")
        return
    res = cursor.execute(
        """WITH RouteOnDate (RouteID, Direction, RouteDate, TrackID) AS (SELECT TR.TrainRouteID, TR.Direction, TrO.RouteDate, TR.TrackID FROM TrainOccurence as TrO
                LEFT JOIN TrainRoute as TR ON TrO.RouteID = TR.TrainRouteID
                WHERE TrO.RouteDate = date('2023-04-03', '+1 day') OR TrO.RouteDate = date('2023-04-03'))
            SELECT RouteOnDate.RouteID, RouteOnDate.Direction, RouteOnDate.RouteDate, RouteOnDate.TrackID, HS.SubsectionID, SS.StartStation, SS.EndStation, RTT.Time FROM RouteOnDate INNER JOIN HasSubsection as HS ON RouteOnDate.TrackID = HS.TrackID
                INNER JOIN Subsection as SS ON HS.SubsectionID = SS.SubsectionID
                INNER JOIN RouteTimetable as RTT ON RTT.RouteID = RouteOnDate.RouteID AND
                (IIF (RouteOnDate.Direction = 0, RTT.RailwayStation = SS.StartStation, RTT.RailwayStation = SS.EndStation));"""
    )
    res = res.fetchall()
    clean = []
    for row in res:
        clean.append([*row])
    routes = {}
    for row in clean:
        if row[0] not in routes:
            routes[row[0]] = []
        routes[row[0]].append(row)

    direction = start_after_end(start, end)

    valid_results = {}

    for route_id, route_tuple in routes.items():
        for subsection in route_tuple:
            if direction and (not subsection[1]):
                continue
            elif not direction and subsection[1]:
                continue
            else:
                if (
                    route_id not in valid_results
                    and subsection[7] > time
                    and start in subsection
                ):
                    valid_results[route_id] = [subsection]
                elif (
                    route_id in valid_results
                    and subsection[7] > time
                    and start in subsection
                ):
                    valid_results[route_id].append(subsection)

    valid_routes = []
    for valid_route_tuple in valid_results.values():
        for subsection in valid_route_tuple:
            valid_routes.append(subsection)

    sorted_by_date = sorted(valid_routes, key=lambda x: parser.isoparse(x[2]))

    if not valid_results:
        print("No routes found on the given date and stations")
        return
    else:
        print(f"Routes from {start} to {end} on {date} at {time}:")
        for subsection in sorted_by_date:
            print(
                f"Route {subsection[0]}: {start} - {end} on {subsection[2]} at {subsection[7]}"
            )

    return


get_train_route_between_two_stations(
    "Trondheim", "Steinkjer", "2023-04-03", "07:00"
)
