from flaskApp.config.mysqlconnection import connectToMySQL
from flaskApp.models import user_mod
from flaskApp.models import flight_mod

class Booking_cls: 
    db = 'loginAndRegistration_sch'

    def __init__(self, data): 
        self.id = data['id']
        self.tripLeaderFirstName = data['tripLeaderFirstName']
        self.tripLeaderLastName = data['tripLeaderLastName']
        self.passengerCount = data['passengerCount']
        self.passengerCountAdult = data['passengerCountAdult']
        self.flightDate = data['flightDate']
        self.checkedBagsCount = data['checkedBagsCount']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']

    @classmethod
    def get_allBooking(cls):
        q = 'select * from booking;'
        result = connectToMySQL(cls.db).query_db(q)
        bookingList = []
        for row in result: 
            bookingList.append(cls(row))
        return bookingList

    @classmethod
    def get_oneBooking(cls, data):
        q = 'select * from booking where id = %(id)s;'
        result = connectToMySQL(cls.db).query_db(q, data)
        if len(result) <1:
            return False
        return cls(result[0])

    @classmethod
    def saveBooking(cls, data):
        q = 'insert into booking (tripLeaderFirstName, tripLeaderLastName, passengerCount, passengerCountAdult, flightDate, checkedBagsCount, createdAt, updatedAt) values ( %(tripLeaderFirstName)s, %(tripLeaderLastName)s, %(passengerCount)s, %(passengerCountAdult)s, %(flightDate)s, %(checkedBagsCount)s , NOW(), NOW() );'
        return connectToMySQL(cls.db).query_db(q, data)

    @classmethod
    def updateBooking (cls, data):
        q = 'update booking set tripLeaderFirstName=%(tripLeaderFirstName)s, tripLeaderLastName=%(tripLeaderLastName)s, passengerCount=%(passengerCount)s, passengerCountAdult=%(passengerCountAdult)s, flightDate=%(flightDate)s , checkedBagsCount=%(checkedBagsCount)s , updatedAt= NOW() ;'
        return connectToMySQL(cls.db).query_db(q, data)

    @classmethod
    def deleteBooking (cls, data):
        q = 'delete from booking where id = %(id)s;'
        return connectToMySQL(cls.db).query_db(q, data)
