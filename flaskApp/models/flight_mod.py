from flaskApp.config.mysqlconnection import connectToMySQL
from flaskApp.models import airline_mod

class Flight_cls: 
    db = 'loginAndRegistration_sch'

    def __init__(self, data): 
        self.id = data['id']
        self.flightNumber = data['flightNumber']
        self.departureAirport = data['departureAirport']
        self.arrivalAirport = data['arrivalAirport']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.airline_id = data['airline_id']

    @classmethod
    def get_allFlight(cls):
        q = 'select * from flight;'
        result = connectToMySQL(cls.db).query_db(q)
        flightList = []
        for row in result: 
            flightList.append(cls(row))
        return flightList

    @classmethod
    def get_oneFlight(cls, data):
        q = 'select * from flight where id = %(id)s;'
        result = connectToMySQL(cls.db).query_db(q, data)
        if len(result) <1:
            return False
        return cls(result[0])

    @classmethod
    def saveFlight(cls, data):
        q = 'insert into flight (flightNumber, departureAirport, arrivalAirport, createdAt, updatedAt, airline_id) values ( %(flightNumber)s, %(departureAirport)s, %(arrivalAirport)s, NOW(), NOW(), %(airline_id)s );'
        return connectToMySQL(cls.db).query_db(q, data)

    @classmethod
    def updateFlight (cls, data):
        q = "update flight set flightNumber = %(flightNumber)s, departureAirport = %(departureAirport)s, arrivalAirport = %(arrivalAirport)s, updatedAt = NOW() where id = %(id)s;" 
        return connectToMySQL(cls.db).query_db(q, data)

    @classmethod
    def deleteFlight (cls, data):
        q = 'delete from flight where id = %(id)s;'
        return connectToMySQL(cls.db).query_db(q, data)
