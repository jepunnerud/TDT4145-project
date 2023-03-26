import sqlite3


def createTables():
    con = sqlite3.connect("trainDB.db")
    cursor = con.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS RailwayStation (
        Name TEXT NOT NULL,
        Altitude REAL NOT NULL,
        CONSTRAINT PK_RailwayStation PRIMARY KEY (Name)
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS TrackSection(
        TrackID INTEGER NOT NULL,
        Name TEXT NOT NULL,
        Electric INTEGER NOT NULL,
        StartStation TEXT NOT NULL,
        EndStation TEXT NOT NULL,
        CONSTRAINT PK_TrackSection PRIMARY KEY (TrackID),
        CONSTRAINT FK_StartStation FOREIGN KEY (Name) REFERENCES RailwayStation (Name) ON DELETE CASCADE,
        CONSTRAINT FK_EndStation FOREIGN KEY (Name) REFERENCES RailwayStation (Name) ON DELETE CASCADE
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Subsection(
        SubsectionID INTEGER NOT NULL,
        Length REAL NOT NULL,
        DoubleTrack INTEGER NOT NULL,
        StartStation TEXT NOT NULL,
        EndStation TEXT NOT NULL,
        CHECK (Length > 0),
        CONSTRAINT PK_Subsection PRIMARY KEY (SubsectionID),
        CONSTRAINT FK_StartStation FOREIGN KEY (StartStation) REFERENCES RailwayStation (Name) ON DELETE CASCADE,
        CONSTRAINT FK_EndStation FOREIGN KEY (EndStation) REFERENCES RailwayStation (Name) ON DELETE CASCADE
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS HasSubsection(
        TrackID INTEGER NOT NULL,
        SubsectionID INTEGER NOT NULL,
        OrderIndex INTEGER NOT NULL,
        CONSTRAINT PK_Track PRIMARY KEY (TrackID, SubsectionID),
        CONSTRAINT FK_Subsection FOREIGN KEY (SubsectionID) REFERENCES Subsection (SubsectionID) ON DELETE CASCADE,
        CONSTRAINT FK_Track FOREIGN KEY (TrackID) REFERENCES Track (TrackID) ON DELETE CASCADE
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS TrainRoute(
        TrainRouteID INTEGER NOT NULL,
        Direction INTEGER NOT NULL,
        OperatorID INTEGER NOT NULL,
        TrackID INTEGER NOT NULL,
        ArrangementID INTEGER NOT NULL,
        CONSTRAINT PK_TrainRoute PRIMARY KEY (TrainRouteID),
        CONSTRAINT FK_Operator FOREIGN KEY (OperatorID) REFERENCES Operator (OperatorID) ON DELETE CASCADE,
        CONSTRAINT FK_TrackSection FOREIGN KEY (TrackID) REFERENCES TrackSection (TrackID) ON DELETE CASCADE,
        CONSTRAINT FK_Arrangement FOREIGN KEY (ArrangementID) REFERENCES CarArrangement (ArrangementID) ON DELETE CASCADE
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS TrainOccurence(
        RouteID INTEGER NOT NULL,
        RouteDate TEXT NOT NULL,
        CONSTRAINT PK_TrainOccurence PRIMARY KEY (RouteID, RouteDate),
        CONSTRAINT FK_TrainRoute FOREIGN KEY (RouteID) REFERENCES TrainRoute (TrainRouteID) ON DELETE CASCADE
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Operator(
        OperatorID INTEGER NOT NULL,
        Name TEXT NOT NULL,
        DifferentCarsCount INTEGER NOT NULL,
        CONSTRAINT PK_Operator PRIMARY KEY (OperatorID)
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Customer(
        CustomerNo INTEGER NOT NULL,
        Name TEXT NOT NULL,
        email TEXT NOT NULL,
        phoneNo INTEGER NOT NULL UNIQUE,
        CONSTRAINT PK_CustomerNo PRIMARY KEY (CustomerNo)
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS CustomerOrder(
        OrderNo INTEGER NOT NULL,
        CustomerID INTEGER NOT NULL,
        orderDateTime TEXT NOT NULL,
        CONSTRAINT PK_OrderNo PRIMARY KEY (OrderNo),
        CONSTRAINT FK_Customer FOREIGN KEY (CustomerID) REFERENCES Customer (CustomerNo) ON DELETE CASCADE
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS SeatTicket(
        TicketNo INTEGER NOT NULL,
        OrderNo INTEGER,
        TicketStart TEXT NOT NULL,
        TicketEnd TEXT NOT NULL,
        RouteID INTEGER NOT NULL,
        TicketDate TEXT NOT NULL,
        CarID INTEGER NOT NULL,
        SeatNo INTEGER NOT NULL,
        CONSTRAINT PK_Ticket PRIMARY KEY (TicketNo),
        CONSTRAINT FK_OrderNo FOREIGN KEY (OrderNo) REFERENCES CustomerOrder (OrderNo),
        CONSTRAINT FK_TicketStart FOREIGN KEY (TicketStart) REFERENCES RailwayStation (Name) ON DELETE CASCADE,
        CONSTRAINT FK_TicketEnd FOREIGN KEY (TicketEnd) REFERENCES RailwayStation (Name) ON DELETE CASCADE,
        CONSTRAINT FK_Car FOREIGN KEY (CarID) REFERENCES ChairCar (CarID) ON DELETE CASCADE,
        CONSTRAINT FK_Occurence FOREIGN KEY (RouteID, TicketDate) REFERENCES TrainOccurence (RouteID, RouteDate) ON DELETE CASCADE
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS BedTicket(
        TicketNo INTEGER NOT NULL,
        OrderNo INTEGER NOT NULL,
        TicketStart TEXT NOT NULL,
        TicketEnd TEXT NOT NULL,
        RouteID INTEGER NOT NULL,
        TicketDate TEXT NOT NULL,
        BedNo INTEGER NOT NULL,
        CONSTRAINT PK_Ticket PRIMARY KEY (TicketNo),
        CONSTRAINT FK_OrderNo FOREIGN KEY (OrderNo) REFERENCES CustomerOrder (OrderNo) ON DELETE CASCADE,
        CONSTRAINT FK_TicketStart FOREIGN KEY (TicketStart) REFERENCES RailwayStation (Name) ON DELETE CASCADE,
        CONSTRAINT FK_TicketEnd FOREIGN KEY (TicketEnd) REFERENCES RailwayStation (Name) ON DELETE CASCADE,
        CONSTRAINT FK_Occurence FOREIGN KEY (RouteID, TicketDate) REFERENCES TrainOccurence (RouteID, RouteDate) ON DELETE CASCADE
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Car(
        CarID INTEGER NOT NULL,
        CONSTRAINT PK_Car PRIMARY KEY (CarID)
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS ChairCar(
        CarID INTEGER NOT NULL,
        OperatorID INTEGER NOT NULL,
        SeatingRowCount INTEGER NOT NULL,
        SeatsPerRow INTEGER NOT NULL,
        CHECK (SeatingRowCount > 0),
        CONSTRAINT PK_Car PRIMARY KEY (CarID),
        CONSTRAINT FK_Car FOREIGN KEY (CarID) REFERENCES Car (CarID) ON DELETE CASCADE,
        CONSTRAINT FK_Operator FOREIGN KEY (OperatorID) REFERENCES Operator (OperatorID) ON DELETE CASCADE
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS SleepingCar(
        CarID INTEGER NOT NULL,
        OperatorID INTEGER NOT NULL,
        SleepingCompartmentCount INTEGER NOT NULL,
        CHECK (SleepingCompartmentCount > 0),
        CONSTRAINT PK_Car PRIMARY KEY (CarID),
        CONSTRAINT FK_Car FOREIGN KEY (CarID) REFERENCES Car (CarID) ON DELETE CASCADE,
        CONSTRAINT FK_Operator FOREIGN KEY (OperatorID) REFERENCES Operator (OperatorID) ON DELETE CASCADE
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Seat(
        CarID INTEGER NOT NULL,
        SeatNo INTEGER NOT NULL,
        CONSTRAINT FK_Car FOREIGN KEY (CarID) REFERENCES ChairCar (CarID) ON DELETE CASCADE,
        CONSTRAINT PK_Seat PRIMARY KEY (CarID, SeatNo)
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Bed(
        CarID INTEGER NOT NULL,
        CompartmentNo INTEGER NOT NULL,
        BedNo INTEGER NOT NULL,
        CONSTRAINT FK_Car FOREIGN KEY (CarID) REFERENCES SleepingCar (CarID) ON DELETE CASCADE,
        CONSTRAINT PK_Bed PRIMARY KEY (CarID, BedNo)
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS RouteTimetable(
        RouteID INTEGER NOT NULL,
        RailwayStation TEXT NOT NULL,
        Time TEXT NOT NULL,
        CONSTRAINT FK_RouteID FOREIGN KEY (RouteID) REFERENCES TrainRoute (RouteID) ON DELETE CASCADE,
        CONSTRAINT FK_RailwayStation FOREIGN KEY (RailwayStation) REFERENCES RailwayStation (Name) ON DELETE CASCADE,
        CONSTRAINT PK_Timetable PRIMARY KEY (RouteID, RailwayStation)
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS CarArrangement(
        ArrangementID INTEGER NOT NULL,
        CONSTRAINT PK_Arrangement PRIMARY KEY (ArrangementID)
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS CarInArrangement(
        ArrangementID INTEGER NOT NULL,
        CarID INTEGER NOT NULL,
        CONSTRAINT PK_CarInArrangement PRIMARY KEY (ArrangementID, CarID),
        CONSTRAINT FK_Arrangement FOREIGN KEY (ArrangementID) REFERENCES CarArrangement (ArrangementID) ON DELETE CASCADE,
        CONSTRAINT FK_Car FOREIGN KEY (CarID) REFERENCES Car (CarID) ON DELETE CASCADE
    );
    """
    )

    con.commit()
    con.close()
