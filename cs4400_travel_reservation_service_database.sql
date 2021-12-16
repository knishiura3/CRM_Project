DROP DATABASE IF EXISTS travel_reservation_service;
CREATE DATABASE IF NOT EXISTS travel_reservation_service;
USE travel_reservation_service;
SET GLOBAL sql_mode = sys.list_drop(@@GLOBAL.sql_mode, 'ONLY_FULL_GROUP_BY');
------------------------------------------
--
-- Entities
--
------------------------------------------

CREATE TABLE Accounts (
    Email VARCHAR(50) NOT NULL,
    First_Name VARCHAR(100) NOT NULL,
    Last_Name VARCHAR(100) NOT NULL,
    Pass VARCHAR(50) NOT NULL,

    PRIMARY KEY (Email)
);

-- Admin is a keyword in MySQL
CREATE TABLE Admins (
    Email VARCHAR(50) NOT NULL,

    PRIMARY KEY (Email),
    FOREIGN KEY (Email) REFERENCES Accounts (Email)
);

CREATE TABLE Clients (
    Email VARCHAR(50) NOT NULL,
    Phone_Number Char(12) UNIQUE NOT NULL CHECK (length(Phone_Number) = 12), -- Assuming format 123-456-7890

    PRIMARY KEY (Email),
    FOREIGN KEY (Email) REFERENCES Accounts (Email) 
);

-- Owner is a keyword in MySQL
CREATE TABLE Owners (
    Email VARCHAR(50) NOT NULL,

    PRIMARY KEY (Email),
    FOREIGN KEY (Email) REFERENCES Clients (Email)
);

CREATE TABLE Customer (
    Email VARCHAR(50) NOT NULL,
    CcNumber VARCHAR(19) UNIQUE NOT NULL CHECK (length(CcNumber) = 19), -- Assuming format "1234 1234 1234 1234"
    Cvv CHAR(3) NOT NULL CHECK (length(Cvv) = 3),
    Exp_Date DATE NOT NULL,
    Location VARCHAR(50) NOT NULL,

    PRIMARY KEY (Email),
    FOREIGN KEY (Email) REFERENCES Clients (Email)
);

CREATE TABLE Airline (
    Airline_Name VARCHAR(50) NOT NULL, -- Name is a keyword in MySQL
    Rating DECIMAL(2, 1) NOT NULL CHECK (Rating >= 1 AND Rating <= 5), -- Assuming 5 point rating scale

    PRIMARY KEY (Airline_Name)
);

CREATE TABLE Airport (
    Airport_Id CHAR(3) NOT NULL CHECK (length(Airport_Id) = 3),
    Airport_Name VARCHAR(50) UNIQUE NOT NULL,
    Time_Zone CHAR(3) NOT NULL CHECK(length(Time_Zone) = 3), -- Assuming 3 letter timezone abbreviation is used
    Street VARCHAR(50) NOT NULL,
    City VARCHAR(50) NOT NULL,
    State CHAR(2) NOT NULL CHECK(length(State) = 2),
    Zip CHAR(5) NOT NULL CHECK(length(Zip) = 5),

    PRIMARY KEY (Airport_Id),
    UNIQUE KEY (Street, City, State, Zip)
);

------------------------------------------
--
-- Weak Entities
--
------------------------------------------

CREATE TABLE Flight (
	-- Comment length check until flight numbers are updated
    Flight_Num CHAR(5) NOT NULL, -- CHECK(length(Flight_Num) = 5),
    Airline_Name VARCHAR(50) NOT NULL,
    From_Airport CHAR(3) NOT NULL,
    To_Airport CHAR(3) NOT NULL,
    Departure_Time TIME NOT NULL,
    Arrival_Time TIME NOT NULL,
    Flight_Date DATE NOT NULL,
    Cost DECIMAL(6, 2) NOT NULL CHECK (Cost >= 0), -- Allow prices from $0.00 to $9999.99
    Capacity INT NOT NULL CHECK (Capacity > 0),

    PRIMARY KEY (Flight_Num, Airline_Name),
    FOREIGN KEY (Airline_Name) REFERENCES Airline (Airline_Name),
    FOREIGN KEY (From_Airport) REFERENCES Airport (Airport_Id),
    FOREIGN KEY (To_Airport) REFERENCES Airport (Airport_Id),
    
    -- Destination airport must be different from origin airport
    CHECK (From_Airport != To_Airport)
    -- Flight must arrive after it departs
    -- Commenting this for now. Since for short flights across time zones
    -- this may not always hold
    -- CHECK (Departure_Time < Arrival_Time)
);

CREATE TABLE Property (
    Property_Name VARCHAR(50) NOT NULL,
    Owner_Email VARCHAR(50) NOT NULL,
    Descr VARCHAR(500) NOT NULL, -- Description is a keyword in MySQL
    Capacity INT NOT NULL CHECK (Capacity > 0),
    Cost DECIMAL(6, 2) NOT NULL CHECK (Cost >= 0), -- Allow prices from $0.00 to $9999.99
    Street VARCHAR(50) NOT NULL,
    City VARCHAR(50) NOT NULL,
    State CHAR(2) NOT NULL CHECK(length(State) = 2),
    Zip CHAR(5) NOT NULL CHECK(length(Zip) = 5),

    PRIMARY KEY (Property_Name, Owner_Email),
    FOREIGN KEY (Owner_Email) REFERENCES Owners (Email),
    UNIQUE KEY (Street, City, State, Zip)
);

------------------------------------------
--
-- Multivalued Attributes
--
------------------------------------------

CREATE TABLE Amenity (
    Property_Name VARCHAR(50) NOT NULL,
    Property_Owner VARCHAR(50) NOT NULL,
    Amenity_Name VARCHAR(50) NOT NULL,

    PRIMARY KEY (Property_Name, Property_Owner, Amenity_Name),
    FOREIGN KEY (Property_Name, Property_Owner) REFERENCES Property (Property_Name, Owner_Email) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Attraction (
    Airport CHAR(3) NOT NULL,
    Attraction_Name VARCHAR(50) NOT NULL,

    PRIMARY KEY (Airport, Attraction_Name),
    FOREIGN KEY (Airport) REFERENCES Airport (Airport_Id)
);

------------------------------------------
--
-- M-N Relationships
--
------------------------------------------

CREATE TABLE Review (
    Property_Name VARCHAR(50) NOT NULL,
    Owner_Email VARCHAR(50) NOT NULL,
    Customer VARCHAR(50) NOT NULL,
    Content VARCHAR(500), -- Assuming a customer could provide just a rating
    Score INT NOT NULL CHECK (Score >= 1 AND Score <= 5), -- Assuming 5 point rating scale

    PRIMARY KEY (Property_Name, Owner_Email, Customer),
    FOREIGN KEY (Property_Name, Owner_Email) REFERENCES Property (Property_Name, Owner_Email) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (Customer) REFERENCES Customer (Email)
);

CREATE TABLE Reserve (
    Property_Name VARCHAR(50) NOT NULL,
    Owner_Email VARCHAR(50) NOT NULL,
    Customer VARCHAR(50) NOT NULL,
    Start_Date DATE NOT NULL,
    End_Date DATE NOT NULL,
    Num_Guests INT NOT NULL CHECK (Num_Guests > 0),
    Was_Cancelled BOOLEAN NOT NULL,

    PRIMARY KEY (Property_Name, Owner_Email, Customer),
    FOREIGN KEY (Property_Name, Owner_Email) REFERENCES Property (Property_Name, Owner_Email),
    FOREIGN KEY (Customer) REFERENCES Customer (Email),
    
    -- End date must be after start date
    CHECK(End_Date >= Start_Date)
);

CREATE TABLE Is_Close_To (
    Property_Name VARCHAR(50) NOT NULL,
    Owner_Email VARCHAR(50) NOT NULL,
    Airport CHAR(3) NOT NULL,
    Distance INT NOT NULL CHECK (Distance >= 0), -- Assuming all distances rounded to nearest mile

    PRIMARY KEY (Property_Name, Owner_Email, Airport),
    FOREIGN KEY (Property_Name, Owner_Email) REFERENCES Property (Property_Name, Owner_Email) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (Airport) REFERENCES Airport (Airport_Id)
);

CREATE TABLE Book (
    Customer VARCHAR(50) NOT NULL,
    Flight_Num CHAR(5) NOT NULL,
    Airline_Name VARCHAR(50) NOT NULL,
    Num_Seats INT NOT NULL CHECK (Num_Seats > 0),
    Was_Cancelled BOOLEAN NOT NULL,

    PRIMARY KEY (Customer, Flight_Num, Airline_Name),
    FOREIGN KEY (Customer) REFERENCES Customer (Email),
    FOREIGN KEY (Flight_Num, Airline_Name) REFERENCES Flight (Flight_Num, Airline_Name)
);

CREATE TABLE Owners_Rate_Customers (
    Owner_Email VARCHAR(50) NOT NULL,
    Customer VARCHAR(50) NOT NULL,
    Score INT NOT NULL CHECK (Score >= 1 AND Score <= 5), -- Assuming 5 point rating scale

    PRIMARY KEY (Owner_Email, Customer),
    FOREIGN KEY (Owner_Email) REFERENCES Owners (Email) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (Customer) REFERENCES Customer (Email)
);

CREATE TABLE Customers_Rate_Owners (
    Customer VARCHAR(50) NOT NULL,
    Owner_Email VARCHAR(50) NOT NULL,
    Score INT NOT NULL CHECK (Score >= 1 AND Score <= 5), -- Assuming 5 point rating scale

    PRIMARY KEY (Customer, Owner_Email),
    FOREIGN KEY (Customer) REFERENCES Customer (Email),
    FOREIGN KEY (Owner_Email) REFERENCES Owners (Email) ON UPDATE CASCADE ON DELETE CASCADE
);

------------------------------------------
--
-- Insert Statements
--
------------------------------------------

INSERT INTO Accounts (Email, First_Name, Last_Name, Pass) VALUES
('mmoss1@travelagency.com', 'Mark', 'Moss', 'password1'),
('asmith@travelagency.com', 'Aviva', 'Smith', 'password2'),
('mscott22@gmail.com', 'Michael', 'Scott', 'password3'),
('arthurread@gmail.com', 'Arthur', 'Read', 'password4'),
('jwayne@gmail.com', 'John', 'Wayne', 'password5'),
('gburdell3@gmail.com', 'George', 'Burdell', 'password6'),
('mj23@gmail.com', 'Michael', 'Jordan', 'password7'),
('lebron6@gmail.com', 'Lebron', 'James', 'password8'),
('msmith5@gmail.com', 'Michael', 'Smith', 'password9'),
('ellie2@gmail.com', 'Ellie', 'Johnson', 'password10'),
('scooper3@gmail.com', 'Sheldon', 'Cooper', 'password11'),
('mgeller5@gmail.com', 'Monica', 'Geller', 'password12'),
('cbing10@gmail.com', 'Chandler', 'Bing', 'password13'),
('hwmit@gmail.com', 'Howard', 'Wolowitz', 'password14'),
('swilson@gmail.com', 'Samantha', 'Wilson', 'password16'),
('aray@tiktok.com', 'Addison', 'Ray', 'password17'),
('cdemilio@tiktok.com', 'Charlie', 'Demilio', 'password18'),
('bshelton@gmail.com', 'Blake', 'Shelton', 'password19'),
('lbryan@gmail.com', 'Luke', 'Bryan', 'password20'),
('tswift@gmail.com', 'Taylor', 'Swift', 'password21'),
('jseinfeld@gmail.com', 'Jerry', 'Seinfeld', 'password22'),
('maddiesmith@gmail.com', 'Madison', 'Smith', 'password23'),
('johnthomas@gmail.com', 'John', 'Thomas', 'password24'),
('boblee15@gmail.com', 'Bob', 'Lee', 'password25');

INSERT INTO Admins (Email) VALUES
('mmoss1@travelagency.com'),
('asmith@travelagency.com');

INSERT INTO Clients (Email, Phone_Number) VALUES
('mscott22@gmail.com', '555-123-4567'),
('arthurread@gmail.com', '555-234-5678'),
('jwayne@gmail.com', '555-345-6789'),
('gburdell3@gmail.com', '555-456-7890'),
('mj23@gmail.com', '555-567-8901'),
('lebron6@gmail.com', '555-678-9012'),
('msmith5@gmail.com', '555-789-0123'),
('ellie2@gmail.com', '555-890-1234'),
('scooper3@gmail.com', '678-123-4567'),
('mgeller5@gmail.com', '678-234-5678'),
('cbing10@gmail.com', '678-345-6789'),
('hwmit@gmail.com', '678-456-7890'),
('swilson@gmail.com', '770-123-4567'),
('aray@tiktok.com', '770-234-5678'),
('cdemilio@tiktok.com', '770-345-6789'),
('bshelton@gmail.com', '770-456-7890'),
('lbryan@gmail.com', '770-567-8901'),
('tswift@gmail.com', '770-678-9012'),
('jseinfeld@gmail.com', '770-789-0123'),
('maddiesmith@gmail.com', '770-890-1234'),
('johnthomas@gmail.com', '404-770-5555'),
('boblee15@gmail.com', '404-678-5555');

INSERT INTO Owners (Email) VALUES
('mscott22@gmail.com'),
('arthurread@gmail.com'),
('jwayne@gmail.com'),
('gburdell3@gmail.com'),
('mj23@gmail.com'),
('lebron6@gmail.com'),
('msmith5@gmail.com'),
('ellie2@gmail.com'),
('scooper3@gmail.com'),
('mgeller5@gmail.com'),
('cbing10@gmail.com'),
('hwmit@gmail.com');

INSERT INTO Customer (Email, CCNumber, Cvv, Exp_Date, Location) VALUES
('scooper3@gmail.com', '6518 5559 7446 1663', '551', '2024-2-01', ''),
('mgeller5@gmail.com', '2328 5670 4310 1965', '644', '2024-3-01', ''),
('cbing10@gmail.com', '8387 9523 9827 9291', '201', '2023-2-01', ''),
('hwmit@gmail.com', '6558 8596 9852 5299', '102', '2023-4-01', ''),
('swilson@gmail.com', '9383 3212 4198 1836', '455', '2022-8-01', ''),
('aray@tiktok.com', '3110 2669 7949 5605', '744', '2022-8-01', ''),
('cdemilio@tiktok.com', '2272 3555 4078 4744', '606', '2025-2-01', ''),
('bshelton@gmail.com', '9276 7639 7883 4273', '862', '2023-9-01', ''),
('lbryan@gmail.com', '4652 3726 8864 3798', '258', '2023-5-01', ''),
('tswift@gmail.com', '5478 8420 4436 7471', '857', '2024-12-01', ''),
('jseinfeld@gmail.com', '3616 8977 1296 3372', '295', '2022-6-01', ''),
('maddiesmith@gmail.com', '9954 5698 6355 6952', '794', '2022-7-01', ''),
('johnthomas@gmail.com', '7580 3274 3724 5356', '269', '2025-10-01', ''),
('boblee15@gmail.com', '7907 3513 7161 4248', '858', '2025-11-01', '');

INSERT INTO Airline (Airline_Name, Rating) VALUES
('Delta Airlines', 4.7),
('Southwest Airlines', 4.4),
('American Airlines', 4.6),
('United Airlines', 4.2),
('JetBlue Airways', 3.6),
('Spirit Airlines', 3.3),
('WestJet', 3.9),
('Interjet', 3.7);

INSERT INTO Airport (Airport_Id, Airport_Name, Time_Zone, Street, City, State, Zip) VALUES
('ATL', 'Atlanta Hartsfield Jackson Airport', 'EST', '6000 N Terminal Pkwy', 'Atlanta', 'GA', '30320'),
('JFK', 'John F Kennedy International Airport', 'EST', '455 Airport Ave', 'Queens', 'NY', '11430'),
('LGA', 'Laguardia Airport', 'EST', '790 Airport St', 'Queens', 'NY', '11371'),
('LAX', 'Lost Angeles International Airport', 'PST', '1 World Way', 'Los Angeles', 'CA', '90045'),
('SJC', 'Norman Y. Mineta San Jose International Airport', 'PST', '1702 Airport Blvd', 'San Jose', 'CA', '95110'),
('ORD', 'O\'Hare International Airport', 'CST', '10000 W O\'Hare Ave', 'Chicago', 'IL', '60666'),
('MIA', 'Miami International Airport', 'EST', '2100 NW 42nd Ave', 'Miami', 'FL', '33126'),
('DFW', 'Dallas International Airport', 'CST', '2400 Aviation DR', 'Dallas', 'TX', '75261');

INSERT INTO Flight (Flight_Num, Airline_Name, From_Airport, To_Airport, Departure_Time, Arrival_Time, Flight_Date, Cost, Capacity) VALUES
( '1', 'Delta Airlines', 'ATL', 'JFK', '100000', '120000', '2021-10-18', 400, 150),
( '2', 'Southwest Airlines', 'ORD', 'MIA', '103000', '143000', '2021-10-18', 350, 125),
( '3', 'American Airlines', 'MIA', 'DFW', '130000', '160000', '2021-10-18', 350, 125),
( '4', 'United Airlines', 'ATL', 'LGA', '163000', '183000', '2021-10-18', 400, 100),
( '5', 'JetBlue Airways', 'LGA', 'ATL', '110000', '130000', '2021-10-19', 400, 130),
( '6', 'Spirit Airlines', 'SJC', 'ATL', '123000', '213000', '2021-10-19', 650, 140),
( '7', 'WestJet', 'LGA', 'SJC', '130000', '160000', '2021-10-19', 700, 100),
( '8', 'Interjet', 'MIA', 'ORD', '193000', '213000', '2021-10-19', 350, 125),
( '9', 'Delta Airlines', 'JFK', 'ATL', '80000', '100000', '2021-10-20', 375, 150),
( '10', 'Delta Airlines', 'LAX', 'ATL', '91500', '181500', '2021-10-20', 700, 110),
( '11', 'Southwest Airlines', 'LAX', 'ORD', '120700', '190700', '2021-10-20', 600, 95),
( '12', 'United Airlines', 'MIA', 'ATL', '153500', '173500', '2021-10-20', 275, 115);

INSERT INTO Property (Property_Name, Owner_Email, Descr, Capacity, Cost, Street, City, State, Zip) VALUES
('Atlanta Great Property', 'scooper3@gmail.com', 'This is right in the middle of Atlanta near many attractions!', 4, 600, '2nd St', 'ATL', 'GA', '30008'),
('House near Georgia Tech', 'gburdell3@gmail.com', 'Super close to bobby dodde stadium!', 3, 275, 'North Ave', 'ATL', 'GA', '30008'),
('New York City Property', 'cbing10@gmail.com', 'A view of the whole city. Great property!', 2, 750, '123 Main St', 'NYC', 'NY', '10008'),
('Statue of Libery Property', 'mgeller5@gmail.com', 'You can see the statue of liberty from the porch', 5, 1000, '1st St', 'NYC', 'NY', '10009'),
('Los Angeles Property', 'arthurread@gmail.com', '', 3, 700, '10th St', 'LA', 'CA', '90008'),
('LA Kings House', 'arthurread@gmail.com', 'This house is super close to the LA kinds stadium!', 4, 750, 'Kings St', 'La', 'CA', '90011'),
('Beautiful San Jose Mansion', 'arthurread@gmail.com', 'Huge house that can sleep 12 people. Totally worth it!', 12, 900, 'Golden Bridge Pkwt', 'San Jose', 'CA', '90001'),
('LA Lakers Property', 'lebron6@gmail.com', 'This house is right near the LA lakers stadium. You might even meet Lebron James!', 4, 850, 'Lebron Ave', 'LA', 'CA', '90011'),
('Chicago Blackhawks House', 'hwmit@gmail.com', 'This is a great property!', 3, 775, 'Blackhawks St', 'Chicago', 'IL', '60176'),
('Chicago Romantic Getaway', 'mj23@gmail.com', 'This is a great property!', 2, 1050, '23rd Main St', 'Chicago', 'IL', '60176'),
('Beautiful Beach Property', 'msmith5@gmail.com', 'You can walk out of the house and be on the beach!', 2, 975, '456 Beach Ave', 'Miami', 'FL', '33101'),
('Family Beach House', 'ellie2@gmail.com', 'You can literally walk onto the beach and see it from the patio!', 6, 850, '1132 Beach Ave', 'Miami', 'FL', '33101'),
('Texas Roadhouse', 'mscott22@gmail.com', 'This property is right in the center of Dallas, Texas!', 3, 450, '17th Street', 'Dallas', 'TX', '75043'),
('Texas Longhorns House', 'mscott22@gmail.com', 'You can walk to the longhorns stadium from here!', 10, 600, '1125 Longhorns Way', 'Dallas', 'TX', '75001');

INSERT INTO Amenity (Property_Name, Property_Owner, Amenity_Name) VALUES
('Atlanta Great Property', 'scooper3@gmail.com', 'A/C & Heating'),
('Atlanta Great Property', 'scooper3@gmail.com', 'Pets allowed'),
('Atlanta Great Property', 'scooper3@gmail.com', 'Wifi & TV'),
('Atlanta Great Property', 'scooper3@gmail.com', 'Washer and Dryer'),
('House near Georgia Tech', 'gburdell3@gmail.com', 'Wifi & TV'),
('House near Georgia Tech', 'gburdell3@gmail.com', 'Washer and Dryer'),
('House near Georgia Tech', 'gburdell3@gmail.com', 'Full Kitchen'),
('New York City Property', 'cbing10@gmail.com', 'A/C & Heating'),
('New York City Property', 'cbing10@gmail.com', 'Wifi & TV'),
('Statue of Libery Property', 'mgeller5@gmail.com', 'A/C & Heating'),
('Statue of Libery Property', 'mgeller5@gmail.com', 'Wifi & TV'),
('Los Angeles Property', 'arthurread@gmail.com', 'A/C & Heating'),
('Los Angeles Property', 'arthurread@gmail.com', 'Pets allowed'),
('Los Angeles Property', 'arthurread@gmail.com', 'Wifi & TV'),
('LA Kings House', 'arthurread@gmail.com', 'A/C & Heating'),
('LA Kings House', 'arthurread@gmail.com', 'Wifi & TV'),
('LA Kings House', 'arthurread@gmail.com', 'Washer and Dryer'),
('LA Kings House', 'arthurread@gmail.com', 'Full Kitchen'),
('Beautiful San Jose Mansion', 'arthurread@gmail.com', 'A/C & Heating'),
('Beautiful San Jose Mansion', 'arthurread@gmail.com', 'Pets allowed'),
('Beautiful San Jose Mansion', 'arthurread@gmail.com', 'Wifi & TV'),
('Beautiful San Jose Mansion', 'arthurread@gmail.com', 'Washer and Dryer'),
('Beautiful San Jose Mansion', 'arthurread@gmail.com', 'Full Kitchen'),
('LA Lakers Property', 'lebron6@gmail.com', 'A/C & Heating'),
('LA Lakers Property', 'lebron6@gmail.com', 'Wifi & TV'),
('LA Lakers Property', 'lebron6@gmail.com', 'Washer and Dryer'),
('LA Lakers Property', 'lebron6@gmail.com', 'Full Kitchen'),
('Chicago Blackhawks House', 'hwmit@gmail.com', 'A/C & Heating'),
('Chicago Blackhawks House', 'hwmit@gmail.com', 'Wifi & TV'),
('Chicago Blackhawks House', 'hwmit@gmail.com', 'Washer and Dryer'),
('Chicago Blackhawks House', 'hwmit@gmail.com', 'Full Kitchen'),
('Chicago Romantic Getaway', 'mj23@gmail.com', 'A/C & Heating'),
('Chicago Romantic Getaway', 'mj23@gmail.com', 'Wifi & TV'),
('Beautiful Beach Property', 'msmith5@gmail.com', 'A/C & Heating'),
('Beautiful Beach Property', 'msmith5@gmail.com', 'Wifi & TV'),
('Beautiful Beach Property', 'msmith5@gmail.com', 'Washer and Dryer'),
('Family Beach House', 'ellie2@gmail.com', 'A/C & Heating'),
('Family Beach House', 'ellie2@gmail.com', 'Pets allowed'),
('Family Beach House', 'ellie2@gmail.com', 'Wifi & TV'),
('Family Beach House', 'ellie2@gmail.com', 'Washer and Dryer'),
('Family Beach House', 'ellie2@gmail.com', 'Full Kitchen'),
('Texas Roadhouse', 'mscott22@gmail.com', 'A/C & Heating'),
('Texas Roadhouse', 'mscott22@gmail.com', 'Pets allowed'),
('Texas Roadhouse', 'mscott22@gmail.com', 'Wifi & TV'),
('Texas Roadhouse', 'mscott22@gmail.com', 'Washer and Dryer'),
('Texas Longhorns House', 'mscott22@gmail.com', 'A/C & Heating'),
('Texas Longhorns House', 'mscott22@gmail.com', 'Pets allowed'),
('Texas Longhorns House', 'mscott22@gmail.com', 'Wifi & TV'),
('Texas Longhorns House', 'mscott22@gmail.com', 'Washer and Dryer'),
('Texas Longhorns House', 'mscott22@gmail.com', 'Full Kitchen');

INSERT INTO Attraction (Airport, Attraction_Name) VALUES
('ATL', 'The Coke Factory'),
('ATL', 'The Georgia Aquarium'),
('JFK', 'The Statue of Liberty'),
('JFK', 'The Empire State Building'),
('LGA', 'The Statue of Liberty'),
('LGA', 'The Empire State Building'),
('LAX', 'Lost Angeles Lakers Stadium'),
('LAX', 'Los Angeles Kings Stadium'),
('SJC', 'Winchester Mystery House'),
('SJC', 'San Jose Earthquakes Soccer Team'),
('ORD', 'Chicago Blackhawks Stadium'),
('ORD', 'Chicago Bulls Stadium'),
('MIA', 'Crandon Park Beach'),
('MIA', 'Miami Heat Basketball Stadium'),
('DFW', 'Texas Longhorns Stadium'),
('DFW', 'The Original Texas Roadhouse');

INSERT INTO Review (Property_Name, Owner_Email, Customer, Content, Score) VALUES
('House near Georgia Tech', 'gburdell3@gmail.com', 'swilson@gmail.com', 'This was so much fun. I went and saw the coke factory, the falcons play, GT play, and the Georgia aquarium. Great time! Would highly recommend!', 5),
('New York City Property', 'cbing10@gmail.com', 'aray@tiktok.com', 'This was the best 5 days ever! I saw so much of NYC!', 5),
('Statue of Libery Property', 'mgeller5@gmail.com', 'bshelton@gmail.com', 'This was truly an excellent experience. I really could see the Statue of Liberty from the property!', 4),
('Los Angeles Property', 'arthurread@gmail.com', 'lbryan@gmail.com', 'I had an excellent time!', 4),
('Beautiful San Jose Mansion', 'arthurread@gmail.com', 'tswift@gmail.com', "We had a great time, but the house wasn\'t fully cleaned when we arrived", 3),
('LA Lakers Property', 'lebron6@gmail.com', 'jseinfeld@gmail.com', 'I was disappointed that I did not meet lebron james', 2),
('Chicago Blackhawks House', 'hwmit@gmail.com', 'maddiesmith@gmail.com', 'This was awesome! I met one player on the chicago blackhawks!', 5),
('New York City Property', 'cbing10@gmail.com', 'cdemilio@tiktok.com', 'It was decent, but could have been better', 4);

INSERT INTO Reserve (Property_Name, Owner_Email, Customer, Start_Date, End_Date, Num_Guests, Was_Cancelled) VALUES
('House near Georgia Tech', 'gburdell3@gmail.com', 'swilson@gmail.com', '2021-10-19', '2021-10-25', 3, 0),
('New York City Property', 'cbing10@gmail.com', 'aray@tiktok.com', '2021-10-18', '2021-10-23', 2, 0),
('New York City Property', 'cbing10@gmail.com', 'cdemilio@tiktok.com', '2021-10-24', '2021-10-30', 2, 0),
('Statue of Libery Property', 'mgeller5@gmail.com', 'bshelton@gmail.com', '2021-10-18', '2021-10-22', 4, 0),
('Los Angeles Property', 'arthurread@gmail.com', 'lbryan@gmail.com', '2021-10-19', '2021-10-25', 2, 0),
('Beautiful San Jose Mansion', 'arthurread@gmail.com', 'tswift@gmail.com', '2021-10-19', '2021-10-22', 10, 0),
('LA Lakers Property', 'lebron6@gmail.com', 'jseinfeld@gmail.com', '2021-10-19', '2021-10-24', 4, 0),
('Chicago Blackhawks House', 'hwmit@gmail.com', 'maddiesmith@gmail.com', '2021-10-19', '2021-10-23', 2, 0),
('Chicago Romantic Getaway', 'mj23@gmail.com', 'aray@tiktok.com', '2021-11-1', '2021-11-7', 2, 1),
('Beautiful Beach Property', 'msmith5@gmail.com', 'cbing10@gmail.com', '2021-10-18', '2021-10-25', 2, 0),
('Family Beach House', 'ellie2@gmail.com', 'hwmit@gmail.com', '2021-10-18', '2021-10-28', 5, 1),
('New York City Property', 'cbing10@gmail.com', 'mgeller5@gmail.com', '2021-11-02', '2021-11-06', 3, 1);

INSERT INTO Is_Close_To (Property_Name, Owner_Email, Airport, Distance) VALUES
('Atlanta Great Property', 'scooper3@gmail.com', 'ATL', 12),
('House near Georgia Tech', 'gburdell3@gmail.com', 'ATL', 7),
('New York City Property', 'cbing10@gmail.com', 'JFK', 10),
('Statue of Libery Property', 'mgeller5@gmail.com', 'JFK', 8),
('New York City Property', 'cbing10@gmail.com', 'LGA', 25),
('Statue of Libery Property', 'mgeller5@gmail.com', 'LGA', 19),
('Los Angeles Property', 'arthurread@gmail.com', 'LAX', 9),
('LA Kings House', 'arthurread@gmail.com', 'LAX', 12),
('Beautiful San Jose Mansion', 'arthurread@gmail.com', 'SJC', 8),
('Beautiful San Jose Mansion', 'arthurread@gmail.com', 'LAX', 30),
('LA Lakers Property', 'lebron6@gmail.com', 'LAX', 6),
('Chicago Blackhawks House', 'hwmit@gmail.com', 'ORD', 11),
('Chicago Romantic Getaway', 'mj23@gmail.com', 'ORD', 13),
('Beautiful Beach Property', 'msmith5@gmail.com', 'MIA', 21),
('Family Beach House', 'ellie2@gmail.com', 'MIA', 19),
('Texas Roadhouse', 'mscott22@gmail.com', 'DFW', 8),
('Texas Longhorns House', 'mscott22@gmail.com', 'DFW', 17);

INSERT INTO Book (Customer, Flight_Num, Airline_Name, Num_Seats, Was_Cancelled) VALUES
('swilson@gmail.com', '5', 'JetBlue Airways', 3, 0),
('aray@tiktok.com', '1', 'Delta Airlines', 2, 0),
('bshelton@gmail.com', '4', 'United Airlines', 4, 0),
('lbryan@gmail.com', '7', 'WestJet', 2, 0),
('tswift@gmail.com', '7', 'WestJet', 2, 0),
('jseinfeld@gmail.com', '7', 'WestJet', 4, 1),
('bshelton@gmail.com', '5', 'JetBlue Airways', 4, 1),
('maddiesmith@gmail.com', '8', 'Interjet', 2, 0),
('cbing10@gmail.com', '2', 'Southwest Airlines', 2, 0),
('hwmit@gmail.com', '2', 'Southwest Airlines', 5, 1);

INSERT INTO Owners_Rate_Customers (Owner_Email, Customer, Score) VALUES
('gburdell3@gmail.com', 'swilson@gmail.com', 5),
('cbing10@gmail.com', 'aray@tiktok.com', 5),
('mgeller5@gmail.com', 'bshelton@gmail.com', 3),
('arthurread@gmail.com', 'lbryan@gmail.com', 4),
('arthurread@gmail.com', 'tswift@gmail.com', 4),
('lebron6@gmail.com', 'jseinfeld@gmail.com', 1),
('hwmit@gmail.com', 'maddiesmith@gmail.com', 2);

INSERT INTO Customers_Rate_Owners (Customer, Owner_Email, Score) VALUES
('swilson@gmail.com', 'gburdell3@gmail.com', 5),
('aray@tiktok.com', 'cbing10@gmail.com', 5),
('bshelton@gmail.com', 'mgeller5@gmail.com', 3),
('lbryan@gmail.com', 'arthurread@gmail.com', 4),
('tswift@gmail.com', 'arthurread@gmail.com', 4),
('jseinfeld@gmail.com', 'lebron6@gmail.com', 1),
('maddiesmith@gmail.com', 'hwmit@gmail.com', 2);

-- CS4400: Introduction to Database Systems (Fall 2021)
-- Phase III: Stored Procedures & Views [v0] Tuesday, November 9, 2021 @ 12:00am EDT
-- Team 103
-- arvind bangaru (abangaru3)
-- Dongkyung Lee (dlee812)
-- Jenna Kang (jkang394)
-- Kenji Nishiura (knishiura3)
-- Directions:
-- Please follow all instructions for Phase III as listed on Canvas.
-- Fill in the team number and names and GT usernames for all members above.


-- ID: 1a
-- Name: register_customer
drop procedure if exists register_customer;
delimiter //
create procedure register_customer (
    in i_email varchar(50),
    in i_first_name varchar(100),
    in i_last_name varchar(100),
    in i_password varchar(50),
    in i_phone_number char(12),
    in i_cc_number varchar(19),
    in i_cvv char(3),
    in i_exp_date date,
    in i_location varchar(50)
) 
sp_main: begin
-- TODO: Implement your solution here
	if (select count(*) from Accounts where Email=i_email) >0 then
		if (select count(*) from Clients where Email=i_email) >0 then
			if (select count(*) from Customer where Email=i_email) >0 then leave sp_main; end if;
			INSERT INTO Customer (Email, CCNumber, Cvv, Exp_Date, Location) VALUES (i_email,i_cc_number,i_cvv,i_exp_date,i_location);
        end if;
	else
		if (select count(*) from Accounts where Email=i_email) >0 then leave sp_main; end if;
        if (select count(*) from Clients where Phone_Number=i_phone_number) >0 then leave sp_main; end if;
        if (select count(*) from Customer where CcNumber=i_cc_number) >0 then leave sp_main; end if;
        
        INSERT INTO Accounts (Email, First_Name, Last_Name, Pass) VALUES (i_email,i_first_name,i_last_name,i_password);
        INSERT INTO Clients (Email, Phone_Number) VALUES (i_email,i_phone_number);
        INSERT INTO Customer (Email, CCNumber, Cvv, Exp_Date, Location) VALUES (i_email,i_cc_number,i_cvv,i_exp_date,i_location);

	end if;
end //
delimiter ;

-- ID: 1b
-- Name: register_owner
drop procedure if exists register_owner;
delimiter //
create procedure register_owner (
    in i_email varchar(50),
    in i_first_name varchar(100),
    in i_last_name varchar(100),
    in i_password varchar(50),
    in i_phone_number char(12)
) 
sp_main: begin
-- TODO: Implement your solution here
	-- if (select count(*) from Accounts where Email = i_email) > 0
	-- 	then leave sp_main; end if;
	-- if (select count(*) from Clients where Phone_Number = i_phone_number) > 0
	-- 	then leave sp_main; end if;
        
	if (select count(*) from Clients where Email = i_email) > 0 and 
	(select count(*) from Accounts where Email = i_email) > 0 and 
	(select count(*) from Owners where Email = i_email) = 0
    then insert into Owners (Email) values (i_email);
    leave sp_main; end if;
        
	insert into Accounts (Email, First_Name, Last_Name, Pass)
    values (i_email, i_first_name, i_last_name, i_password);
    insert into Clients (Email, Phone_Number) values (i_email, i_phone_number);
    insert into Owners (Email) values (i_email);
end //
delimiter ;


-- ID: 1c
-- Name: remove_owner
drop procedure if exists remove_owner;
delimiter //
create procedure remove_owner ( 
    in i_owner_email varchar(50)
)
sp_main: begin
-- TODO: Implement your solution here
	if (select count(*) from Property where Owner_Email = i_owner_email) > 0
    then leave sp_main; end if;
    
    delete from Owners_Rate_Customers where Owner_Email = i_owner_email;
    delete from Owners where Email = i_owner_email;
    
    if (select count(*) from Customer where Email = i_owner_email) = 0
    then delete from Clients where Email = i_owner_email;
    delete from Accounts where Email = i_owner_email; 
    end if;
end //
delimiter ;


-- ID: 2a
-- Name: schedule_flight
drop procedure if exists schedule_flight;
delimiter //
create procedure schedule_flight (
    in i_flight_num char(5),
    in i_airline_name varchar(50),
    in i_from_airport char(3),
    in i_to_airport char(3),
    in i_departure_time time,
    in i_arrival_time time,
    in i_flight_date date,
    in i_cost decimal(6, 2),
    in i_capacity int,
    in i_current_date date
)
sp_main: begin
-- TODO: Implement your solution here
	if (select Flight_Date from Flight where Flight_Num = i_flight_num) <= i_current_date then leave sp_main; end if;
    if i_from_airport = i_to_airport then leave sp_main; end if;
    
    if (select count(*) from Flight where Flight_Num = i_flight_num 
    and Airline_Name = i_airline_name) > 0 then leave sp_main; end if;
    
    insert into Flight (Flight_Num, Airline_Name, From_Airport, To_Airport, Departure_Time, Arrival_Time, Flight_Date, Cost, Capacity)
    values (i_flight_num, i_airline_name, i_from_airport, i_to_airport, i_departure_time, i_arrival_time, i_flight_date, i_cost, i_capacity);
    
end //
delimiter ;


-- ID: 2b
-- Name: remove_flight
drop procedure if exists remove_flight;
delimiter //
create procedure remove_flight ( 
    in i_flight_num char(5),
    in i_airline_name varchar(50),
    in i_current_date date
) 
sp_main: begin
-- TODO: Implement your solution here
	if (select Flight_Date from Flight where Flight_Num = i_flight_num) < i_current_date
    then leave sp_main; end if;
    
    
    delete from Book where Flight_Num = i_flight_num;
    delete from Flight where Flight_Num = i_flight_num;
    
    
end //
delimiter ;


-- ID: 3a
-- Name: book_flight
drop procedure if exists book_flight;
delimiter //
create procedure book_flight (
    in i_customer_email varchar(50),
    in i_flight_num char(5),
    in i_airline_name varchar(50),
    in i_num_seats int,
    in i_current_date date
)
sp_main: begin
-- TODO: Implement your solution here
-- Update seat numbers if Customer/AirlineName/FlightNumber match for non-cancelled booking
UPDATE Book
SET Num_Seats = Num_Seats + i_num_seats
WHERE Customer = i_customer_email
AND Airline_Name = i_airline_name
AND Flight_Num = i_flight_num
AND NOT Was_Cancelled = 1
;
INSERT INTO Book (Customer, Flight_Num, Airline_Name, Num_Seats, Was_Cancelled)
SELECT * FROM (SELECT i_customer_email, i_flight_num, i_airline_name, i_num_seats, 0) AS tmp
-- combo of customer email, flight number, and airline name can't be duplicates:
WHERE NOT EXISTS 
	(
     SELECT Customer, Flight_Num, Airline_Name
     FROM Book 
     WHERE Customer = i_customer_email
     AND Flight_Num = i_flight_num
     AND Airline_Name = i_airline_name
 	) 
-- number of seats being booked cannot exceed remaining seats on a flight
AND NOT EXISTS
	(    
	select Capacity-seats as seats_remaining from Flight
	join (
		select Flight_Num,Airline_Name,sum(Num_Seats) as seats from Book
		where Book.Was_Cancelled = 0
		group by Book.Flight_Num, Book.Airline_Name
		) as Booked
	on Flight.Flight_Num = Booked.Flight_Num and Flight.Airline_Name = Booked.Airline_Name
    WHERE i_num_seats > (Capacity-seats)
    )
-- Flight date must be in the future:
AND EXISTS 
	(
    SELECT Flight_Date 
    from Flight
    WHERE Flight_Date > i_current_date
    )
-- Can't have an existing non-cancelled flight 
AND NOT EXISTS
	(
        select * from Book 
        join Flight 
            on Book.Flight_Num = Flight.Flight_Num
            and Book.Airline_Name = Flight.Airline_Name
        WHERE 
            Book.Was_Cancelled = 0
            AND Book.Customer =  i_customer_email
            and Flight.Flight_Date in (
                select Flight.Flight_Date from Flight 
                where Flight.Flight_Num = i_flight_num
                and Flight.Airline_Name = i_airline_name)
	) 
;
end //
delimiter ;

-- ID: 3b
-- Name: cancel_flight_booking-
drop procedure if exists cancel_flight_booking;
delimiter //
create procedure cancel_flight_booking ( 
    in i_customer_email varchar(50),
    in i_flight_num char(5),
    in i_airline_name varchar(50),
    in i_current_date date
)
sp_main: begin
-- TODO: Implement your solution here
	if (select count(*) from Book where Customer = i_customer_email and Flight_Num = i_flight_num) = 0
    then leave sp_main; end if;
    if (select Flight_Date from Flight where Flight_Num = i_flight_num) <= i_current_date
    then leave sp_main; end if;
    
    update Book set Was_Cancelled = 1 where Customer = i_customer_email and Flight_Num = i_flight_num;
    
end //
delimiter ;

-- ID: 3c
-- Name: view_flight
create or replace view view_flight (
    flight_id,
    flight_date,
    airline,
    destination,
    seat_cost,
    num_empty_seats,
    total_spent
) as
-- TODO: replace this select query with your solution
select Flight.Flight_Num, Flight_Date, Flight.Airline_Name, To_Airport, Cost,
coalesce(Capacity-Sum(Num_Seats),Capacity),
coalesce(sum(Num_Seats),0)*Cost+(coalesce((select num_seats from Book where Flight.Flight_Num = Book.Flight_Num and Was_Cancelled = 1),0)*Cost*0.2)
from Flight left outer join Book on Flight.Flight_Num = Book.Flight_Num
where Was_Cancelled = 0 or Was_Cancelled is NULL
group by Flight.Flight_Num;

-- ID: 3c modified for phase 4
-- Name: view_flight
create or replace view view_flight_all (
    flight_id,
    flight_date,
    airline,
    source,
    destination,
    seat_cost,
    num_empty_seats,
    total_spent
) as
-- TODO: replace this select query with your solution
select Flight.Flight_Num, Flight_Date, Flight.Airline_Name,From_Airport, To_Airport, Cost,
coalesce(Capacity-Sum(Num_Seats),Capacity),
coalesce(sum(Num_Seats),0)*Cost+(coalesce((select num_seats from Book where Flight.Flight_Num = Book.Flight_Num and Was_Cancelled = 1),0)*Cost*0.2)
from Flight left outer join Book on Flight.Flight_Num = Book.Flight_Num
where Was_Cancelled = 0 or Was_Cancelled is NULL
group by Flight.Flight_Num;


-- ID: 4a
-- Name: add_property
drop procedure if exists add_property;
delimiter //
create procedure add_property (
    in i_property_name varchar(50),
    in i_owner_email varchar(50),
    in i_description varchar(500),
    in i_capacity int,
    in i_cost decimal(6, 2),
    in i_street varchar(50),
    in i_city varchar(50),
    in i_state char(2),
    in i_zip char(5),
    in i_nearest_airport_id char(3),
    in i_dist_to_airport int
) 
sp_main: begin
	if (select count(*) from Property where Street = i_street and City = i_city and Zip = i_zip and State = i_state) >0 then leave sp_main; end if;
	if (select count(*) from Property where Property_Name = i_property_name and Owner_Email = i_owner_email) >0 then leave sp_main; end if;
    INSERT INTO Property (Property_Name, Owner_Email, Descr, Capacity, Cost, Street, City, State, Zip) VALUES
	(i_property_name, i_owner_email, i_description, i_capacity, i_cost, i_street, i_city, i_state, i_zip);
    if (i_nearest_airport_id is not NULL) then
		if (i_dist_to_airport is not NULL) then
			if (select count(*) from Airport where Airport_Id = i_nearest_airport_id) = 0 then leave sp_main; end if;
            INSERT INTO Is_Close_To (Property_Name, Owner_Email, Airport, Distance) VALUES
			(i_property_name, i_owner_email, i_nearest_airport_id, i_dist_to_airport);
		end if;
	end if;
	select * from Property;
  
end //
delimiter ;

-- ID: 4b
-- Name: remove_property
drop procedure if exists remove_property;
delimiter //
create procedure remove_property (
    in i_property_name varchar(50),
    in i_owner_email varchar(50),
    in i_current_date date
)
sp_main: begin
-- TODO: Implement your solution here
	if (select count(*) from Reserve where Property_Name = i_property_name and Owner_Email = i_owner_email and Start_Date = i_current_date and Was_Cancelled = 0) > 0
		then leave sp_main; end if;
        
	delete from Reserve where Property_Name = i_property_name and Owner_Email = i_owner_email;
    delete from Property where Property_Name = i_property_name and Owner_Email = i_owner_email;
    /*
	delete from Review where Property_Name = i_property_name and Owner_Email = i_owner_email;
    delete from Amenity where Property_Name = i_property_name and Owner_Email = i_owner_email;
    delete from Is_Close_To where Property_Name = i_property_name and Owner_Email = i_owner_email;
    */
end //
delimiter ;



-- ID: 5a
-- This procedure allows customers to reserve an available property advertised by an owner if (and only if) the following conditions are met:
-- • The combination of property_name, owner_email, and customer_email should be unique in the system
-- • The start date of the reservation should be in the future (use current date for comparison)
-- • The guest has not already reserved a property that overlaps with the dates of this reservation
-- • The available capacity for the property during the span of dates must be greater than or equal to i_num_guests during the span of dates provided
-- • Note: for simplicity, the available capacity of a property over a span of time will be defined as the capacity of the property minus the total number of guests staying at that property during that span of time
-- Name: reserve_property
drop procedure if exists reserve_property;
delimiter //
create procedure reserve_property (
    in i_property_name varchar(50),
    in i_owner_email varchar(50),
    in i_customer_email varchar(50),
    in i_start_date date,
    in i_end_date date,
    in i_num_guests int,
    in i_current_date date
)
sp_main: begin
-- TODO: Implement your solution here
INSERT INTO Reserve (Property_Name, Owner_Email, Customer, Start_Date, End_Date, Num_Guests, Was_Cancelled)
SELECT * FROM (SELECT i_property_name, i_owner_email, i_customer_email, i_start_date, i_end_date, i_num_guests, 0) AS tmp
-- combo of property name and owner/cust emails can't be duplicates:
WHERE NOT EXISTS 
	(
    SELECT Property_Name, Owner_Email, Customer
    FROM Reserve 
    WHERE Property_Name = i_property_name
    AND Owner_Email = i_owner_email
    AND Customer = i_customer_email
	) 
-- Start date must be in the future:
AND i_start_date > i_current_date
-- input dates can't overlap existing reservations for the input customer:
AND NOT EXISTS
	(
    SELECT Customer, Start_Date, End_Date
    FROM Reserve 
    WHERE 
		Customer = i_customer_email
		AND ((i_start_date > Start_Date) AND (i_start_date < End_Date) OR (i_end_date > Start_Date) AND (i_end_date < End_Date))
    )
-- for any given property with a non-cancelled reservation, number of guests on new input reservation needs to fit within remaining capacity for the same dates
-- /*
AND NOT EXISTS
	(
	select Property.Property_Name, Property.Owner_Email, Property.Capacity, Was_Cancelled, Reserve.Num_guests from Property 
	left outer join Reserve ON Reserve.Property_Name=Property.Property_Name AND Reserve.Owner_Email=Property.Owner_Email
	WHERE Was_Cancelled=0 
	AND (((i_start_date > Start_Date) AND (i_start_date < End_Date)) OR ((i_end_date > Start_Date) AND (i_end_date < End_Date)))
	AND (i_num_guests > Property.Capacity
    OR i_num_guests > (Property.Capacity-Reserve.Num_guests))
	)
-- */
LIMIT 1;
end //
delimiter ;



-- ID: 5b
-- This procedure allows a customer to cancel an existing property reservation if (and only if) the following conditions are met:
-- • The customer must already have reserved this property
-- • If the reservation is already cancelled, this procedure should do nothing
-- • The date of the reservation must be at a date in the future (use the current date passed in for comparison)
-- • To cancel a reservation, the was_cancelled attribute in the reserve table should be set to 1
-- Name: cancel_property_reservation
drop procedure if exists cancel_property_reservation;
delimiter //
create procedure cancel_property_reservation (
    in i_property_name varchar(50),
    in i_owner_email varchar(50),
    in i_customer_email varchar(50),
    in i_current_date date
)
sp_main: begin
-- TODO: Implement your solution here
UPDATE Reserve
SET Was_Cancelled = 1
WHERE Property_Name = i_property_name
AND Owner_Email = i_owner_email
AND Customer = i_customer_email
AND NOT Was_Cancelled = 1
AND i_current_date < Start_Date
;
end //
delimiter ;

-- ####################################################################
-- ####################################################################
-- ID: 5c
-- This procedure allows customers to leave a review for a property at which they stayed if (and only if) the following conditions are met:
-- • The customer must have started a stay at this property at a date in the past that wasn’t cancelled (current date must be equal to or later than the start date of the reservation at this property)
-- • The combination of property_name, owner_email, and customer_email should be distinct in the review table (a customer should not be able to review a property more than once)
-- Name: customer_review_property
drop procedure if exists customer_review_property;
delimiter //
create procedure customer_review_property (
    in i_property_name varchar(50),
    in i_owner_email varchar(50),
    in i_customer_email varchar(50),
    in i_content varchar(500),
    in i_score int,
    in i_current_date date
)
sp_main: begin
-- TODO: Implement your solution here
INSERT INTO Review (Property_Name, Owner_Email, Customer, Content, Score)
SELECT * FROM (SELECT i_property_name, i_owner_email, i_customer_email, i_content, i_score) AS tmp
-- exact combo of property name and owner/cust emails can't exist:
WHERE NOT EXISTS 
	(
    SELECT Property_Name, Owner_Email, Customer
    FROM Review 
    WHERE Property_Name = i_property_name
    AND Owner_Email = i_owner_email
    AND Customer = i_customer_email
	) 
-- There must be a proprety reservation matching the review property/owner
AND EXISTS
	(
	SELECT Property_Name, Owner_Email, Customer, Start_Date
    FROM Reserve
    WHERE Property_Name = i_property_name
    AND Owner_Email = i_owner_email
    AND Customer = i_customer_email
    AND Was_Cancelled = 0
    AND i_current_date > Start_Date
	)
;
end //
delimiter ;
-- ####################################################################
-- ####################################################################

-- ID: 5d
-- This view displays the name, average rating score, description, concatenated address, capacity, and cost per night of all properties. 
-- Note: The concatenated address should have a comma and space (‘, ‘) between each part of the address (ie: “Blackhawks St, Chicago, IL, 60176”).
-- Name: view_properties
create or replace view view_properties (
    property_name, 
    average_rating_score, 
    description, 
    address, 
    capacity, 
    cost_per_night
) as
-- TODO: replace this select query with your solution
select 
	Property.Property_Name,
    average_score,
    Descr, 
	CONCAT(Street, ", ", City, ", ", State, ", ", ZIP) as full_address, 
	Capacity, 
	Cost
from 
	(
	select Property_Name,avg(Score) as average_score from Review
	group by Review.Property_Name
    ) as Prating
right outer join Property 
on Property.Property_Name = Prating.Property_Name;
-- ####################################################################
-- ####################################################################
-- ID: 5e
-- Name: view_individual_property_reservations
drop procedure if exists view_individual_property_reservations;
delimiter //
create procedure view_individual_property_reservations (
    in i_property_name varchar(50),
    in i_owner_email varchar(50)
)
sp_main: begin
    drop table if exists view_individual_property_reservations;
    create table view_individual_property_reservations (
        property_name varchar(50),
        start_date date,
        end_date date,
        customer_email varchar(50),
        customer_phone_num char(12),
        total_booking_cost decimal(6,2),
        rating_score int,
        review varchar(500)
    ) as
    -- TODO: replace this select query with your solution
    select 
		Reserve.Property_Name as property_name,
        Start_Date as start_date,
        End_Date as end_date,
        Reserve.Customer as customer_email ,
		Clients.Phone_Number as customer_phone_num,
		(datediff(Reserve.End_Date, Reserve.Start_Date)+1 )*Property.Cost*(1-0.8*Reserve.Was_Cancelled) as total_booking_cost,
		Review.Score as rating_score,
        Review.Content  as review
	from Reserve
	join Property on
		Reserve.Property_Name= Property.Property_Name and 
		Reserve.Owner_Email= Property.Owner_Email
	join Clients on
		Clients.Email= Reserve.Customer
	left outer join Review on
		Reserve.Property_Name= Review.Property_Name and 
		Reserve.Owner_Email= Review.Owner_Email and
		Reserve.Customer = Review.Customer
	-- where Reserve.Property_Name='New York City Property' and Reserve.Owner_Email = 'cbing10@gmail.com';
	where 
		Reserve.Property_Name=i_property_name and 
        Reserve.Owner_Email = i_owner_email;
    

end //
delimiter ;



-- ####################################################################
-- ####################################################################
-- ID: 6a
-- Name: customer_rates_owner
drop procedure if exists customer_rates_owner;
delimiter //
create procedure customer_rates_owner (
    in i_customer_email varchar(50),
    in i_owner_email varchar(50),
    in i_score int,
    in i_current_date date
)
sp_main: begin
if (
    SELECT count(*)
    FROM Reserve 
    WHERE Owner_Email = i_owner_email
    AND Customer = i_customer_email
    AND Was_Cancelled <> 1
    AND Start_Date <= i_current_date
    ) =0 then leave sp_main; end if;

if (
    SELECT count(*)
    FROM Owners
    Where Email = i_owner_email
) =0 then leave sp_main; end if;
-- AND EXISTS
    -- input customer is in database
if (
    SELECT count(*)
    FROM Customer
    Where Email = i_customer_email
    )=0 then leave sp_main; end if;
-- AND NOT EXISTS
    -- review doesn't already exist for customer/owner pair
if (
    SELECT count(*)
    FROM Customers_Rate_Owners
    WHERE Owner_Email = i_owner_email
    AND Customer = i_customer_email
    )>0 then leave sp_main; end if;
INSERT INTO Customers_Rate_Owners (Customer, Owner_Email, Score)
values (i_customer_email, i_owner_email, i_score);
end //
delimiter ;
-- ####################################################################
-- ####################################################################
-- ID: 6b
-- Name: owner_rates_customer
drop procedure if exists owner_rates_customer;
delimiter //
create procedure owner_rates_customer (
    in i_owner_email varchar(50),
    in i_customer_email varchar(50),
    in i_score int,
    in i_current_date date
)
sp_main: begin
-- TODO: Implement your solution here

-- there is a reservation in the past matching property name, owner/customer emails that was not cancelled.
if (
    SELECT count(*)
    FROM Reserve 
    WHERE Owner_Email = i_owner_email
    AND Customer = i_customer_email
    AND Was_Cancelled <> 1
    AND Start_Date <= i_current_date
    ) =0 then leave sp_main; end if;

if (
    SELECT count(*)
    FROM Owners
    Where Email = i_owner_email
) =0 then leave sp_main; end if;
-- AND EXISTS
    -- input customer is in database
if (
    SELECT count(*)
    FROM Customer
    Where Email = i_customer_email
    )=0 then leave sp_main; end if;
	-- review doesn't already exist for customer/owner pair
if (
    SELECT count(*)
    FROM Owners_Rate_Customers
    WHERE Owner_Email = i_owner_email
    AND Customer = i_customer_email
    )>0 then leave sp_main; end if;
INSERT INTO Owners_Rate_Customers (Owner_Email, Customer, Score)
values (i_owner_email, i_customer_email, i_score);
end //
delimiter ;
-- ####################################################################
-- ####################################################################
-- ID: 7a
-- Name: view_airports
create or replace view view_airports (
    airport_id, 
    airport_name, 
    time_zone, 
    total_arriving_flights, 
    total_departing_flights, 
    avg_departing_flight_cost
) as
-- TODO: replace this select query with your solution    
select Airport_ID, Airport_Name, Time_Zone, 
(select count(*) from Flight where Airport.Airport_Id = Flight.To_Airport),
(select count(*) from Flight where Airport.Airport_Id = Flight.From_Airport),
(select avg(Cost) from Flight where Airport.Airport_Id = Flight.From_Airport) 
from Airport, Flight
group by Airport_ID
order by Airport_ID;
-- ####################################################################
-- ####################################################################
-- ID: 7b
-- Name: view_airlines
create or replace view view_airlines (
    airline_name, 
    rating, 
    total_flights, 
    min_flight_cost
) as
-- TODO: replace this select query with your solution
select Airline.Airline_Name,
	Rating,
	(select count(*) from Flight where Airline.Airline_Name = Flight.Airline_Name),
    (select min(Cost) from Flight where Airline.Airline_Name = Flight.Airline_Name) 
    from Airline join Flight on Airline.Airline_Name = Flight.Airline_Name
    group by Airline.Airline_Name;

-- ####################################################################
-- ####################################################################
-- ID: 8a
-- Name: view_customers
create or replace view view_customers (
    customer_name, 
    avg_rating, 
    location, 
    is_owner, 
    total_seats_purchased
) as
-- TODO: replace this select query with your solution
-- view customers
select customer_name, avg_rating, location, is_owner, total_seats_purchased
from (select Customer.Email as email, concat(First_Name,' ',Last_Name) as customer_name, Location as location from Customer join Accounts on Accounts.Email = Customer.Email)
as fullname_t  
join (select avg(Score) as avg_rating, Email as email from Customer  left join Owners_Rate_Customers on Owners_Rate_Customers.Customer = Customer.Email group by Customer.Email)
as avg_rat_t on fullname_t.email = avg_rat_t.email
join (select count(Owners.Email) as is_owner,Customer.Email as email from Customer left outer join Owners on Customer.Email = Owners.Email group by Customer.Email)
as is_owner_t on fullname_t.email = is_owner_t.email
join (select Customer.Email as email, sum(ifnull(Num_Seats,0)) as total_seats_purchased from Customer left outer join Book on Customer.Email = Book.Customer group by Customer.Email)
as tot_seats_t on fullname_t.email = tot_seats_t.email
;
-- ####################################################################
-- ####################################################################
-- ID: 8b
-- Name: view_owners
create or replace view view_owners (
    owner_name, 
    avg_rating, 
    num_properties_owned, 
    avg_property_rating
) as
-- TODO: replace this select query with your solution
select owner_name, avg_rating, num_prp,avg_prp_rating
from (select Owners.Email as email, concat(First_Name,' ',Last_Name) as owner_name from Accounts join Owners on Accounts.Email = Owners.Email) as full_name_t
left join (select Owner_Email as email,avg(Score) as avg_rating from Customers_Rate_Owners group by Owner_Email) as avg_rating_t
on full_name_t.email = avg_rating_t.email
left join (select Owner_Email as email,avg(Score) as avg_prp_rating from Review group by Owner_Email) as avg_prp_rating_t 
on full_name_t.email = avg_prp_rating_t.email
join (select Email as email, count(Owner_Email) as num_prp from Owners left outer join Property on Email = Owner_Email group by Email) as num_prp_t 
on full_name_t.email = num_prp_t.email
;
-- ####################################################################
-- ####################################################################
-- ID: 9a
-- Name: process_date
drop procedure if exists process_date;
delimiter //
create procedure process_date ( 
    in i_current_date date
)
sp_main: begin
-- TODO: Implement your solution herelower case
	DROP VIEW IF EXISTS view_9a;
	create view view_9a as
	select Book.Customer, Airport.State, Flight.Flight_Date
	from Book
	join Flight on 
		Flight.Airline_Name = Book.Airline_Name and 
		Flight.Flight_Num = Book.Flight_Num
	join Airline on 
		Airline.Airline_Name = Book.Airline_Name
	join Airport on 
		Airport.Airport_Id = Flight.To_Airport
    where 
		Book.Was_Cancelled <> 1;
        
    update
		Customer
	set
		Customer.Location = (
			select view_9a.State 
            from view_9a 
            where view_9a.Customer = Customer.Email and view_9a.Flight_Date =  i_current_date
            )
	where 
		Customer.Email in (
			select view_9a.Customer 
            from view_9a 
            where view_9a.Flight_Date = i_current_date
            );
end //
delimiter ;
-- ####################################################################
-- ####################################################################
drop procedure if exists check_account_type;
delimiter //
create procedure check_account_type (
    in i_email varchar(50),
    in i_password varchar(50)
) 
sp_main: begin
-- TODO: Implement your solution here
	select 
		Accounts.Email as acc,
        Owners.Email as own,
        Customer.Email as cus,
        Admins.Email as adm
	from Accounts
	left join Owners
		on Accounts.Email = Owners.Email
	left join Customer
		on Accounts.Email = Customer.Email
	left join Admins
		on Accounts.Email = Admins.Email
	where 
		Accounts.Email = i_email and
        Accounts.Pass = i_password;
end //
delimiter ;
-- ####################################################################
-- ####################################################################

drop procedure if exists check_email;
delimiter //
create procedure check_email (
    in i_email varchar(50)
) 
sp_main: begin
-- TODO: Implement your solution here
	select Accounts.Email from Accounts
	where 
		Accounts.Email = i_email;
end //
delimiter ;
-- ####################################################################
-- ####################################################################
drop procedure if exists check_account;
delimiter //
create procedure check_account (
    in i_email varchar(50),
    in i_password varchar(50)
) 
sp_main: begin
-- TODO: Implement your solution here
	select Accounts.Email from Accounts
	where 
		Accounts.Email = i_email and
        Accounts.Pass = i_password;
end //
delimiter ;
-- ####################################################################
-- ####################################################################

drop procedure if exists check_phonenumber;
delimiter //
create procedure check_phonenumber (
    in i_phone_number char(12)
) 
sp_main: begin
-- TODO: Implement your solution here
	select Clients.Phone_Number from Clients
	where 
		Clients.Phone_Number = i_phone_number;
end //
delimiter ;
-- ####################################################################
-- ####################################################################
drop procedure if exists check_credit_card;
delimiter //
create procedure check_credit_card (
    in i_cc_number varchar(19)
) 
sp_main: begin
-- TODO: Implement your solution here
	select Customer.CcNumber from Customer
	where 
		Customer.CcNumber = i_cc_number;
end //
delimiter ;

-- ####################################################################
-- ####################################################################
-- ####################################################################
-- kenji ####################################################################
create or replace view view_active_flight_bookings (
    airline_name, 
    flight_number, 
    flight_date, 
    customer_email
) as
-- TODO: replace this select query with your solution
SELECT Flight.Airline_Name, Flight.Flight_Num, Flight.Flight_Date, Book.Customer
FROM Flight
LEFT JOIN Book ON Book.Airline_Name = Flight.Airline_Name
AND Book.Flight_Num = Flight.Flight_Num
WHERE Book.Was_Cancelled = 0;
-- ####################################################################
-- ####################################################################
-- ####################################################################
-- kenji ####################################################################
create or replace view view_property_needs_review (
    start_date, 
    property_name, 
    owner_email, 
    address,
    customer_email
) as
-- TODO: replace this select query with your solution
SELECT Reserve.Start_Date, Reserve.Property_Name, Reserve.Owner_Email, concat(Property.Street," ",Property.City," ",Property.State," ",Property.Zip) as Address,Reserve.Customer
FROM Reserve LEFT JOIN Review ON (Reserve.Property_Name = Review.Property_Name AND Reserve.Owner_Email = Review.Owner_Email AND Reserve.Customer = Review.Customer)
LEFT JOIN Property on Property.Property_Name = Reserve.Property_Name 
WHERE Review.Property_Name IS NULL
;

-- ####################################################################
-- ####################################################################
drop procedure if exists check_airline_name;
delimiter //
create procedure check_airline_name (
in i_airline_name varchar(50)
) 
sp_main: begin
-- TODO: Implement your solution here
select Airline_Name from Airline
where 
Airline_Name = i_airline_name;
end //
delimiter ;


drop procedure if exists check_airport_id;
delimiter //
create procedure check_airport_id (
in i_airport_id char(3)
) 
sp_main: begin
-- TODO: Implement your solution here
select Airport_Id from Airport
where 
Airport_Id = i_airport_id;
end //
delimiter ;
