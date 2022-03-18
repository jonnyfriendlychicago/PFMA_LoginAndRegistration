from flaskApp.config.mysqlconnection import connectToMySQL
from flaskApp.models import flight_mod  # this line is needd for our join statement at the end. 

class Airline_cls: 
    db = 'loginAndRegistration_sch' # here, we are creating a reliable variable 'db' so that when we inevitably change the name of the db we are referencing, we only need to change this line to reflect that. 

    def __init__(self, data): 
        self.id = data['id']
        self.airlineName = data['airlineName']
        self.hqCity = data['hqCity']
        self.locationCount = data['locationCount']
        self.workerCount = data['workerCount']
        self.planeCount = data['planeCount']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.airlineAllFlightList = [] # used in the get_oneAirlineAllFlight method below

    @classmethod
    def get_allAirline(cls):
        q = 'select * from airline;'
        result = connectToMySQL(cls.db).query_db(q)
        airlineList = []
        for row in result: 
            airlineList.append(cls(row))
        return airlineList

    @classmethod
    def get_oneAirline(cls, data):
        q = 'select * from airline where id = %(id)s;'
        result = connectToMySQL(cls.db).query_db(q, data)
        if len(result) <1:
            return False
        return cls(result[0])

    @classmethod
    def saveAirline(cls, data):
        q = 'insert into airline (airlineName, hqCity, locationCount, workerCount, planeCount, createdAt, updatedAt) values ( %(airlineName)s, %(hqCity)s, %(locationCount)s, %(workerCount)s, %(planeCount)s, NOW(), NOW() );'
        return connectToMySQL(cls.db).query_db(q, data)

    @classmethod
    def updateAirline (cls, data):
        q = 'update airline set airlineName = %(airlineName)s, hqCity = %(hqCity)s, location = %(locationCount)s, workersCount = %(workersCount)s, planesCount = %(planesCount)s;'
        return connectToMySQL(cls.db).query_db(q, data)

    @classmethod
    def deleteAirline (cls, data):
        q = 'delete from airline where id = %(id)s;'
        return connectToMySQL(cls.db).query_db(q, data)

    @classmethod
    def get_oneAirlineAllFlight(cls, data):
        q = 'select * from airline a left join flight f on a.id = f.airline_id where a.id = %(id)s;'
        result = connectToMySQL(cls.db).query_db(q, data)
        # print('something??')
        airlineX = cls(result[0])
        for row in result: 
            airlineFlightDataDict = {
                'id': row['flight.id'],
                'flightNumber': row['flightNumber'],
                'departureAirport': row['departureAirport'],
                'arrivalAirport': row['arrivalAirport'],
                'createdAt': row['createdAt'],
                'updatedAt': row['updatedAt'],
                'airline_id': row['airline_id']
            }
            
            airlineX.airlineAllFlightList.append(flight_mod.Flight_cls(airlineFlightDataDict))
            # print("printing the lst form models: ", Airline_cls.flight)
        return airlineX

