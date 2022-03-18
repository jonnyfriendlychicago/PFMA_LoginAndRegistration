from flaskApp import app

from flaskApp.controllers import flight_ctrl, airline_ctrl, user_ctrl, booking_ctrl

if __name__ == "__main__": 
    app.run(debug = True)