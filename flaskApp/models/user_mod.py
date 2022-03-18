from flaskApp.config.mysqlconnection import connectToMySQL
from flaskApp.models import booking_mod
from flaskApp.models import flight_mod
from flaskApp.models import airline_mod
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# NAME_REGEX = re.compile(r'^[a-zA-Z ]+$') #WORKS!
# NAME_REGEX = re.compile(r'^[a-zA-Z -\'\\]+$') #this works too, for future reference
NAME_REGEX = re.compile(r'^[a-zA-Z -]+$') #WORKS!

# NAME_REGEX = re.compile(r'^[a-zA-Z -]+$')

class User_cls: 
    db = 'loginAndRegistration_sch'

    def __init__(self, data): 
        self.id = data['id']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.email = data['email']
        self.password = data['password']
        self.accessLevel = data['accessLevel']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        # below shall be used for join(s)
        
        self.booking = None
        self.flight = None
        self.airline = None
        self.flightList = []
    
    # below is a cheeky little function to save some typing.  Think about how functions like this can be exploited in other ways. 
    def fullName(self):
        return (f"{self.firstName} {self.lastName}")

    @staticmethod
    def validate(user):
        isValid = True
        q = 'select * from user where email = %(email)s;'
        result = connectToMySQL(User_cls.db).query_db(q, user)
        if len(result) >= 1: # somewhat clumsy way (??) of saying, if one or more results!
            isValid = False
            flash("Email already in use.")
        
        if not EMAIL_REGEX.match(user['email']): 
            isValid = False
            flash("Invalid email address.")
        
        if len(user['firstName']) < 1: # orig code says 2 char, but 1 seems better to me.  Malcolm X !
            isValid = False
            flash("First name cannot be blank.")
        
        if not NAME_REGEX.match(user['firstName']): 
            isValid = False
            flash("First name can only contain letters, spaces and hypen/dash/-.")

        if len(user['lastName']) < 1: # orig code says 2 char, but 1 seems better to me.  Malcolm X !
            isValid = False
            flash("Last name cannot be blank.")
        
        if not NAME_REGEX.match(user['lastName']): 
            isValid = False
            flash("Last name can only contain letters, spaces and hypen/dash/-.")

        # NAME_REGEX = re.compile(r'^a-zA-Z')

        if len(user['password']) < 8:
            isValid = False
            flash("Password must be at least 8 characters, ")
        if user['password'] != user['confirm']:
            isValid = False
            flash("Password entries must match.")
        return  isValid

    @classmethod
    def get_oneUser(cls, data):
        q = 'select * from user where id = %(id)s;'
        result = connectToMySQL(cls.db).query_db(q, data)
        if len(result) <1:
            return False
        return cls(result[0])

    @classmethod
    def get_allUser(cls, data):
        q = 'select * from user;'
        result = connectToMySQL(cls.db).query_db(q, data)
        userList = []
        for row in result:
            userList.append(cls(row))
        return userList
        
    @classmethod
    def get_userEmail(cls, data): # pretty sure that this shall be used for validating whether email exists already??
        q = 'select * from user where email = %(email)s;'
        result = connectToMySQL(cls.db).query_db(q, data)
        if len(result) <1:
            return False
        return cls(result[0])

    @classmethod
    def saveUser(cls, data):
        # below is deliberately leaving out accessLevel... yes? 
        # also, orig code left OUT createdAt & updatedAt... which I'm adding now. 
        q = 'insert into user (firstName, lastName, email, password, createdAt, updatedAt) values ( %(firstName)s, %(lastName)s, %(email)s, %(password)s, NOW(), NOW() );'
        return connectToMySQL(cls.db).query_db(q, data)

    # need to discuss below and why not make this a working feature. 
    @classmethod
    def updateUser (cls, data):
        pass

    @classmethod
    def updateUserEmpType (cls, data):
        q = 'update user set accessLevel = 9 where id = %(id)s;'
        return connectToMySQL(cls.db).query_db(q, data)

    # need to discuss below and why not make this a working feature. 
    @classmethod
    def delete (cls, data):
        pass

# above, good, let's figure out below now

    @classmethod
    def get_userBookingFlightAirline(cls, data):
        query = 'SELECT * FROM user Left JOIN booking ON user.id = booking.user_id LEFT JOIN flight ON booking.flight_id = flight.id LEFT JOIN airline ON flight.airline_id = airline.id WHERE user.id = %(id)s;'
        result = connectToMySQL(cls.db).query_db(query, data)
        print('userBookings model results: ', result)
        user = cls(result[0])
        for row in result:
            bookingData = {
                'id': row['booking.id'],
                'tripLeaderFirstName': row['tripLeaderFirstName'],
                'tripLeaderLastName': row['tripLeaderLastName'],
                'passengerCount': row['passengerCount'],
                'passengerCountAdult': row['passengerCountAdult'],
                'flightDate': row['flightDate'],
                'checkedBagsCount': row['checkedBagsCount'],
                'createdAt': row['booking.createdAt'],
                'updatedAt': row['booking.updatedAt'],
                'user_id': row['user_id'],
                'flight_id': row['flight_id'],
            }
            oneBooking = booking_mod.Booking_cls(bookingData) # clarify what this 'bookingData' is?  referencing?
            user.booking = oneBooking # explain this line please? 
            # Created a field for each  for this it is booking and set to none
            flightData = {
                'id': row['flight.id'],
                'flightNumber': row['flightNumber'],
                'departureAirport': row['departureAirport'],
                'arrivalAirport': row['arrivalAirport'],
                'createdAt': row['flight.createdAt'],
                'updatedAt': row['flight.updatedAt'],
                'airline_id': row['airline_id'],
            }
            oneFlight = flight_mod.Flight_cls(flightData)
            user.flight = oneFlight  
            airlineData = {
                'id': row['airline.id'],
                'airlineName': row['airlineName'],
                'hqCity': row['hqCity'],
                'locationCount': row['locationCount'],
                'workerCount': row['workerCount'],
                'planeCount': row['planeCount'],
                'createdAt': row['airline.createdAt'],
                'updatedAt': row['airline.updatedAt'],
            }
            oneAirline = airline_mod.Airline_cls(airlineData)
            user.airline = oneAirline
            # here we are taking these new single use values that were none and appending them to the flights then since it is single use or just a string that keeps getting updated each loop it will have new data and thus append new info...
            user.flightList.append(user)
            print('each row of users flights userBooking Model: ', bookingData, flightData, airlineData)
        print("printing list after append in model: ", user.flightList)
        return user.flightList