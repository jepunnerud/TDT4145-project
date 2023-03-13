CREATE TABLE RailwayStation(
    Name TEXT NOT NULL,
    Altitude REAL NOT NULL,
    CONSTRAINT PK_RailwayStation PRIMARY KEY (Name)
);
CREATE TABLE TrackSection(
    TrackID INTEGER NOT NULL,
    Name TEXT NOT NULL,
    Electric INTEGER NOT NULL,
    TrackID INTEGER NOT NULL,
    StartStation TEXT NOT NULL,
    EndStation TEXT NOT NULL,
    CONSTRAINT PK_TrackSection PRIMARY KEY (TrackID),
    CONSTRAINT FK_StartStation FOREIGN KEY (Name) REFERENCES RailwayStation (Name) ON DELETE CASCADE,
    CONSTRAINT FK_EndStation FOREIGN KEY (Name) REFERENCES RailwayStation (Name) ON DELETE CASCADE
);
CREATE TABLE Subsection(
    SubsectionID INTEGER NOT NULL,
    Length REAL NOT NULL,
    DoubleTrack INTEGER NOT NULL,
    StartStation TEXT NOT NULL,
    EndStation TEXT NOT NULL,
    CONSTRAINT FK_StartStation FOREIGN KEY (Name) REFERENCES RailwayStation (Name) ON DELETE CASCADE,
    CONSTRAINT FK_EndStation FOREIGN KEY (Name) REFERENCES RailwayStation (Name) ON DELETE CASCADE
);
CREATE TABLE HasSubsection(
    CONSTRAINT FK_Subsection FOREIGN KEY (SubsectionID) REFERENCES Subsection (SubsectionID) ON DELETE CASCADE,
    CONSTRAINT FK_Track FOREIGN KEY (TrackID) REFERENCES Track (TrackID) ON DELETE CASCADE
);
CREATE TABLE TrainRoute(
    TrainRouteID INTEGER NOT NULL,
    Direction INTEGER NOT NULL,
    OperatorID INTEGER NOT NULL,
    TrackID INTEGER NOT NULL,
    ArragementID INTEGER NOT NULL CONSTRAINT PK_TrainRoute PRIMARY KEY (TrainRouteID),
    CONSTRAINT FK_Operator FOREIGN KEY (OperatorID) REFERENCES Operator (OperatorID) ON DELETE CASCADE,
    CONSTRAINT FK_TrackSection FOREIGN KEY (TrackID) REFERENCES TrackSection (TrackID) ON DELETE CASCADE,
    CONSTRAINT FK_Arragement FOREIGN KEY (ArragementID) REFERENCES CarArrangement (ArragementID) ON DELETE CASCADE
);
CREATE TABLE TrainOccurence(
    RouteID INTEGER NOT NULL,
    RouteDate TEXT NOT NULL,
    CONSTRAINT PK_TrainOccurence PRIMARY KEY (RouteID, RouteDate)
);
CREATE TABLE Operator(
    OperatorID INTEGER NOT NULL,
    Name TEXT NOT NULL,
    DifferentCarsCount INTEGER NOT NULL,
    CONSTRAINT PK_Operator PRIMARY KEY (OperatorID)
);
CREATE TABLE Customer(
    CustomerNo INTEGER NOT NULL,
    Name TEXT NOT NULL,
    email TEXT NOT NULL,
    phoneNo INTEGER NOT NULL,
    OperatorID INTEGER NOT NULL,
    CONSTRAINT PK_CustomerNo PRIMARY KEY (CustomerNo),
    CONSTRAINT FK_RegisteredCustomer FOREIGN KEY (OperatorID) REFERENCES Operator (OperatorID) ON DELETE CASCADE
);
CREATE TABLE CustomerOrder(
    OrderNo INTEGER NOT NULL,
    CustomerID INTEGER NOT NULL,
    orderDateTime TEXT NOT NULL,
    CONSTRAINT PK_OrderNo PRIMARY KEY (OrderNo),
    CONSTRAINT FK_Customer FOREIGN KEY (CustomerID) REFERENCES Customer (CustomerNo) ON DELETE CASCADE
);
CREATE TABLE SeatTicket(
    TicketID INTEGER NOT NULL,
    OrderNo INTEGER NOT NULL,
    TicketStart TEXT NOT NULL,
    TicketEnd TEXT NOT NULL,
    RouteID INTEGER NOT NULL,
    TicketDate TEXT NOT NULL,
    SeatNo INTEGER NOT NULL,
    CONSTRAINT PK_Ticket PRIMARY KEY (TicketID),
    CONSTRAINT FK_OrderNo FOREIGN KEY (OrderNo) REFERENCES CustomerOrder (OrderNo) ON DELETE CASCADE,
    CONSTRAINT FK_TicketStart FOREIGN KEY (TicketStart) REFERENCES RailwayStation (Name) ON DELETE CASCADE,
    CONSTRAINT FK_TicketEnd FOREIGN KEY (TicketEnd) REFERENCES RailwayStation (Name) ON DELETE CASCADE,
    CONSTRAINT FK_Occurence FOREIGN KEY (RouteID, TicketDate) REFERENCES TrainOccurence (RouteID, RouteDate) ON DELETE CASCADE
);