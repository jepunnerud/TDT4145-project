import sqlite3

con = sqlite3.connect("trainDB.db")
cursor = con.cursor()


def get_train_occurences_from_date(date):
    res = cursor.execute(
        f"SELECT * FROM TrainOccurence as TrO LEFT JOIN TrainRoute as TR ON TrO.RouteID = TR.TrainRouteID where TrO.RouteDate = '{date}';"
    )
    return res.fetchall()


print(get_train_occurences_from_date("2023-04-03"))


# query that returns all subsections on a route
def get_subsections_on_route(route_id):
    res = cursor.execute(
        f"SELECT * FROM HasSubsection as HS LEFT JOIN Subsection as S ON HS.SubsectionID = S.SubsectionID where HS.TrackID = {route_id};"
    )
    return res.fetchall()


print(get_subsections_on_route(3))


def get_stations_on_route(route_id):
    res = cursor.execute(
        f"""SELECT DISTINCT RS.Name FROM RailwayStation as RS
        JOIN Subsection as SS on (RS.Name == SS.StartStation OR RS.Name == SS.EndStation) 
        JOIN HasSubsection as HS On SS.SubsectionID == HS.SubsectionID JOIN TrackSection as TS ON HS.TrackID == TS.TrackID 
        JOIN TrainRoute as TR on TR.TrackID = TS.TrackID where TR.TrainRouteID = {route_id};"""
    )
    tmp = []
    for row in res.fetchall():
        tmp.append(*row)

    return tmp


print(get_stations_on_route(2))
