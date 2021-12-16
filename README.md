# CRM_Project
A Customer Relationship Management class project with GUI &amp; SQL database

Instructions to setup the app:
    create the database 'travel_reservation_system' by running the 
    sql file 'cs4400_travel_reservation_service_database.sql' provided in submission
    (by running it in mysql-workbench for example)

    install the python prequisits using the command:
        pip install mysql-connector-python 
    or if you use anaconda:
        conda install mysql-connector-python
    mysql connection information in main.py:
        change the connection_config_dict according to your installation, for example:
        connection_config_dict = {
            'host':'localhost',
            'user': 'root',
            'password': 'password',
            'db': 'travel_reservation_service'
        }

Instructions to run the app:
    to run the app execute the main.py python script in terminal
    using:
        python3 main.py
    or by using:
        chmod +x main.py
        ./main.py
Brief explanation of what technologies you used and how you accomplished your application:
    tkinter: Tkinter is a Python binding to the Tk GUI toolkit.
    It is the standard Python interface to the Tk GUI toolkit, and is Python's de facto standard GUI
    use tkinter to make the different screens and aligned the lables and buttons using pack and grid
    function
    mysql.connector: MySQL Connector/Python, is a self-contained Python driver for communicating with MySQL servers
    used this to connect to the MySQL database created using the 'cs4400_travel_reservation_service_database.sql' script
    stored procedures: called the stored procedures created for phase 3 using the mysql.connector in python and 
    used these to manupulate the database
work done by teammates:
    all the team members have extensively tested the script 
    arvind bangaru (abangaru3):
        worked on login, register, Customer Admin Owner Home, Admin Remove Flight, Book Flight, Customer Reserve Property
    Dongkyung Lee (dlee812):
        Book Flight, Customer Cancel Flight, Customer Rate Owner, Owner Add Property, Owner Remove Property, Owner Rate Customer, Customer View Flights
    Jenna Kang (jkang394):
        Admin Process Date, Customer View Flights, Customer Cancel Property Reservation, Customer View Properties, Customer View Individual Property Reservations, Owner Deletes Account

    Kenji Nishiura (knishiura3):
        Admin Schedule Flight, Admin View Airports, Admin View Airlines, Admin View Customers, Admin View Owners, Customer Cancel Flight, Customer Review Property
