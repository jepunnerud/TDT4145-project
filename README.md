# TDT4145-project

## Problem Description

You are tasked to create a database for the Norwegian railway system. In order to achieve appropriate
complexity and workload, the description of the railway system has been simplified considerably.
During the project, it will be necessary to make some assumptions which must be documented in the
project report.

The Norwegian railway system consists of physical track sections, such as the Nordland Line from
Trondheim to Bodø and the Dovre Line from Oslo to Trondheim. A track section starts at a railway
station, passes through a number of railway stations, and ends at a railway station. All track sections
have a name, are equipped for a driving energy that is either electric or diesel, and consist of a number
of sub-sections. A sub-section runs between two railway stations, has a length in km, and is either
single track or double track. Railway stations have a unique name, and the altitude of the station is
recorded (masl - meters above sea level).

The figure shows a simplified version of the Nordland Line, which we will use when storing data in the
database. We have assumed a double track between Trondheim and Steinkjer, since this is crucial and
should have been in place a long time ago. Trains on the Nordland
Line are powered by diesel.

Train routes run on track sections and these train routes may run in
the track section’s main direction or in the opposite direction. For the
Nordland Line, the main direction is from Trondheim to Bodø. A train
route can run the entire track section or only parts of it, for instance
from Mo i Rana to Trondheim. A train route has a start station and
an end station and usually stops at stations in-between. For each
railway station on the train route we have an arrival time/departure
time, except at the start station where the train route only has a
departure time and at the end station where the train route only has
an arrival time. A train route runs at most once a day, and it must be
recorded on which days of the week the train route runs from the
start station.

A train route is operated by an operator; on the Nordland Line, this
is SJ, which has a number of car types where customers can buy
tickets for seats. A car type has a name and is either a chair car or a
sleeping car. Chair cars have a number of seat rows where there are
a number of seats in each row. The seats are numbered from the
front of the car and from left to right. In a car with four seats per row,
we have seat numbers one to four on the first row, seat numbers five
to eight on the second row, etc. A sleeping car consists of a number
of sleeping compartments that are numbered from the front of the
car and backwards, so that a sleeping car with four sleeping compartments will have compartment
numbers from one to four. The beds are numbered from the front of the car so that the lower bed has
the lowest number in a compartment. A sleeping car with four sleeping compartments will have
sleeping places from number one to number eight, where sleeping place number six is the upper bed
in compartment number three.

A train route has a fixed car arrangement, made up of available car types, for example, two chair cars
and one sleeping car. In a car arrangement, the cars are numbered from the front to the back of the
train so that the car right after the locomotive is car number one. In the task, we ignore locomotives
and other service cars that can be included in a car arrangement. A train route has a fixed timetable
with departure/arrival times for each station on the route.

A train route has a train occurrence for each day the train route is operated. To travel on a train route,
a customer buys a ticket for one or more seats in a train occurrence. To purchase tickets, one must be
registered as a customer in the operators' common customer registry, with a unique customer
number, name, email address, and mobile number. A ticket purchase is organized into a customer
order that has a unique order number, day and time of purchase, and a number of ticket purchases in
the same train occurrence. To simplify the task, we ignore prices and payment of tickets. A ticket
applies to either a seat in a chair car or a bed in a sleeping car and reserves the space from one station
on the route to another station on the route. It should not be possible to buy tickets for seats that are
already sold. However, the same seat can be sold to several customers as long as their journeys do not
overlap. A customer can buy one or two places in a sleeping compartment. If a customer has reserved
a bed in a sleeping compartment, we cannot sell the available bed to another customer. If someone
has a ticket for one of the beds in a sleeping compartment on a part of the route, we do not sell the
seats in the compartment to others, even if their journey does not overlap with the journey of the
person who has already purchased a sleeping space.
