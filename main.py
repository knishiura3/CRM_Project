#!/usr/bin/env python3
# Purpose : testing gui (tkinter) and connecting to mySQL database in python
# Authors  : arvind bangaru, Dongkyung Lee, Jenna Kang, Kenji Nishiura
# Email   : abangaru3@gatech.edu, dlee812@gatech.edu, jkang394@gatech.edu, knishiura3@gatech.edu
# ------------------------------------------------------------
# /home/vrionto/mySSD/education/GaTech/Fall 2021/classes/CS4400/project/phase-3/cs4400_travel_reservation_service_database.sql

# installing the database and intialising travel_reservation_service
# providing dbinfo to python script
# installing mysql.connector

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import BOLD
import tkinter
import mysql.connector
import re
from datetime import datetime
import time

connection_config_dict = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "db": "travel_reservation_service",
}

# testing
########################################
# current_user_account_type = []
# current_email = 'cbing10@gmail.com'
# current_password = ''
# current_date = '2022-10-12'

###########################################

# sections

# for login and registration
if True:
    # for login and registratio

    def login():
        global login_email
        global login_password
        login_email = var_login_email.get()
        login_password = var_login_password.get()

        w_login_email.config(text="")
        w_login_password.config(text="")
        # print([login_email,login_password])

        # if the fields are empty
        if login_email == "":
            w_login_email.config(text="email can not be empty")
            return None
        if login_password == "":
            w_login_password.config(text="password can not be empty")
            return None

        # check if email is registered
        if check_email(login_email) == False:
            w_login_email.config(text="email not registered")
            w_login_password.config(text="")
            return None

        if check_account(login_email, login_password) == False:
            w_login_email.config(text="")
            w_login_password.config(text="password is wrong")
            return None

        global current_user_account_type
        global current_email
        global current_password
        current_email = login_email
        current_password = login_password
        current_user_account_type = get_account_type(login_email, login_password)
        screen_login.destroy()

    def register():

        register_fname = var_register_fname.get()
        register_lname = var_register_lname.get()
        register_email = var_register_email.get()
        register_password1 = var_register_password1.get()
        register_password2 = var_register_password2.get()
        register_phonenumber = var_register_phonenumber.get()
        register_customer = var_register_customer.get()
        register_card_num = var_register_card_num.get()
        register_card_cvv = var_register_card_cvv.get()
        register_card_exp = var_register_card_exp.get()
        register_owner = var_register_owner.get()

        w_register_fname.config(text="")
        w_register_lname.config(text="")
        w_register_email.config(text="")
        w_register_password1.config(text="")
        w_register_password2.config(text="")
        w_register_phonenumber.config(text="")
        w_register_customer.config(text="")
        w_register_card_num.config(text="")
        w_register_card_cvv.config(text="")
        w_register_card_exp.config(text="")
        w_register_owner.config(text="")

        if register_fname == "":
            w_register_fname.config(text="first name can not be empty")
            return None
        if register_lname == "":
            w_register_lname.config(text="last name can not be empty")
            return None
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", register_email):
            w_register_email.config(text="enter valid email")
            return None
        if check_email(register_email) == True:
            w_register_email.config(
                text="email already registered, use a different one"
            )
            return None

        if register_password1 == "":
            w_register_password1.config(text="password can not be empty")
            return None
        elif register_password2 == "":
            w_register_password2.config(text="re enter password")
            return None
        elif register_password1 != register_password2:
            w_register_password2.config(text="passwords dont match")
            return None

        if not re.match(r"^[0-9]{3}-[0-9]{3}-[0-9]{4}$", register_phonenumber):
            w_register_phonenumber.config(
                text="enter valid US phone number eg: 123-456-7890"
            )
            return None
        if check_phonenumber(register_phonenumber) == True:
            w_register_phonenumber.config(
                text="phone number already registered, use a different one"
            )
            return None
        # print([register_customer,register_owner])
        if register_owner in ["", "0"] and register_customer in ["", "0"]:
            w_register_owner.config(
                text="check the checkbox for owner and/or customer "
            )
            w_register_customer.config(
                text="check the checkbox for owner and/or customer"
            )
            return None
        if register_customer == "1":

            if not re.match(r"^[0-9]{16}$", register_card_num):
                w_register_card_num.config(
                    text="enter a valid 16 digit credit card number"
                )
                return None
            else:
                formatted_register_card_num = " ".join(
                    [
                        register_card_num[i : i + 4]
                        for i in range(0, len(register_card_num), 4)
                    ]
                )
                # print([formatted_register_card_num])
            if check_credit_card(formatted_register_card_num) == True:
                # print([formatted_register_card_num,'True'])
                w_register_card_num.config(
                    text="credit card already registered, use a different one"
                )
                return None
            if not re.match(r"^[0-9]{3}$", register_card_cvv):
                w_register_card_cvv.config(text="enter a valid 3 digit credit card cvv")
                return None
            try:
                datetime.strptime(register_card_exp, "%Y-%m-%d")
            except:
                w_register_card_exp.config(
                    text="enter a valid credit card expiry date yyyy-mm-dd"
                )
                return None

        if register_customer == "1":

            register_customer_new(
                register_email,
                register_fname,
                register_lname,
                register_password1,
                register_phonenumber,
                formatted_register_card_num,
                register_card_cvv,
                register_card_exp,
            )
        if register_owner == "1":

            register_owner_new(
                register_email,
                register_fname,
                register_lname,
                register_password1,
                register_phonenumber,
            )

        global current_user_account_type
        current_user_account_type = get_account_type(register_email, register_password1)
        global current_email
        global current_password
        current_email = register_email
        current_password = register_password1
        screen_register.destroy()

    def logout(screen_now):
        global current_email
        global current_password
        current_email = ""
        current_password = ""
        screen_now.destroy()
        window_login()

    def exit_app(screen_now):
        screen_now.destroy()

    def check_email(email):
        db = mysql.connector.connect(**connection_config_dict)
        mysql_connection = db.cursor()
        savequery = f"call check_email('{email}')"
        results = mysql_connection.execute(savequery, multi=True)
        for cur in results:
            if cur.with_rows:
                table_fetched = cur.fetchall()
                # print('result:',table_fetched )
        mysql_connection.close()
        if len(table_fetched) == 1:
            return True
        else:
            return False

    def check_account(email, password):
        db = mysql.connector.connect(**connection_config_dict)
        mysql_connection = db.cursor()
        savequery = f"call check_account('{email}', '{password}')"
        results = mysql_connection.execute(savequery, multi=True)
        for cur in results:
            if cur.with_rows:
                table_fetched = cur.fetchall()
                # print('result:',table_fetched )
        mysql_connection.close()
        if len(table_fetched) == 1:
            return True
        else:
            return False

    def check_phonenumber(phonenumber):
        db = mysql.connector.connect(**connection_config_dict)
        mysql_connection = db.cursor()
        savequery = f"call check_phonenumber('{phonenumber}')"
        results = mysql_connection.execute(savequery, multi=True)
        for cur in results:
            if cur.with_rows:
                table_fetched = cur.fetchall()
                # print('result:',table_fetched )
        mysql_connection.close()
        if len(table_fetched) == 1:
            return True
        else:
            return False

    def check_credit_card(card_number):
        db = mysql.connector.connect(**connection_config_dict)
        mysql_connection = db.cursor()
        savequery = f"call check_credit_card('{card_number}')"
        results = mysql_connection.execute(savequery, multi=True)
        for cur in results:
            if cur.with_rows:
                table_fetched = cur.fetchall()
                # print('result:',table_fetched )
        mysql_connection.close()
        if len(table_fetched) == 1:
            return True
        else:
            return False

    def get_account_type(email, password):
        account_type = []
        db = mysql.connector.connect(**connection_config_dict)
        mysql_connection = db.cursor()
        savequery = f"call check_account_type('{email}', '{password}')"
        results = mysql_connection.execute(savequery, multi=True)
        for cur in results:
            if cur.with_rows:
                table_fetched = cur.fetchall()
                # print('result:',table_fetched )
        mysql_connection.close()
        if table_fetched[0][1] != None:
            account_type.append("owner")
        if table_fetched[0][2] != None:
            account_type.append("customer")
        if table_fetched[0][3] != None:
            account_type.append("admin")

        mysql_connection.close()
        return account_type

    def register_customer_new(
        email, fname, lname, password, phone_number, card_number, cvv_number, card_exp
    ):
        # print('registering as cust')
        db = mysql.connector.connect(**connection_config_dict)
        mysql_connection = db.cursor()
        savequery = f"call register_customer('{email}', '{fname}', '{lname}', '{password}', '{phone_number}', '{card_number}', '{cvv_number}', '{card_exp}', '')"
        # print([savequery])
        # return None
        # mysql_connection.execute(savequery)
        # my_result = mysql_connection.fetchall()

        # print([savequery, my_result])
        results = mysql_connection.execute(savequery, multi=True)
        for cur in results:
            if cur.with_rows:
                table_fetched = cur.fetchall()
                print("result:", table_fetched)
        db.commit()
        mysql_connection.close()

    def register_owner_new(email, fname, lname, password, phone_number):
        # print('registering as own')
        db = mysql.connector.connect(**connection_config_dict)
        mysql_connection = db.cursor()
        savequery = f"call register_owner('{email}', '{fname}', '{lname}', '{password}', '{phone_number}')"
        # print([savequery])
        # return None
        # mysql_connection.execute(savequery)
        # my_result = mysql_connection.fetchall()
        # db.commit()
        # mysql_connection.close()
        results = mysql_connection.execute(savequery, multi=True)
        for cur in results:
            if cur.with_rows:
                table_fetched = cur.fetchall()
                print("result:", table_fetched)
        db.commit()
        mysql_connection.close()

    def window_login():
        try:
            screen_register.destroy()
        except:
            pass

        global screen_login
        screen_login = Tk()
        screen_login.geometry("700x700")
        screen_login.title("login")
        # l_title = Label(text = "Travel reservation application", bg = "grey", width = "300", height = "2", font = ("Calibri", 13))
        Label(
            text="Travel reservation application",
            bg="grey",
            font=("Calibri", 13),
            width=65,
        ).grid(row=0, column=0, columnspan=3)
        Label(text="").grid(row=1, column=0)

        global var_login_email
        global var_login_password
        var_login_email = StringVar()
        var_login_password = StringVar()

        Label(text="Email").grid(row=2, column=0)
        Entry(screen_login, textvariable=var_login_email).grid(row=2, column=1)

        Label(text="Password").grid(row=3, column=0)
        Entry(screen_login, textvariable=var_login_password, show="*").grid(
            row=3, column=1
        )

        Button(text="Login", command=login).grid(row=4, column=1)
        Label(text="").grid(row=5)
        Label(text="Not registered yet?").grid(row=6, column=1)
        Button(text="Register", command=window_register).grid(row=7, column=1)

        global w_login_email
        global w_login_password
        w_login_email = Label(text="")
        w_login_email.grid(row=2, column=2)
        w_login_password = Label(text="")
        w_login_password.grid(row=3, column=2)

        Button(text="exit", command=lambda: exit_app(screen_login)).grid(
            row=8, column=1
        )
        screen_login.mainloop()

    def window_register():
        try:
            screen_login.destroy()
        except:
            pass
        global screen_register

        screen_register = Tk()
        screen_register.geometry("700x700")
        screen_register.title("register")

        Label(
            text="Travel reservation application",
            bg="grey",
            font=("Calibri", 13),
            width=65,
        ).grid(row=0, column=0, columnspan=3)
        Label(text="").grid(row=1, column=0)
        global var_register_fname
        global var_register_lname
        global var_register_email
        global var_register_password1
        global var_register_password2
        global var_register_phonenumber
        global var_register_customer
        global var_register_card_num
        global var_register_card_cvv
        global var_register_card_exp
        global var_register_owner

        var_register_fname = StringVar()
        var_register_lname = StringVar()
        var_register_email = StringVar()
        var_register_password1 = StringVar()
        var_register_password2 = StringVar()
        var_register_phonenumber = StringVar()
        var_register_customer = StringVar()
        var_register_card_num = StringVar()
        var_register_card_cvv = StringVar()
        var_register_card_exp = StringVar()
        var_register_owner = StringVar()

        Entry(width=35, textvariable=var_register_fname).grid(row=2, column=1)
        Entry(width=35, textvariable=var_register_lname).grid(row=3, column=1)
        Entry(width=35, textvariable=var_register_email).grid(row=4, column=1)
        Entry(width=35, textvariable=var_register_password1).grid(row=5, column=1)
        Entry(width=35, textvariable=var_register_password2).grid(row=6, column=1)
        Entry(width=35, textvariable=var_register_phonenumber).grid(row=7, column=1)
        Checkbutton(width=35, variable=var_register_customer).grid(row=8, column=1)
        Entry(width=35, textvariable=var_register_card_num).grid(row=9, column=1)
        Entry(width=35, textvariable=var_register_card_cvv).grid(row=10, column=1)
        Entry(width=35, textvariable=var_register_card_exp).grid(row=11, column=1)
        Checkbutton(width=35, variable=var_register_owner).grid(row=12, column=1)

        global w_register_fname
        global w_register_lname
        global w_register_email
        global w_register_password1
        global w_register_password2
        global w_register_phonenumber
        global w_register_customer
        global w_register_card_num
        global w_register_card_cvv
        global w_register_card_exp
        global w_register_owner

        w_register_fname = Label(text="")
        w_register_lname = Label(text="")
        w_register_email = Label(text="")
        w_register_password1 = Label(text="")
        w_register_password2 = Label(text="")
        w_register_phonenumber = Label(text="")
        w_register_customer = Label(text="")
        w_register_card_num = Label(text="")
        w_register_card_cvv = Label(text="")
        w_register_card_exp = Label(text="")
        w_register_owner = Label(text="")

        w_register_fname.grid(row=2, column=2)
        w_register_lname.grid(row=3, column=2)
        w_register_email.grid(row=4, column=2)
        w_register_password1.grid(row=5, column=2)
        w_register_password2.grid(row=6, column=2)
        w_register_phonenumber.grid(row=7, column=2)
        w_register_customer.grid(row=8, column=2)
        w_register_card_num.grid(row=9, column=2)
        w_register_card_cvv.grid(row=10, column=2)
        w_register_card_exp.grid(row=11, column=2)
        w_register_owner.grid(row=12, column=2)

        Label(text="first name").grid(row=2, column=0)
        Label(text="last name").grid(row=3, column=0)
        Label(text="email").grid(row=4, column=0)
        Label(text="password").grid(row=5, column=0)
        Label(text="confirm password").grid(row=6, column=0)
        Label(text="phone number").grid(row=7, column=0)
        Label(text="register as customer").grid(row=8, column=0)
        Label(text="credit card number").grid(row=9, column=0)
        Label(text="credit card cvv").grid(row=10, column=0)
        Label(text="credit card expiration date").grid(row=11, column=0)
        Label(text="register as owner").grid(row=12, column=0)

        Button(text="Register", command=register).grid(row=13, column=1)
        Label(text="").grid(row=14)
        Label(text="Already registered?").grid(row=15, column=1)
        Button(text="Login", command=window_login).grid(row=16, column=1)

        Button(text="exit", command=lambda: exit_app(screen_register)).grid(
            row=17, column=1
        )
        screen_register.mainloop()


# worked by arvind
if True:

    def exit_view_global():
        # bens screens
        try:
            screen_customer_rate_owner.destroy()
        except:
            pass
        try:
            screen_owner_add_property.destroy()
        except:
            pass
        try:
            screen_owner_remove_property.destroy()
        except:
            pass
        try:
            screen_owner_rate_customer.destroy()
        except:
            pass
        # jennas screens
        try:
            screen_process_date.destroy()
        except:
            pass
        try:
            screen_customer_view_flights.destroy()
        except:
            pass
        try:
            screen_customer_view_properties.destroy()
        except:
            pass
        try:
            screen_customer_view__reserved_properties.destroy()
        except:
            pass
        try:
            screen_delete_owner.destroy()
        except:
            pass
        try:
            screen_customer_cancel_properties.destroy()
        except:
            pass

        window_home()

    def window_home():
        try:
            screen_test.destroy()
        except:
            pass
        global screen_home
        screen_home = Tk()
        screen_home.geometry("700x700")
        screen_home.title("home")
        # l_title = Label(text = "Travel reservation application", bg = "grey", width = "300", height = "2", font = ("Calibri", 13))
        Label(
            text="Travel reservation application",
            bg="grey",
            font=("Calibri", 13),
            width=65,
        ).pack()
        Label(text="").pack()
        Label(text=f"welcome {current_email}").pack()

        # print(current_user_account_type)
        if "customer" in current_user_account_type:
            Label(text="customer options").pack()
            Button(text="book flight", command=window_customer_book_flight).pack()
            Button(text="cancel flight", command=window_c_cancel_flight).pack()
            Button(
                text="View flight bookings", command=window_customer_view_flights
            ).pack()
            Button(
                text="View Properies", command=window_customer_view_properties
            ).pack()
            Button(text="reserve property", command=window_test).pack()
            Button(
                text="Cancel property reservations",
                command=window_customer_cancel_property,
            ).pack()
            Button(
                text="View reserved properties",
                command=window_customer_view_reserved_properties,
            ).pack()

            Button(text="Review properties", command=window_c_rev_p).pack()
            Button(text="rate owners", command=window_customer_rate_owner).pack()
        if "owner" in current_user_account_type:
            Label(text="owner options").pack()
            Button(text="add property", command=window_owner_add_property).pack()
            Button(text="remove property", command=window_owner_remove_property).pack()
            Button(text="rate customers", command=window_owner_rate_customer).pack()
            Button(text="delete my account", command=window_delete_owner).pack()

        if "admin" in current_user_account_type:
            Label(text="admin options").pack()
            Button(text="schedule flight", command=window_a_sched_f).pack()
            Button(text="remove flight", command=window_admin_remove_flight).pack()
            Button(text="process date", command=window_process_date).pack()
            Button(text="view airports", command=window_a_view_airports).pack()
            Button(text="view airlines", command=window_a_view_airlines).pack()
            Button(text="view customers", command=window_a_view_customers).pack()
            Button(text="view owners", command=window_a_view_owners).pack()

        Button(text="log out", command=lambda: logout(screen_home)).pack()
        Button(text="exit", command=lambda: exit_app(screen_home)).pack()
        screen_home.mainloop()


# worked by arvind 2

if True:

    def window_customer_book_flight():
        def sort_by(col_index):
            # extract values from treeview, assign to list named subset
            subset = []
            for record in all_flights.get_children():
                subset.append(all_flights.item(record)["values"])

            print(col_index, len(subset[0]))
            # return None
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[col_index] for item in subset]) == (
                [item[col_index] for item in subset]
            ):
                subset.sort(key=lambda x: x[col_index] or 0, reverse=True)
                # clear tree view
                all_flights.delete(*all_flights.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    all_flights.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                            record[5],
                            record[6],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[col_index] or 0)
                # clear tree view
                all_flights.delete(*all_flights.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    all_flights.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                            record[5],
                            record[6],
                        ),
                    )
                    i += 1

        def acess_view_flight():
            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = (
                f"select * from view_flight_all where flight_date > '{current_date}'"
            )
            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()
            return table_fetched

        def check_flight_booking():
            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = f"select Flight.Flight_Date from Book join Flight on Book.Flight_Num = Flight.Flight_Num and Book.Airline_Name = Flight.Airline_Name WHERE Book.Was_Cancelled = 0 and Book.Customer = '{current_email}'"
            # savequery = f"select * from Book where Customer = '{current_email}' and Was_Cancelled <> 1"
            results = mysql_connection.execute(savequery, multi=True)
            table_fetched = []
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()
            return_table = []
            for i in table_fetched:
                return_table.append(str(i[0]))
            # if len(table_fetched) > 0:
            #     return True
            # else:
            #     return True
            return return_table

        def update_view(arg_1=None):
            calc_amount.config(text="")
            calc_flight_num.config(text="")
            w_customer_book_flight.config(text="")
            selected = all_flights.focus()
            values = []
            values = all_flights.item(selected, "values")
            print([values[2]])
            if [values] == [""]:
                w_customer_book_flight.config(text="select a flight")
                return None
            seats_to_book = var_seats_to_book.get()
            if not str.isdigit(seats_to_book):
                w_customer_book_flight.config(
                    text="enter valid number of seats to book"
                )
                return None

            try:
                amount_spent = float(values[5]) * float(seats_to_book)
            except:
                w_customer_book_flight.config(
                    text="enter valid number of seats to book"
                )
                return None

            if int(seats_to_book) > int(values[6]):
                w_customer_book_flight.config(
                    text="seats to book exceeds available number of seats available"
                )
                return None
            if values[2] in check_flight_booking():
                w_customer_book_flight.config(
                    text="you have an active booking on the same day, cant book two flights for same day"
                )
                return None
            calc_amount.config(text=f"{amount_spent}")
            calc_flight_num.config(text=f"{values[1]}")
            print([values])
            return True

        def book_flight_new():
            if update_view() != True:
                print("stopped in update view")
                return None

            seats_to_book = var_seats_to_book.get()
            selected = all_flights.focus()
            values = []
            values = all_flights.item(selected, "values")

            print(current_email, values[1], values[0], seats_to_book, current_date)

            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = f"call book_flight('{current_email}', '{values[1]}', '{values[0]}', {seats_to_book}, '{current_date}')"
            print(savequery)
            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()

            db.commit()
            mysql_connection.close()
            w_customer_book_flight.config(
                text=f"Booked sucessfully {seats_to_book} seats in flight {values[0]}{values[1]}"
            )

            all_flights.delete(*all_flights.get_children())
            # inserting data
            i = 0
            for record in acess_view_flight():
                all_flights.insert(
                    parent="",
                    index="end",
                    iid=i,
                    text="",
                    values=(
                        record[2],
                        record[0],
                        record[1],
                        record[3],
                        record[4],
                        record[5],
                        record[6],
                    ),
                )
                i += 1

            return None

        def exit_view():
            try:
                screen_customer_book_flight.destroy()
            except:
                pass
            window_home()

        try:
            screen_home.destroy()
        except:
            pass
        global screen_customer_book_flight
        screen_customer_book_flight = Tk()
        screen_customer_book_flight.geometry("1200x700")
        screen_customer_book_flight.title("test")

        # window title
        title_label = Label(
            screen_customer_book_flight, text="Customer Book Flight", font=(BOLD, 36)
        ).pack()

        # building treeview
        all_flights = ttk.Treeview(screen_customer_book_flight)
        tree_frame = Frame(screen_customer_book_flight)
        tree_frame.pack(pady=20)

        # make scroll bar
        vertscroll = ttk.Scrollbar(tree_frame, orient="vertical")
        vertscroll.pack(fill=Y, side="right")
        all_flights = ttk.Treeview(
            tree_frame,
            yscrollcommand=vertscroll.set,
            show="headings",
            selectmode="browse",
        )
        vertscroll.configure(command=all_flights.yview)
        all_flights.pack()

        columns_view_flight = {
            "airline": "Airline",
            "flight_id": "Flight Number",
            "flight_date": "Date of Departure",
            "source": "From Airport",
            "destination": "To Airport",
            "seat_cost": "Cost per seat",
            "num_empty_seats": "Available seats",
        }
        # define header names from sql database
        all_flights["columns"] = list(columns_view_flight.keys())

        # define column sizes
        for col_key in columns_view_flight:
            all_flights.column(col_key, width=150, minwidth=50, anchor=tkinter.CENTER)

        # define gui column headings based on database column headers
        all_flights.heading(
            "airline",
            text=columns_view_flight["airline"],
            anchor=tkinter.CENTER,
            command=lambda: sort_by(0),
        )
        all_flights.heading(
            "flight_id",
            text=columns_view_flight["flight_id"],
            anchor=tkinter.CENTER,
            command=lambda: sort_by(1),
        )
        all_flights.heading(
            "flight_date",
            text=columns_view_flight["flight_date"],
            anchor=tkinter.CENTER,
            command=lambda: sort_by(2),
        )
        all_flights.heading(
            "source",
            text=columns_view_flight["source"],
            anchor=tkinter.CENTER,
            command=lambda: sort_by(3),
        )
        all_flights.heading(
            "destination",
            text=columns_view_flight["destination"],
            anchor=tkinter.CENTER,
            command=lambda: sort_by(4),
        )
        all_flights.heading(
            "seat_cost",
            text=columns_view_flight["seat_cost"],
            anchor=tkinter.CENTER,
            command=lambda: sort_by(5),
        )
        all_flights.heading(
            "num_empty_seats",
            text=columns_view_flight["num_empty_seats"],
            anchor=tkinter.CENTER,
            command=lambda: sort_by(6),
        )

        # inserting data
        i = 0
        for record in acess_view_flight():
            all_flights.insert(
                parent="",
                index="end",
                iid=i,
                text="",
                values=(
                    record[2],
                    record[0],
                    record[1],
                    record[3],
                    record[4],
                    record[5],
                    record[6],
                ),
            )
            i += 1

        frame_2 = Frame(screen_customer_book_flight)
        frame_2.pack()

        global var_seats_to_book
        var_seats_to_book = StringVar()
        Label(frame_2, text="seats to book: ").grid(row=0, column=0)
        Label(frame_2, text="booked flight number: ").grid(row=1, column=0)
        Label(frame_2, text="Amount spent: ").grid(row=2, column=0)
        w_customer_book_flight = Label(frame_2, text="press calculate")
        w_customer_book_flight.grid(row=3, column=1)

        entry_seats_to_book = Entry(frame_2, width=35, textvariable=var_seats_to_book)
        entry_seats_to_book.grid(row=0, column=1)
        calc_flight_num = Label(frame_2, text="press calculate")
        calc_flight_num.grid(row=1, column=1)
        calc_amount = Label(frame_2, text="press calculate")
        calc_amount.grid(row=2, column=1)

        Button(frame_2, text="calculate", command=update_view).grid(row=0, column=2)

        Button(text="Submit", command=book_flight_new).pack()
        Button(text="back", command=exit_view).pack()
        screen_customer_book_flight.mainloop()

    def window_admin_remove_flight():
        def sort_by(col_index):
            # extract values from treeview, assign to list named subset
            subset = []
            for record in all_flights.get_children():
                subset.append(all_flights.item(record)["values"])

            print(col_index, len(subset[0]))
            # return None
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[col_index] for item in subset]) == (
                [item[col_index] for item in subset]
            ):
                subset.sort(key=lambda x: x[col_index] or 0, reverse=True)
                # clear tree view
                all_flights.delete(*all_flights.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    all_flights.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                            record[5],
                            record[6],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[col_index] or 0)
                # clear tree view
                all_flights.delete(*all_flights.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    all_flights.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                            record[5],
                            record[6],
                        ),
                    )
                    i += 1

        def acess_view_flight():
            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = (
                f"select * from view_flight_all where flight_date > '{current_date}'"
            )
            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()
            return table_fetched

        def remove_flight():
            selected = all_flights.focus()
            values = []
            values = all_flights.item(selected, "values")

            print(values[1], values[0], current_date)

            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = (
                f"call remove_flight('{values[1]}', '{values[0]}', '{current_date}')"
            )
            print(savequery)
            # return None
            # savequery = f"call book_flight('{current_email}', '{values[1]}', '{values[0]}', {seats_to_book}, '{current_date}')"
            print(savequery)
            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()

            db.commit()
            mysql_connection.close()
            reset_selected()
            return None

        def exit_view():
            try:
                screen_admin_remove_flight.destroy()
            except:
                pass
            window_home()

        def filter_selected():
            filtered_flights = []
            for record in acess_view_flight():
                filtered_flights.append(
                    [
                        record[2],
                        record[0],
                        record[1],
                        record[3],
                        record[4],
                        record[5],
                        record[6],
                    ]
                )

            text_from_date = var_from_date.get()
            text_to_date = var_to_date.get()
            text_airline = var_airline.get()
            text_flight_num = var_flight_num.get()

            print([text_from_date, text_to_date, text_airline, text_flight_num])

            for record in filtered_flights:
                print(record[1], int(record[1]), text_flight_num)

            if text_from_date == "":
                print("text from date is empty, not filtered")
            else:
                try:
                    print(datetime.strptime(text_from_date, "%Y-%m-%d"))
                    w_admin_remove_flight.config(text="")
                    filtered_flights = [
                        record
                        for record in filtered_flights
                        if str(record[2]) >= text_from_date
                    ]
                except:
                    w_admin_remove_flight.config(
                        text="enter a valid from date (YYYY-MM-DD) or leave empty"
                    )

            if text_to_date == "":
                print("text from date is empty, not filtered")
            else:
                try:
                    print(datetime.strptime(text_to_date, "%Y-%m-%d"))
                    w_admin_remove_flight.config(text="")
                    filtered_flights = [
                        record
                        for record in filtered_flights
                        if str(record[2]) <= text_to_date
                    ]
                except:
                    w_admin_remove_flight.config(
                        text="enter a valid to date (YYYY-MM-DD) or leave empty"
                    )

            if text_airline == "":
                print("text from airline empty, not filtered")
            else:
                filtered_flights = [
                    record
                    for record in filtered_flights
                    if text_airline.lower() in str(record[0]).lower()
                ]

            if text_flight_num == "":
                print("text from flight num empty, not filtered")
            else:
                try:
                    filtered_flights = [
                        record
                        for record in filtered_flights
                        if int(text_flight_num) == int(record[1])
                    ]
                except:
                    w_admin_remove_flight.config(
                        text="enter a valid flight number or leave empty"
                    )

            all_flights.delete(*all_flights.get_children())
            i = 0
            for record in filtered_flights:
                all_flights.insert(
                    "",
                    i,
                    text="",
                    values=(
                        record[0],
                        record[1],
                        record[2],
                        record[3],
                        record[4],
                        record[5],
                        record[6],
                    ),
                )
                i += 1

        def reset_selected():
            entry_from_date.delete(0, END)
            entry_to_date.delete(0, END)
            entry_airline.delete(0, END)
            entry_flight_num.delete(0, END)

            filtered_flights = []
            for record in acess_view_flight():
                filtered_flights.append(
                    [
                        record[2],
                        record[0],
                        record[1],
                        record[3],
                        record[4],
                        record[5],
                        record[6],
                    ]
                )
            all_flights.delete(*all_flights.get_children())
            i = 0
            for record in filtered_flights:
                all_flights.insert(
                    "",
                    i,
                    text="",
                    values=(
                        record[0],
                        record[1],
                        record[2],
                        record[3],
                        record[4],
                        record[5],
                        record[6],
                    ),
                )
                i += 1

        try:
            screen_home.destroy()
        except:
            pass
        global screen_admin_remove_flight
        screen_admin_remove_flight = Tk()
        screen_admin_remove_flight.geometry("1200x700")
        screen_admin_remove_flight.title("test")

        # window title
        title_label = Label(
            screen_admin_remove_flight, text="Customer Book Flight", font=(BOLD, 36)
        ).pack()

        frame_1 = Frame(screen_admin_remove_flight)
        frame_1.pack()

        var_from_date = StringVar()
        var_to_date = StringVar()
        var_airline = StringVar()
        var_flight_num = StringVar()

        Label(frame_1, text="dates (from - to): ").grid(row=0, column=0)
        Label(frame_1, text="Airline:").grid(row=1, column=0)
        Label(frame_1, text="Current date: ").grid(row=2, column=0)
        Label(frame_1, text="Flight number:").grid(row=3, column=0)

        Button(frame_1, text="Filter", command=filter_selected).grid(row=4, column=0)
        Button(frame_1, text="Reset", command=reset_selected).grid(row=5, column=0)
        Label(frame_1, text=f"{current_date}").grid(row=2, column=1)

        entry_from_date = Entry(frame_1, width=35, textvariable=var_from_date)
        entry_to_date = Entry(frame_1, width=35, textvariable=var_to_date)
        entry_airline = Entry(frame_1, width=35, textvariable=var_airline)
        entry_flight_num = Entry(frame_1, width=35, textvariable=var_flight_num)

        entry_from_date.grid(row=0, column=1)
        entry_to_date.grid(row=0, column=2)
        entry_airline.grid(row=1, column=1)
        entry_flight_num.grid(row=3, column=1)

        # building treeview
        all_flights = ttk.Treeview(screen_admin_remove_flight)
        tree_frame = Frame(screen_admin_remove_flight)
        tree_frame.pack(pady=20)

        # make scroll bar
        vertscroll = ttk.Scrollbar(tree_frame, orient="vertical")
        vertscroll.pack(fill=Y, side="right")
        all_flights = ttk.Treeview(
            tree_frame,
            yscrollcommand=vertscroll.set,
            show="headings",
            selectmode="browse",
        )
        vertscroll.configure(command=all_flights.yview)
        all_flights.pack()

        columns_view_flight = {
            "airline": "Airline",
            "flight_id": "Flight Number",
            "flight_date": "Date of Departure",
            "source": "From Airport",
            "destination": "To Airport",
            "seat_cost": "Cost per seat",
            "num_empty_seats": "Available seats",
        }
        # define header names from sql database
        all_flights["columns"] = list(columns_view_flight.keys())

        # define column sizes
        for col_key in columns_view_flight:
            all_flights.column(col_key, width=150, minwidth=50, anchor=tkinter.CENTER)

        # define gui column headings based on database column headers
        all_flights.heading(
            "airline",
            text=columns_view_flight["airline"],
            anchor=tkinter.CENTER,
            command=lambda: sort_by(0),
        )
        all_flights.heading(
            "flight_id",
            text=columns_view_flight["flight_id"],
            anchor=tkinter.CENTER,
            command=lambda: sort_by(1),
        )
        all_flights.heading(
            "flight_date",
            text=columns_view_flight["flight_date"],
            anchor=tkinter.CENTER,
            command=lambda: sort_by(2),
        )
        all_flights.heading(
            "source",
            text=columns_view_flight["source"],
            anchor=tkinter.CENTER,
            command=lambda: sort_by(3),
        )
        all_flights.heading(
            "destination",
            text=columns_view_flight["destination"],
            anchor=tkinter.CENTER,
            command=lambda: sort_by(4),
        )
        all_flights.heading(
            "seat_cost",
            text=columns_view_flight["seat_cost"],
            anchor=tkinter.CENTER,
            command=lambda: sort_by(5),
        )
        all_flights.heading(
            "num_empty_seats",
            text=columns_view_flight["num_empty_seats"],
            anchor=tkinter.CENTER,
            command=lambda: sort_by(6),
        )

        # inserting data
        i = 0
        for record in acess_view_flight():
            all_flights.insert(
                parent="",
                index="end",
                iid=i,
                text="",
                values=(
                    record[2],
                    record[0],
                    record[1],
                    record[3],
                    record[4],
                    record[5],
                    record[6],
                ),
            )
            i += 1

        frame_2 = Frame(screen_admin_remove_flight)
        frame_2.pack()

        # global var_seats_to_book
        # var_seats_to_book  = StringVar()
        # Label(frame_2,text = "seats to book: ").grid(row=0,column=0)
        # Label(frame_2,text = "booked flight number: ").grid(row=1,column=0)
        # Label(frame_2,text = "Amount spent: ").grid(row=2,column=0)
        w_admin_remove_flight = Label(frame_2, text="select a flight to remove")
        w_admin_remove_flight.grid(row=3, column=1)

        # entry_seats_to_book = Entry(frame_2,width=35,textvariable=var_seats_to_book)
        # entry_seats_to_book.grid(row=0,column=1)
        # calc_flight_num = Label(frame_2,text = "press calculate")
        # calc_flight_num.grid(row=1,column=1)
        # calc_amount = Label(frame_2,text = "press calculate")
        # calc_amount.grid(row=2,column=1)

        # Button(frame_2,text = "calculate",command=update_view).grid(row=0,column=2)

        Button(text="Remove selected flight", command=remove_flight).pack()
        Button(text="back", command=exit_view).pack()
        screen_admin_remove_flight.mainloop()

    def window_customer_cancel_flight():
        def sort_by(col_index):
            # extract values from treeview, assign to list named subset
            subset = []
            for record in all_flights.get_children():
                subset.append(all_flights.item(record)["values"])

            print(col_index, len(subset[0]))
            # return None
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[col_index] for item in subset]) == (
                [item[col_index] for item in subset]
            ):
                subset.sort(key=lambda x: x[col_index] or 0, reverse=True)
                # clear tree view
                all_flights.delete(*all_flights.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    all_flights.insert("", i, text="", values=(record))
                    i += 1
            else:
                subset.sort(key=lambda x: x[col_index] or 0)
                # clear tree view
                all_flights.delete(*all_flights.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    all_flights.insert("", i, text="", values=(record))
                    i += 1

        def acess_view_booked_flight():
            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = f"select Book.Flight_Num,Book.Airline_Name,From_Airport,To_Airport,Flight_Date,Book.Num_Seats,Num_Seats*Cost,Num_Seats*Cost*0.2 from Book join Flight on Book.Flight_Num = Flight.Flight_Num and Book.Airline_Name = Flight.Airline_Name WHERE Book.Was_Cancelled = 0 AND Book.Customer = '{current_email}' and Flight_date > '{current_date}'"
            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()
            print(table_fetched)
            return table_fetched

        def cancel_booked_flight():
            selected = all_flights.focus()
            values = []
            values = all_flights.item(selected, "values")

            print(values[1], values[0], current_date)

            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = f"call cancel_flight_booking('{current_email}', '{values[0]}', '{values[1]}', '{current_date}')"
            # savequery = f"call remove_flight('{values[1]}', '{values[0]}', '{current_date}')"
            print(savequery)
            # return None
            # savequery = f"call book_flight('{current_email}', '{values[1]}', '{values[0]}', {seats_to_book}, '{current_date}')"
            # print(savequery)
            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()

            db.commit()
            mysql_connection.close()
            reset_selected()
            return None

        def exit_view():
            try:
                screen_customer_cancel_flight.destroy()
            except:
                pass
            window_home()

        def filter_selected():
            filtered_flights = []
            for record in acess_view_booked_flight():
                filtered_flights.append(record)
            text_airline = var_airline.get()
            text_flight_num = var_flight_num.get()

            print([text_airline, text_flight_num])

            for record in filtered_flights:
                print(record[1], int(record[0]), text_flight_num)

            if text_airline == "":
                print("text from airline empty, not filtered")
            else:
                filtered_flights = [
                    record
                    for record in filtered_flights
                    if text_airline.lower() in str(record[1]).lower()
                ]

            if text_flight_num == "":
                print("text from flight num empty, not filtered")
            else:
                try:
                    filtered_flights = [
                        record
                        for record in filtered_flights
                        if int(text_flight_num) == int(record[0])
                    ]
                except:
                    w__customer_cancel_flight.config(
                        text="enter a valid flight number or leave empty"
                    )

            all_flights.delete(*all_flights.get_children())
            i = 0
            for record in filtered_flights:
                all_flights.insert(
                    "",
                    i,
                    text="",
                    values=(
                        record[0],
                        record[1],
                        record[2],
                        record[3],
                        record[4],
                        record[5],
                        record[6],
                    ),
                )
                i += 1

        def reset_selected():
            entry_airline.delete(0, END)
            entry_flight_num.delete(0, END)

            filtered_flights = []
            for record in acess_view_booked_flight():
                filtered_flights.append(
                    [
                        record[2],
                        record[0],
                        record[1],
                        record[3],
                        record[4],
                        record[5],
                        record[6],
                    ]
                )
            all_flights.delete(*all_flights.get_children())
            i = 0
            for record in filtered_flights:
                all_flights.insert(
                    "",
                    i,
                    text="",
                    values=(
                        record[0],
                        record[1],
                        record[2],
                        record[3],
                        record[4],
                        record[5],
                        record[6],
                    ),
                )
                i += 1

        try:
            screen_home.destroy()
        except:
            pass
        global screen_customer_cancel_flight
        screen_customer_cancel_flight = Tk()
        screen_customer_cancel_flight.geometry("1200x700")
        screen_customer_cancel_flight.title("test")

        # window title
        title_label = Label(
            screen_customer_cancel_flight, text="Customer Book Flight", font=(BOLD, 36)
        ).pack()

        frame_1 = Frame(screen_customer_cancel_flight)
        frame_1.pack()

        var_from_date = StringVar()
        var_to_date = StringVar()
        var_airline = StringVar()
        var_flight_num = StringVar()

        Label(frame_1, text="Airline:").grid(row=1, column=0)
        Label(frame_1, text="Current date: ").grid(row=2, column=0)
        Label(frame_1, text="Flight number:").grid(row=3, column=0)

        Button(frame_1, text="Filter", command=filter_selected).grid(row=4, column=0)
        Button(frame_1, text="Reset", command=reset_selected).grid(row=5, column=0)
        Label(frame_1, text=f"{current_date}").grid(row=2, column=1)

        entry_airline = Entry(frame_1, width=35, textvariable=var_airline)
        entry_flight_num = Entry(frame_1, width=35, textvariable=var_flight_num)

        entry_airline.grid(row=1, column=1)
        entry_flight_num.grid(row=3, column=1)

        # building treeview
        all_flights = ttk.Treeview(screen_customer_cancel_flight)
        tree_frame = Frame(screen_customer_cancel_flight)
        tree_frame.pack(pady=20)

        # make scroll bar
        vertscroll = ttk.Scrollbar(tree_frame, orient="vertical")
        vertscroll.pack(fill=Y, side="right")
        all_flights = ttk.Treeview(
            tree_frame,
            yscrollcommand=vertscroll.set,
            show="headings",
            selectmode="browse",
        )
        vertscroll.configure(command=all_flights.yview)
        all_flights.pack()

        columns_view_flight = {
            "flight_id": "Flight Number",
            "airline": "Airline",
            "source": "From Airport",
            "destination": "To Airport",
            "flight_date": "Date of Departure",
            "num_seats_booked": "Seats Booked",
            "sum_paid": "Amount Paid",
            "cancel_fee": "Cancellation fee",
        }
        # define header names from sql database
        all_flights["columns"] = list(columns_view_flight.keys())

        # define column sizes
        for col_key in columns_view_flight:
            all_flights.column(col_key, width=150, minwidth=50, anchor=tkinter.CENTER)

        # define gui column headings based on database column headers
        all_flights.heading(
            "flight_id",
            text=columns_view_flight["flight_id"],
            anchor=tkinter.CENTER,
            command=lambda: sort_by(0),
        )
        all_flights.heading(
            "airline",
            text=columns_view_flight["airline"],
            anchor=tkinter.CENTER,
            command=lambda: sort_by(1),
        )
        all_flights.heading(
            "source",
            text=columns_view_flight["source"],
            anchor=tkinter.CENTER,
            command=lambda: sort_by(2),
        )
        all_flights.heading(
            "destination",
            text=columns_view_flight["destination"],
            anchor=tkinter.CENTER,
            command=lambda: sort_by(3),
        )
        all_flights.heading(
            "flight_date",
            text=columns_view_flight["flight_date"],
            anchor=tkinter.CENTER,
            command=lambda: sort_by(4),
        )
        all_flights.heading(
            "num_seats_booked",
            text=columns_view_flight["num_seats_booked"],
            anchor=tkinter.CENTER,
            command=lambda: sort_by(5),
        )
        all_flights.heading(
            "sum_paid",
            text=columns_view_flight["sum_paid"],
            anchor=tkinter.CENTER,
            command=lambda: sort_by(6),
        )
        all_flights.heading(
            "cancel_fee",
            text=columns_view_flight["cancel_fee"],
            anchor=tkinter.CENTER,
            command=lambda: sort_by(7),
        )

        # inserting data
        i = 0
        for record in acess_view_booked_flight():
            all_flights.insert(parent="", index="end", iid=i, text="", values=record)
            i += 1

        frame_2 = Frame(screen_customer_cancel_flight)
        frame_2.pack()

        w__customer_cancel_flight = Label(frame_2, text="select a flight to remove")
        w__customer_cancel_flight.grid(row=3, column=1)

        Button(text="cancel booked flight", command=cancel_booked_flight).pack()
        Button(text="back", command=exit_view).pack()
        screen_customer_cancel_flight.mainloop()

    # window_admin_remove_flight()
    # print(acess_view_flight())

    # window_customer_book_flight()
    # # print(acess_view_flight())

    # window_customer_cancel_flight()

# worked by kenji done1
if True:

    # done 1
    def window_a_sched_f():

        # save list of airlines for combobox
        airlines = []

        try:
            screen_home.destroy()
        except:
            pass

        def exit_view():
            try:
                screen_a_sched_f.destroy()
            except:
                pass
            window_home()

        def get_airlines():
            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = f"SELECT Airline_Name FROM Airline"
            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()
                    # print('result:',table_fetched

            for record in table_fetched:
                airlines.append(record[0])
            if len(table_fetched) == 1:
                return True
            else:
                return False

        def schedule_flight():

            # airline name and airport id checks
            def check_airline(airline_name):

                db = mysql.connector.connect(**connection_config_dict)
                mysql_connection = db.cursor()
                savequery = f"call check_airline_name('{airline_name}')"
                results = mysql_connection.execute(savequery, multi=True)
                for cur in results:
                    if cur.with_rows:
                        table_fetched = cur.fetchall()
                        # print('result:',table_fetched
                if len(table_fetched) == 1:
                    return True
                else:
                    return False

            def check_airport(airport_id):
                db = mysql.connector.connect(**connection_config_dict)
                mysql_connection = db.cursor()
                savequery = f"call check_airport_id('{airport_id}')"
                results = mysql_connection.execute(savequery, multi=True)
                for cur in results:
                    if cur.with_rows:
                        table_fetched = cur.fetchall()
                        # print('result:',table_fetched )
                if len(table_fetched) == 1:
                    return True
                else:
                    return False

            # checking inputs
            if e_flight_num.get() == "" or len(e_flight_num.get()) > 5:
                messagebox.showwarning("Warning", "Invalid flight number!")
                return None
            elif (
                e_airline_name.get() == ""
                or check_airline(e_airline_name.get()) == False
            ):
                messagebox.showwarning("Warning", "Invalid airline name!")
                return None
            elif (
                e_from_airport.get() == ""
                or check_airport(e_from_airport.get()) == False
            ):
                messagebox.showwarning("Warning", "Invalid from airport!")
                return None
            elif e_to_airport.get() == "" or check_airport(e_to_airport.get()) == False:
                messagebox.showwarning("Warning", "Invalid to airport!")
                return None
            elif (
                e_dep_time.get() == ""
                or len(e_dep_time.get()) != 8
                or not re.match(
                    r"^([0-2][0-3]|[0-1][0-9]):[0-5][0-9]+:[0-5][0-9]+$",
                    e_dep_time.get(),
                )
            ):
                messagebox.showwarning(
                    "Warning", "Must enter valid departure time in format HH:MM:SS!"
                )
                return None
            elif (
                e_arr_time.get() == ""
                or len(e_arr_time.get()) != 8
                or not re.match(
                    r"^([0-2][0-3]|[0-1][0-9]):[0-5][0-9]+:[0-5][0-9]+$",
                    e_arr_time.get(),
                )
                or time.strptime(e_dep_time.get(), "%H:%M:%S")
                > time.strptime(e_arr_time.get(), "%H:%M:%S")
            ):
                messagebox.showwarning(
                    "Warning",
                    "Must enter valid arrival time later than departure time in format HH:MM:SS!",
                )
                return None
            elif e_flight_date.get() == "" or datetime.strptime(
                e_flight_date.get(), "%Y-%M-%d"
            ) < datetime.strptime(current_date, "%Y-%M-%d"):
                messagebox.showwarning(
                    "Warning",
                    "Must enter flight date later than current date in format YYYY-MM-DD!",
                )
                return None
            elif (
                e_cost.get() == ""
                or not re.match(r"\d+.?\d{2}", e_cost.get())
                or re.match(r"[A-Za-z]+", e_cost.get())
            ):
                messagebox.showwarning("Warning", "Must enter valid cost!")
                return None
            elif e_capacity.get() == "" or not re.match(r"^\d+$", e_capacity.get()):
                messagebox.showwarning(
                    "Warning", "Must enter an integer for flight capacity!"
                )
                return None
            # execute the query only if inputs are all valid
            else:
                db = mysql.connector.connect(**connection_config_dict)
                mysql_connection = db.cursor()
                savequery = f"call schedule_flight(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                savevalues = (
                    e_flight_num.get(),
                    e_airline_name.get(),
                    e_from_airport.get(),
                    e_to_airport.get(),
                    e_dep_time.get(),
                    e_arr_time.get(),
                    e_flight_date.get(),
                    e_cost.get(),
                    e_capacity.get(),
                    current_date,
                )
                print([savequery], savevalues)
                mysql_connection.execute(savequery, savevalues)
                db.commit()
                mysql_connection.close()
                messagebox.showinfo("Schedule Flight", "Flight successfully scheduled!")

        screen_a_sched_f = tkinter.Tk()
        screen_a_sched_f.geometry("900x400")

        # text
        title_label = Label(
            screen_a_sched_f, text="Admin Schedule Flight", font=(BOLD, 36)
        ).grid(row=0, column=0, columnspan=2)
        l_flight_num = Label(screen_a_sched_f, text="Flight Number").grid(
            row=1, column=0, sticky=E, padx=10, pady=5
        )
        l_airline_name = Label(screen_a_sched_f, text="Airline").grid(
            row=2, column=0, sticky=E, padx=10, pady=5
        )
        l_from_airport = Label(screen_a_sched_f, text="From Airport").grid(
            row=3, column=0, sticky=E, padx=10, pady=5
        )
        l_to_airport = Label(screen_a_sched_f, text="To Airport").grid(
            row=4, column=0, sticky=E, padx=10, pady=5
        )
        l_dep_time = Label(screen_a_sched_f, text="Departure Time").grid(
            row=5, column=0, sticky=E, padx=10, pady=5
        )
        l_arr_time = Label(screen_a_sched_f, text="Arrival Time").grid(
            row=6, column=0, sticky=E, padx=10, pady=5
        )
        l_flight_date = Label(screen_a_sched_f, text="Flight Date").grid(
            row=1, column=4, sticky=E, padx=10, pady=5
        )
        l_cost = Label(screen_a_sched_f, text="$ Per Person").grid(
            row=2, column=4, sticky=E, padx=10, pady=5
        )
        l_capacity = Label(screen_a_sched_f, text="Capacity").grid(
            row=3, column=4, sticky=E, padx=10, pady=5
        )
        l_current_date = Label(screen_a_sched_f, text="Current Date").grid(
            row=4, column=4, sticky=E, padx=10, pady=5
        )

        # entry boxes
        e_flight_num = Entry(screen_a_sched_f)
        e_flight_num.grid(row=1, column=1, padx=10, pady=5)
        get_airlines()
        e_airline_name = ttk.Combobox(screen_a_sched_f, values=airlines)
        e_airline_name.grid(row=2, column=1, padx=10, pady=5)
        e_from_airport = Entry(screen_a_sched_f)
        e_from_airport.grid(row=3, column=1, padx=10, pady=5)
        e_to_airport = Entry(screen_a_sched_f)
        e_to_airport.grid(row=4, column=1, padx=10, pady=5)
        e_dep_time = Entry(screen_a_sched_f)
        e_dep_time.grid(row=5, column=1, padx=10, pady=5)
        e_arr_time = Entry(screen_a_sched_f)
        e_arr_time.grid(row=6, column=1, padx=10, pady=5)
        e_flight_date = Entry(screen_a_sched_f)
        e_flight_date.grid(row=1, column=5, padx=10, pady=5)
        e_cost = Entry(screen_a_sched_f)
        e_cost.grid(row=2, column=5, padx=10, pady=5)
        e_capacity = Entry(screen_a_sched_f)
        e_capacity.grid(row=3, column=5, padx=10, pady=5)
        e_current_date = Entry(screen_a_sched_f)
        e_current_date.insert(0, current_date)
        e_current_date.config(state="disabled")
        e_current_date.grid(row=4, column=5, padx=10, pady=5)

        # buttons
        schedule_button = Button(
            screen_a_sched_f, text="Schedule", command=schedule_flight
        )
        schedule_button.grid(row=8, column=4, pady=50)
        cancel_button = Button(screen_a_sched_f, text="Back", command=exit_view)
        cancel_button.grid(row=8, column=1, pady=50)

        # test
        # schedule_flight('2','Delta Airlines', 'ATL','LAX','13:00:00','14:00:00','2021-10-21',666,100,'2021-01-01')

        screen_a_sched_f.mainloop()

    # done 1
    def window_a_view_airlines():

        try:
            screen_home.destroy()
        except:
            pass

        def exit_view():
            try:
                screen_a_view_airlines.destroy()
            except:
                pass
            window_home()

        def sort_by_name():
            # extract values from treeview, assign to list named subset
            subset = []
            for record in a_view_alines.get_children():
                subset.append(a_view_alines.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[0] for item in subset]) == ([item[0] for item in subset]):
                subset.sort(key=lambda x: x[0] or 0, reverse=True)
                # clear tree view
                a_view_alines.delete(*a_view_alines.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_alines.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[0] or 0)
                # clear tree view
                a_view_alines.delete(*a_view_alines.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_alines.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                        ),
                    )
                    i += 1

        def sort_by_rating():
            # extract values from treeview, assign to list named subset
            subset = []
            for record in a_view_alines.get_children():
                subset.append(a_view_alines.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[1] for item in subset]) == ([item[1] for item in subset]):
                subset.sort(key=lambda x: x[1] or 0, reverse=True)
                # clear tree view
                a_view_alines.delete(*a_view_alines.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_alines.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[1] or 0)
                # clear tree view
                a_view_alines.delete(*a_view_alines.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_alines.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                        ),
                    )
                    i += 1

        def sort_by_total_flights():
            # extract values from treeview, assign to list named subset
            subset = []
            for record in a_view_alines.get_children():
                subset.append(a_view_alines.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[2] for item in subset]) == ([item[2] for item in subset]):
                subset.sort(key=lambda x: x[2] or 0, reverse=True)
                # clear tree view
                a_view_alines.delete(*a_view_alines.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_alines.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[2] or 0)
                # clear tree view
                a_view_alines.delete(*a_view_alines.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_alines.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                        ),
                    )
                    i += 1

        def sort_by_min_cost():
            # extract values from treeview, assign to list named subset
            subset = []
            for record in a_view_alines.get_children():
                subset.append(a_view_alines.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[3] for item in subset]) == ([item[3] for item in subset]):
                subset.sort(key=lambda x: x[3] or 0, reverse=True)
                # clear tree view
                a_view_alines.delete(*a_view_alines.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_alines.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[3] or 0)
                # clear tree view
                a_view_alines.delete(*a_view_alines.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_alines.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                        ),
                    )
                    i += 1

        def filter_id(*args):
            name_query = content.get()
            subset = []
            # loop over content list of tree view, and match text with input airport name query and append to the list "subset"
            for record in a_view_alines_list:
                if name_query.lower() in record[0].lower():
                    # print(record)
                    subset.append(record)
            # clear tree view
            a_view_alines.delete(*a_view_alines.get_children())

            # insert values into treeview
            i = 0
            for record in subset:
                a_view_alines.insert(
                    "",
                    i,
                    text="",
                    values=(
                        record[0],
                        record[1],
                        record[2],
                        record[3],
                    ),
                )
                i += 1

        a_view_alines_list = []

        def view_airlines():
            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = f"SELECT * FROM view_airlines"
            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()
                    # print('result:',table_fetched )
            i = 0
            for record in table_fetched:
                a_view_alines_list.append(record)
                a_view_alines.insert(
                    parent="",
                    index="end",
                    iid=i,
                    text="",
                    values=(
                        record[0],
                        record[1],
                        record[2],
                        record[3],
                    ),
                )
                i += 1
            if len(table_fetched) == 1:
                return True
            else:
                return False

        screen_a_view_airlines = tkinter.Tk()

        screen_a_view_airlines.geometry("800x600")

        # window title
        title_label = Label(
            screen_a_view_airlines, text="Admin View Airlines", font=(BOLD, 36)
        ).pack()

        # building treeview
        a_view_alines = ttk.Treeview(screen_a_view_airlines)
        tree_frame = Frame(screen_a_view_airlines)
        tree_frame.pack(pady=20)

        # make scroll bar
        vertscroll = ttk.Scrollbar(tree_frame, orient="vertical")
        vertscroll.pack(fill=Y, side="right")
        a_view_alines = ttk.Treeview(
            tree_frame,
            yscrollcommand=vertscroll.set,
            show="headings",
            selectmode="browse",
        )
        vertscroll.configure(command=a_view_alines.yview)
        a_view_alines.pack()

        # define header names from sql database
        a_view_alines["columns"] = (
            "Airline_Name",
            "Rating",
            "Total_Flights",
            "Min_Flight_Cost",
        )

        # define column sizes
        a_view_alines.column(
            "Airline_Name", width=150, minwidth=50, anchor=tkinter.CENTER
        )
        a_view_alines.column("Rating", width=70, minwidth=50, anchor=tkinter.CENTER)
        a_view_alines.column(
            "Total_Flights", width=100, minwidth=50, anchor=tkinter.CENTER
        )
        a_view_alines.column(
            "Min_Flight_Cost", width=200, minwidth=50, anchor=tkinter.CENTER
        )

        # define gui column headings based on database column headers
        a_view_alines.heading(
            "Airline_Name", text="Name", anchor=tkinter.CENTER, command=sort_by_name
        )
        a_view_alines.heading(
            "Rating", text="Rating", anchor=tkinter.CENTER, command=sort_by_rating
        )
        a_view_alines.heading(
            "Total_Flights",
            text="Total Flights",
            anchor=tkinter.CENTER,
            command=sort_by_total_flights,
        )
        a_view_alines.heading(
            "Min_Flight_Cost",
            text="Minimum Flight Cost",
            anchor=tkinter.CENTER,
            command=sort_by_min_cost,
        )

        # buttons
        filter_button = Button(screen_a_view_airlines, text="Filter", command=filter_id)
        filter_button.pack()
        back_button = Button(screen_a_view_airlines, text="Back", command=exit_view)
        back_button.pack(pady=5)

        # entry box for writing review

        id_text = Label(screen_a_view_airlines, text="Filter by Airline Name:")
        id_text.pack(pady=10)
        content = Entry(
            screen_a_view_airlines,
        )
        content.pack()

        view_airlines()

        screen_a_view_airlines.mainloop()

    # done 1
    def window_a_view_airports():

        try:
            screen_home.destroy()
        except:
            pass

        def exit_view():
            try:
                screen_a_view_airports.destroy()
            except:
                pass
            window_home()

        def sort_by_id():
            # extract values from treeview
            subset = []
            for record in a_view_aports.get_children():
                subset.append(a_view_aports.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[0] for item in subset]) == ([item[0] for item in subset]):
                subset.sort(key=lambda x: x[0] or 0, reverse=True)
                # clear tree view
                a_view_aports.delete(*a_view_aports.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_aports.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                            record[5],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[0] or 0)
                # clear tree view
                a_view_aports.delete(*a_view_aports.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_aports.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                            record[5],
                        ),
                    )
                    i += 1

        def sort_by_airport_name():
            # extract values from treeview
            subset = []
            for record in a_view_aports.get_children():
                subset.append(a_view_aports.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[1] for item in subset]) == ([item[1] for item in subset]):
                subset.sort(key=lambda x: x[1] or 0, reverse=True)
                # clear tree view
                a_view_aports.delete(*a_view_aports.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_aports.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                            record[5],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[1] or 0)
                # clear tree view
                a_view_aports.delete(*a_view_aports.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_aports.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                            record[5],
                        ),
                    )
                    i += 1

        def sort_by_tz():
            # extract values from treeview
            subset = []
            for record in a_view_aports.get_children():
                subset.append(a_view_aports.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[2] for item in subset]) == ([item[2] for item in subset]):
                subset.sort(key=lambda x: x[2] or 0, reverse=True)
                # clear tree view
                a_view_aports.delete(*a_view_aports.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_aports.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                            record[5],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[2] or 0)
                # clear tree view
                a_view_aports.delete(*a_view_aports.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_aports.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                            record[5],
                        ),
                    )
                    i += 1

        def sort_by_total_arriving():
            # extract values from treeview
            subset = []
            for record in a_view_aports.get_children():
                subset.append(a_view_aports.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[3] for item in subset]) == ([item[3] for item in subset]):
                subset.sort(key=lambda x: x[3] or 0, reverse=True)
                # clear tree view
                a_view_aports.delete(*a_view_aports.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_aports.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                            record[5],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[3] or 0)
                # clear tree view
                a_view_aports.delete(*a_view_aports.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_aports.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                            record[5],
                        ),
                    )
                    i += 1

        def sort_by_total_departing():
            # extract values from treeview
            subset = []
            for record in a_view_aports.get_children():
                subset.append(a_view_aports.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[4] for item in subset]) == ([item[4] for item in subset]):
                subset.sort(key=lambda x: x[4] or 0, reverse=True)
                # clear tree view
                a_view_aports.delete(*a_view_aports.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_aports.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                            record[5],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[4] or 0)
                # clear tree view
                a_view_aports.delete(*a_view_aports.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_aports.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                            record[5],
                        ),
                    )
                    i += 1

        def sort_by_avg_cost_departing():
            # extract values from treeview
            subset = []
            for record in a_view_aports.get_children():
                subset.append(a_view_aports.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[5] for item in subset]) == ([item[5] for item in subset]):
                subset.sort(key=lambda x: x[5] or 0, reverse=True)
                # clear tree view
                a_view_aports.delete(*a_view_aports.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_aports.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                            record[5],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[5] or 0)
                # clear tree view
                a_view_aports.delete(*a_view_aports.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_aports.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                            record[5],
                        ),
                    )
                    i += 1

        def filter_id(*args):
            id_query = content.get()
            subset = []
            # loop over content list of tree view, and match text with input name query and append to the list "subset"
            for record in a_view_aports_list:
                if id_query.lower() in record[0].lower():
                    # print(record)
                    subset.append(record)
            # clear tree view
            a_view_aports.delete(*a_view_aports.get_children())

            # insert values into treeview
            i = 0
            for record in subset:
                a_view_aports.insert(
                    "",
                    i,
                    text="",
                    values=(
                        record[0],
                        record[1],
                        record[2],
                        record[3],
                        record[4],
                        record[5],
                    ),
                )
                i += 1

        def filter_tz(*args):
            tz_query = tz.get()
            subset = []
            # loop over content list of tree view, and match text with input name query and append to the list "subset"
            for record in a_view_aports_list:
                if tz_query.lower() in record[2].lower():
                    # print(record)
                    subset.append(record)
            # clear tree view
            a_view_aports.delete(*a_view_aports.get_children())

            # insert values into treeview
            i = 0
            for record in subset:
                a_view_aports.insert(
                    "",
                    i,
                    text="",
                    values=(
                        record[0],
                        record[1],
                        record[2],
                        record[3],
                        record[4],
                        record[4],
                    ),
                )
                i += 1

        a_view_aports_list = []

        def view_airports():
            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = f"SELECT * FROM view_airports"
            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()
                    # print('result:',table_fetched )
            i = 0
            for record in table_fetched:
                a_view_aports_list.append(record)
                a_view_aports.insert(
                    parent="",
                    index="end",
                    iid=i,
                    text="",
                    values=(
                        record[0],
                        record[1],
                        record[2],
                        record[3],
                        record[4],
                        record[5],
                    ),
                )
                i += 1
            if len(table_fetched) == 1:
                return True
            else:
                return False

        screen_a_view_airports = tkinter.Tk()

        screen_a_view_airports.geometry("800x600")

        # window title
        title_label = Label(
            screen_a_view_airports, text="Admin View Airport", font=(BOLD, 36)
        )
        title_label.pack()

        # building treeview
        a_view_aports = ttk.Treeview(screen_a_view_airports)
        tree_frame = Frame(screen_a_view_airports)
        tree_frame.pack(pady=20)

        # make scroll bar
        vertscroll = ttk.Scrollbar(tree_frame, orient="vertical")
        vertscroll.pack(fill=Y, side="right")
        a_view_aports = ttk.Treeview(
            tree_frame,
            yscrollcommand=vertscroll.set,
            show="headings",
            selectmode="browse",
        )
        vertscroll.configure(command=a_view_aports.yview)
        a_view_aports.pack()

        # define header names from sql database
        a_view_aports["columns"] = (
            "Airport_Id",
            "Airport_Name",
            "Time_Zone",
            "Total_Arriving_Flights",
            "Total_Departing_Flights",
            "Avg_Departing_Flight_Cost",
        )

        # define column sizes
        a_view_aports.column(
            "Airport_Id", width=100, minwidth=50, anchor=tkinter.CENTER
        )
        a_view_aports.column(
            "Airport_Name", width=200, minwidth=50, anchor=tkinter.CENTER
        )
        a_view_aports.column("Time_Zone", width=100, minwidth=50, anchor=tkinter.CENTER)
        a_view_aports.column(
            "Total_Arriving_Flights", width=100, minwidth=50, anchor=tkinter.CENTER
        )
        a_view_aports.column(
            "Total_Departing_Flights", width=100, minwidth=50, anchor=tkinter.CENTER
        )
        a_view_aports.column(
            "Avg_Departing_Flight_Cost", width=100, minwidth=50, anchor=tkinter.CENTER
        )

        # define gui column headings based on database column headers
        a_view_aports.heading(
            "Airport_Id", text="Airport ID", anchor=tkinter.CENTER, command=sort_by_id
        )
        a_view_aports.heading(
            "Airport_Name",
            text="Airport Name",
            anchor=tkinter.CENTER,
            command=sort_by_airport_name,
        )
        a_view_aports.heading(
            "Time_Zone", text="Time Zone", anchor=tkinter.CENTER, command=sort_by_tz
        )
        a_view_aports.heading(
            "Total_Arriving_Flights",
            text="Total Arriving Flights",
            anchor=tkinter.CENTER,
            command=sort_by_total_arriving,
        )
        a_view_aports.heading(
            "Total_Departing_Flights",
            text="Total Departing Flights",
            anchor=tkinter.CENTER,
            command=sort_by_total_departing,
        )
        a_view_aports.heading(
            "Avg_Departing_Flight_Cost",
            text="Avg Departing Flight Cost",
            anchor=tkinter.CENTER,
            command=sort_by_avg_cost_departing,
        )

        # buttons
        filter_button = Button(screen_a_view_airports, text="Filter", command=filter_id)
        filter_button.pack()
        back_button = Button(screen_a_view_airports, text="Back", command=exit_view)
        back_button.pack()

        # entry box for writing review
        tz_text = Label(screen_a_view_airports, text="Time Zone:")
        tz_text.pack()
        tz = ttk.Combobox(
            screen_a_view_airports,
            values=["", "EST", "CST", "HST", "MST", "PST"],
            state="readonly",
        )
        tz.pack(pady=10)
        tz.bind("<<ComboboxSelected>>", filter_tz)
        id_text = Label(screen_a_view_airports, text="Filter by Airport ID:")
        id_text.pack(pady=10)
        content = Entry(
            screen_a_view_airports,
        )
        content.pack()

        view_airports()

        screen_a_view_airports.mainloop()

    # done 1
    def window_a_view_customers():

        try:
            screen_home.destroy()
        except:
            pass

        def exit_view():
            try:
                screen_a_view_customers.destroy()
            except:
                pass
            window_home()

        def sort_by_name():
            # extract values from treeview, assign to list named subset
            subset = []
            for record in a_view_customers.get_children():
                subset.append(a_view_customers.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[0] for item in subset]) == ([item[0] for item in subset]):
                subset.sort(key=lambda x: x[0] or 0, reverse=True)
                # clear tree view
                a_view_customers.delete(*a_view_customers.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_customers.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[0] or 0)
                # clear tree view
                a_view_customers.delete(*a_view_customers.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_customers.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                        ),
                    )
                    i += 1

        def sort_by_rating():
            # extract values from treeview, assign to list named subset
            subset = []
            for record in a_view_customers.get_children():
                subset.append(a_view_customers.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[1] for item in subset]) == ([item[1] for item in subset]):
                subset.sort(key=lambda x: x[1] or 0, reverse=True)
                # clear tree view
                a_view_customers.delete(*a_view_customers.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_customers.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[1] or 0)
                # clear tree view
                a_view_customers.delete(*a_view_customers.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_customers.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                        ),
                    )
                    i += 1

        def sort_by_location():
            # extract values from treeview, assign to list named subset
            subset = []
            for record in a_view_customers.get_children():
                subset.append(a_view_customers.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[2] for item in subset]) == ([item[2] for item in subset]):
                subset.sort(key=lambda x: x[2] or 0, reverse=True)
                # clear tree view
                a_view_customers.delete(*a_view_customers.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_customers.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[2] or 0)
                # clear tree view
                a_view_customers.delete(*a_view_customers.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_customers.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                        ),
                    )
                    i += 1

        def sort_by_is_owner():
            # extract values from treeview, assign to list named subset
            subset = []
            for record in a_view_customers.get_children():
                subset.append(a_view_customers.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[3] for item in subset]) == ([item[3] for item in subset]):
                subset.sort(key=lambda x: x[3] or 0, reverse=True)
                # clear tree view
                a_view_customers.delete(*a_view_customers.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_customers.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[3] or 0)
                # clear tree view
                a_view_customers.delete(*a_view_customers.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_customers.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                        ),
                    )
                    i += 1

        def sort_by_total_seats():
            # extract values from treeview, assign to list named subset
            subset = []
            for record in a_view_customers.get_children():
                subset.append(a_view_customers.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[4] for item in subset]) == ([item[4] for item in subset]):
                subset.sort(key=lambda x: x[4] or 0, reverse=True)
                # clear tree view
                a_view_customers.delete(*a_view_customers.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_customers.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[4] or 0)
                # clear tree view
                a_view_customers.delete(*a_view_customers.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_customers.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                        ),
                    )
                    i += 1

        def view_customers():
            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = f"SELECT * FROM view_customers"
            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()
                    # print('result:',table_fetched )
            i = 0
            for record in table_fetched:
                a_view_customers_list.append(record)
                a_view_customers.insert(
                    parent="",
                    index="end",
                    iid=i,
                    text="",
                    values=(
                        record[0],
                        record[1],
                        record[2],
                        record[3],
                        record[4],
                    ),
                )
                i += 1
            if len(table_fetched) == 1:
                return True
            else:
                return False

        # shows only rows where text input matches some part of name
        def onKeyRelease(*args):
            name_query = input_box.get()
            subset = []
            # loop over content list of tree view, and match text with input name query and append to the list "subset"
            for record in a_view_customers_list:
                if name_query.lower() in record[0].lower():
                    # print(record)
                    subset.append(record)
            # clear tree view
            a_view_customers.delete(*a_view_customers.get_children())

            # insert values into treeview
            i = 0
            for record in subset:
                a_view_customers.insert(
                    "",
                    i,
                    text="",
                    values=(record[0], record[1], record[2], record[3], record[4]),
                )
                i += 1

        screen_a_view_customers = tkinter.Tk()
        screen_a_view_customers.geometry("800x400")

        a_view_customers_list = []

        # window title
        title = Label(
            screen_a_view_customers,
            text="Admin View Customers",
            pady=20,
            font=("Arial", 24, "bold"),
        )
        title.pack()
        # building treeview
        a_view_customers = ttk.Treeview(screen_a_view_customers)
        tree_frame = Frame(screen_a_view_customers)
        tree_frame.pack(pady=20)
        # make scroll bar
        vertscroll = ttk.Scrollbar(tree_frame, orient="vertical")
        vertscroll.pack(fill=Y, side="right")
        a_view_customers = ttk.Treeview(
            tree_frame,
            yscrollcommand=vertscroll.set,
            show="headings",
            selectmode="browse",
        )
        vertscroll.configure(command=a_view_customers.yview)
        a_view_customers.pack()
        # define header names from sql database
        a_view_customers["columns"] = (
            "customer_name",
            "avg_rating",
            "location",
            "is_owner",
            "total_seats_purchased",
        )
        # define column sizes
        a_view_customers.column(
            "customer_name", width=150, minwidth=50, anchor=tkinter.CENTER
        )
        a_view_customers.column(
            "avg_rating", width=150, minwidth=50, anchor=tkinter.CENTER
        )
        a_view_customers.column(
            "location", width=150, minwidth=50, anchor=tkinter.CENTER
        )
        a_view_customers.column(
            "is_owner", width=100, minwidth=50, anchor=tkinter.CENTER
        )
        a_view_customers.column(
            "total_seats_purchased", width=200, minwidth=50, anchor=tkinter.CENTER
        )

        # [no sort version] define gui column headings and function triggers based on database column headers
        a_view_customers.heading(
            "customer_name",
            text="Full Name",
            anchor=tkinter.CENTER,
            command=sort_by_name,
        )
        a_view_customers.heading(
            "avg_rating",
            text="Average Rating",
            anchor=tkinter.CENTER,
            command=sort_by_rating,
        )
        a_view_customers.heading(
            "location",
            text="Current Location",
            anchor=tkinter.CENTER,
            command=sort_by_location,
        )
        a_view_customers.heading(
            "is_owner",
            text="Is Owner?",
            anchor=tkinter.CENTER,
            command=sort_by_is_owner,
        )
        a_view_customers.heading(
            "total_seats_purchased",
            text="Total Seats Purchased",
            command=sort_by_total_seats,
        )

        # entry box for triggers to filter treeview
        text = Label(screen_a_view_customers, text="Filter:  Full Name")
        text.pack()
        input_box = Entry(
            screen_a_view_customers,
        )
        input_box.bind("<KeyRelease>", onKeyRelease)
        input_box.pack()

        view_customers()

        Button(text="Back", command=exit_view).pack()
        screen_a_view_customers.mainloop()

    # done 1
    def window_a_view_owners():

        try:
            screen_home.destroy()
        except:
            pass

        def exit_view():
            try:
                screen_a_view_owners.destroy()
            except:
                pass
            window_home()

        def sort_by_name():
            # extract values from treeview, assign to list named subset
            subset = []
            for record in a_view_owners.get_children():
                subset.append(a_view_owners.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[0] for item in subset]) == ([item[0] for item in subset]):
                subset.sort(key=lambda x: x[0] or 0, reverse=True)
                # clear tree view
                a_view_owners.delete(*a_view_owners.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_owners.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[0] or 0)
                # clear tree view
                a_view_owners.delete(*a_view_owners.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_owners.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                        ),
                    )
                    i += 1

        def sort_by_rating():
            # extract values from treeview, assign to list named subset
            subset = []
            for record in a_view_owners.get_children():
                subset.append(a_view_owners.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[1] for item in subset]) == ([item[1] for item in subset]):
                subset.sort(key=lambda x: x[1] or 0, reverse=True)
                # clear tree view
                a_view_owners.delete(*a_view_owners.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_owners.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[1] or 0)
                # clear tree view
                a_view_owners.delete(*a_view_owners.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_owners.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                        ),
                    )
                    i += 1

        def sort_by_num_owned_prop():
            # extract values from treeview, assign to list named subset
            subset = []
            for record in a_view_owners.get_children():
                subset.append(a_view_owners.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[2] for item in subset]) == ([item[2] for item in subset]):
                subset.sort(key=lambda x: x[2] or 0, reverse=True)
                # clear tree view
                a_view_owners.delete(*a_view_owners.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_owners.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[2] or 0)
                # clear tree view
                a_view_owners.delete(*a_view_owners.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_owners.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                        ),
                    )
                    i += 1

        def sort_by_avg_prop_rating():
            # extract values from treeview, assign to list named subset
            subset = []
            for record in a_view_owners.get_children():
                subset.append(a_view_owners.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[3] for item in subset]) == ([item[3] for item in subset]):
                subset.sort(key=lambda x: x[3] or 0, reverse=True)
                # clear tree view
                a_view_owners.delete(*a_view_owners.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_owners.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[3] or 0)
                # clear tree view
                a_view_owners.delete(*a_view_owners.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_owners.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                        ),
                    )
                    i += 1

        def sort_by_total_seats():
            # extract values from treeview, assign to list named subset
            subset = []
            for record in a_view_owners.get_children():
                subset.append(a_view_owners.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[4] for item in subset]) == ([item[4] for item in subset]):
                subset.sort(key=lambda x: x[4] or 0, reverse=True)
                # clear tree view
                a_view_owners.delete(*a_view_owners.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_owners.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[4] or 0)
                # clear tree view
                a_view_owners.delete(*a_view_owners.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    a_view_owners.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                        ),
                    )
                    i += 1

        def view_owners():
            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = f"SELECT * FROM view_owners"
            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()
                    # print('result:',table_fetched )
            i = 0
            for record in table_fetched:
                a_view_owners_list.append(record)
                a_view_owners.insert(
                    parent="",
                    index="end",
                    iid=i,
                    text="",
                    values=(
                        record[0],
                        record[1],
                        record[2],
                        record[3],
                    ),
                )
                i += 1
            if len(table_fetched) == 1:
                return True
            else:
                return False

        # shows only rows where text input matches some part of name
        def onKeyRelease(*args):
            name_query = input_box.get()
            subset = []
            # loop over content list of tree view, and match text with input name query and append to the list "subset"
            for record in a_view_owners_list:
                if name_query.lower() in record[0].lower():
                    # print(record)
                    subset.append(record)
            # clear tree view
            a_view_owners.delete(*a_view_owners.get_children())

            # insert values into treeview
            i = 0
            for record in subset:
                a_view_owners.insert(
                    "",
                    i,
                    text="",
                    values=(
                        record[0],
                        record[1],
                        record[2],
                        record[3],
                    ),
                )
                i += 1

        screen_a_view_owners = tkinter.Tk()
        screen_a_view_owners.geometry("800x400")

        a_view_owners_list = []

        # window title
        title = Label(
            screen_a_view_owners,
            text="Admin View owners",
            pady=20,
            font=("Arial", 24, "bold"),
        )
        title.pack()
        # building treeview
        a_view_owners = ttk.Treeview(screen_a_view_owners)
        tree_frame = Frame(screen_a_view_owners)
        tree_frame.pack(pady=20)
        # make scroll bar
        vertscroll = ttk.Scrollbar(tree_frame, orient="vertical")
        vertscroll.pack(fill=Y, side="right")
        a_view_owners = ttk.Treeview(
            tree_frame,
            yscrollcommand=vertscroll.set,
            show="headings",
            selectmode="browse",
        )
        vertscroll.configure(command=a_view_owners.yview)
        a_view_owners.pack()
        # define header names from sql database
        a_view_owners["columns"] = (
            "owner_name",
            "avg_rating",
            "num_properties_owned",
            "avg_property_rating",
        )
        # define column sizes
        a_view_owners.column(
            "owner_name", width=150, minwidth=50, anchor=tkinter.CENTER
        )
        a_view_owners.column(
            "avg_rating", width=150, minwidth=50, anchor=tkinter.CENTER
        )
        a_view_owners.column(
            "num_properties_owned", width=150, minwidth=50, anchor=tkinter.CENTER
        )
        a_view_owners.column(
            "avg_property_rating", width=100, minwidth=50, anchor=tkinter.CENTER
        )

        # [no sort version] define gui column headings and function triggers based on database column headers
        a_view_owners.heading(
            "owner_name", text="Full Name", anchor=tkinter.CENTER, command=sort_by_name
        )
        a_view_owners.heading(
            "avg_rating",
            text="Average Rating",
            anchor=tkinter.CENTER,
            command=sort_by_rating,
        )
        a_view_owners.heading(
            "num_properties_owned",
            text="Number of Properties Owned",
            anchor=tkinter.CENTER,
            command=sort_by_num_owned_prop,
        )
        a_view_owners.heading(
            "avg_property_rating",
            text="Average Property Rating",
            anchor=tkinter.CENTER,
            command=sort_by_avg_prop_rating,
        )

        # entry box for triggers to filter treeview
        text = Label(screen_a_view_owners, text="Filter:  Full Name")
        text.pack()
        input_box = Entry(
            screen_a_view_owners,
        )
        input_box.bind("<KeyRelease>", onKeyRelease)
        input_box.pack()

        view_owners()
        Button(text="Back", command=exit_view).pack()
        screen_a_view_owners.mainloop()

    # done 1
    def window_c_cancel_flight():

        try:
            screen_home.destroy()
        except:
            pass

        def exit_view():
            try:
                screen_c_cancel_flight.destroy()
            except:
                pass
            window_home()

        def sort_by_airline():
            # extract values from treeview, assign to list named subset
            subset = []
            for record in c_review_p.get_children():
                subset.append(c_review_p.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[0] for item in subset]) == ([item[0] for item in subset]):
                subset.sort(key=lambda x: x[0] or 0, reverse=True)
                # clear tree view
                c_review_p.delete(*c_review_p.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    c_review_p.insert(
                        "",
                        i,
                        text="",
                        values=(record[0], record[1], record[2], record[3]),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[0] or 0)
                # clear tree view
                c_review_p.delete(*c_review_p.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    c_review_p.insert(
                        "",
                        i,
                        text="",
                        values=(record[0], record[1], record[2], record[3]),
                    )
                    i += 1

        def sort_by_flight_num():
            # extract values from treeview, assign to list named subset
            subset = []
            for record in c_review_p.get_children():
                subset.append(c_review_p.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[1] for item in subset]) == ([item[1] for item in subset]):
                subset.sort(key=lambda x: x[1] or 0, reverse=True)
                # clear tree view
                c_review_p.delete(*c_review_p.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    c_review_p.insert(
                        "",
                        i,
                        text="",
                        values=(record[0], record[1], record[2], record[3]),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[1] or 0)
                # clear tree view
                c_review_p.delete(*c_review_p.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    c_review_p.insert(
                        "",
                        i,
                        text="",
                        values=(record[0], record[1], record[2], record[3]),
                    )
                    i += 1

        def sort_by_flight_date():
            # extract values from treeview, assign to list named subset
            subset = []
            for record in c_review_p.get_children():
                subset.append(c_review_p.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[2] for item in subset]) == ([item[2] for item in subset]):
                subset.sort(key=lambda x: x[2] or 0, reverse=True)
                # clear tree view
                c_review_p.delete(*c_review_p.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    c_review_p.insert(
                        "",
                        i,
                        text="",
                        values=(record[0], record[1], record[2], record[3]),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[2] or 0)
                # clear tree view
                c_review_p.delete(*c_review_p.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    c_review_p.insert(
                        "",
                        i,
                        text="",
                        values=(record[0], record[1], record[2], record[3]),
                    )
                    i += 1

        def check_active_flight_bookings():

            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = f"SELECT * FROM view_active_flight_bookings"
            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()
                    # print('result:',table_fetched )
            i = 0
            for record in table_fetched:
                # check for matching customer email from query to current logged in user email
                if record[3] == current_email:
                    c_review_p.insert(
                        parent="",
                        index="end",
                        iid=i,
                        text="",
                        values=(record[0], record[1], record[2], record[3]),
                    )
                    i += 1
                else:
                    print(
                        f"Query retrieved record[3] = {record[3]} but did not display. current_email = {current_email}"
                    )
            if len(table_fetched) == 1:
                return True
            else:
                return False

        def cancel_flight():
            # extracting values from selected treeview record
            selected = c_review_p.focus()
            values = c_review_p.item(selected, "values")
            if len(values) == 0:
                messagebox.showwarning("Warning", "Please select a valid row")
                return None
            selected_airline_name = values[0]
            selected_flight_number = values[1]
            selected_flight_date = values[2]
            selected_email = values[3]
            if selected_email != current_email:
                messagebox.showwarning(
                    "Warning",
                    "Current logged in user email does not match selected reservation's customer email",
                )
                return None
            elif datetime.strptime(
                selected_flight_date, "%Y-%M-%d"
            ) < datetime.strptime(current_date, "%Y-%M-%d"):
                messagebox.showwarning(
                    "Warning", "Flight date must be in the future in format YYYY-MM-DD!"
                )
                print(
                    f"selected_flight_date = {selected_flight_date}, current_date = {current_date}"
                )
                return None
            else:
                # calling procedure to insert values into sql database
                db = mysql.connector.connect(**connection_config_dict)
                mysql_connection = db.cursor()
                savequery = f"call cancel_flight_booking(%s,%s,%s,%s)"
                savevalues = (
                    current_email,
                    selected_flight_number,
                    selected_airline_name,
                    current_date,
                )
                # print([savequery])
                mysql_connection.execute(savequery, savevalues)
                db.commit()
                mysql_connection.close()
                messagebox.showinfo(
                    "Cancel Flight Booking", "Cancellation successfully submitted!"
                )
                exit_view()

        screen_c_cancel_flight = tkinter.Tk()

        screen_c_cancel_flight.geometry("800x600")

        # window title
        title_label = Label(
            screen_c_cancel_flight, text="Customer Cancel Flight", font=(BOLD, 36)
        ).pack()

        # building treeview
        c_review_p = ttk.Treeview(screen_c_cancel_flight)
        tree_frame = Frame(screen_c_cancel_flight)
        tree_frame.pack(pady=20)

        # make scroll bar
        vertscroll = ttk.Scrollbar(tree_frame, orient="vertical")
        vertscroll.pack(fill=Y, side="right")
        c_review_p = ttk.Treeview(
            tree_frame,
            yscrollcommand=vertscroll.set,
            show="headings",
            selectmode="browse",
        )
        vertscroll.configure(command=c_review_p.yview)
        c_review_p.pack()

        # define header names from sql database
        c_review_p["columns"] = (
            "Airline_Name",
            "Flight_Number",
            "Flight_Date",
            "Customer_Email",
        )
        c_review_p["displaycolumns"] = ("Airline_Name", "Flight_Number", "Flight_Date")

        # define column sizes
        c_review_p.column("Airline_Name", width=150, minwidth=50, anchor=tkinter.CENTER)
        c_review_p.column(
            "Flight_Number", width=150, minwidth=50, anchor=tkinter.CENTER
        )
        c_review_p.column("Flight_Date", width=150, minwidth=50, anchor=tkinter.CENTER)

        # define gui column headings based on database column headers
        c_review_p.heading(
            "Airline_Name",
            text="Airline Name",
            anchor=tkinter.CENTER,
            command=sort_by_airline,
        )
        c_review_p.heading(
            "Flight_Number",
            text="Flight Number",
            anchor=tkinter.CENTER,
            command=sort_by_flight_num,
        )
        c_review_p.heading(
            "Flight_Date",
            text="Flight Date",
            anchor=tkinter.CENTER,
            command=sort_by_flight_date,
        )

        # buttons
        submit_button = Button(
            screen_c_cancel_flight, text="Submit", command=cancel_flight
        )
        submit_button.pack()
        back_button = Button(screen_c_cancel_flight, text="Back", command=exit_view)
        back_button.pack()

        check_active_flight_bookings()

        screen_c_cancel_flight.mainloop()

    # done 1
    def window_c_rev_p():

        try:
            screen_home.destroy()
        except:
            pass

        def exit_view():
            try:
                screen_c_rev_p.destroy()
            except:
                pass
            window_home()

        def sort_by_date():
            # extract values from treeview, assign to list named subset
            subset = []
            for record in c_review_p.get_children():
                subset.append(c_review_p.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[0] for item in subset]) == ([item[0] for item in subset]):
                subset.sort(key=lambda x: x[0] or 0, reverse=True)
                # clear tree view
                c_review_p.delete(*c_review_p.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    c_review_p.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[0] or 0)
                # clear tree view
                c_review_p.delete(*c_review_p.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    c_review_p.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                        ),
                    )
                    i += 1

        def sort_by_property_name():
            # extract values from treeview, assign to list named subset
            subset = []
            for record in c_review_p.get_children():
                subset.append(c_review_p.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[1] for item in subset]) == ([item[1] for item in subset]):
                subset.sort(key=lambda x: x[1] or 0, reverse=True)
                # clear tree view
                c_review_p.delete(*c_review_p.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    c_review_p.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[1] or 0)
                # clear tree view
                c_review_p.delete(*c_review_p.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    c_review_p.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                        ),
                    )
                    i += 1

        def sort_by_owner():
            # extract values from treeview, assign to list named subset
            subset = []
            for record in c_review_p.get_children():
                subset.append(c_review_p.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[2] for item in subset]) == ([item[2] for item in subset]):
                subset.sort(key=lambda x: x[2] or 0, reverse=True)
                # clear tree view
                c_review_p.delete(*c_review_p.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    c_review_p.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[2] or 0)
                # clear tree view
                c_review_p.delete(*c_review_p.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    c_review_p.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                        ),
                    )
                    i += 1

        def sort_by_address():
            # extract values from treeview, assign to list named subset
            subset = []
            for record in c_review_p.get_children():
                subset.append(c_review_p.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[3] for item in subset]) == ([item[3] for item in subset]):
                subset.sort(key=lambda x: x[3] or 0, reverse=True)
                # clear tree view
                c_review_p.delete(*c_review_p.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    c_review_p.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[3] or 0)
                # clear tree view
                c_review_p.delete(*c_review_p.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    c_review_p.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                        ),
                    )
                    i += 1

        def check_property_needs_review():

            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = f"SELECT * FROM view_property_needs_review"
            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()
                    # print('result:',table_fetched )
            i = 0
            for record in table_fetched:
                # check for matching customer email from query to current logged in user email
                if record[4] == current_email:
                    c_review_p.insert(
                        parent="",
                        index="end",
                        iid=i,
                        text="",
                        values=(record[0], record[1], record[2], record[3], record[4]),
                    )
                    i += 1
                else:
                    print(
                        f"Query retrieved record[4] = {record[4]} but did not display. current_email = {current_email}"
                    )
            if len(table_fetched) == 1:
                return True
            else:
                return False

        def review_property():
            # extracting values from selected record
            selected = c_review_p.focus()
            values = c_review_p.item(selected, "values")
            if len(values) == 0:
                messagebox.showwarning("Warning", "Please select a valid row")
                return None
            selected_date = values[0]
            selected_property_name = values[1]
            selected_owner_email = values[2]
            selected_address = values[3]
            selected_email = values[4]
            # Conditions for submission to be accepted
            if selected_email != current_email:
                messagebox.showwarning(
                    "Warning",
                    "Current logged in user email does not match selected reservation's customer email",
                )
                return None
            elif datetime.strptime(selected_date, "%Y-%M-%d") <= datetime.strptime(
                current_date, "%Y-%M-%d"
            ):
                messagebox.showwarning("Warning", "cant review future reservations")
                return None
            elif score.get() == "":
                messagebox.showwarning(
                    "Warning", "Select a score from 1-5 from the dropdown!"
                )
                return None
            elif content.get("1.0", "end-1c") == "":
                messagebox.showwarning("Warning", "Review cannot be empty!")
                return None
            else:
                # calling procedure to insert values into sql database
                db = mysql.connector.connect(**connection_config_dict)
                mysql_connection = db.cursor()
                savequery = f"call customer_review_property(%s,%s,%s,%s,%s,%s)"
                savevalues = (
                    selected_property_name,
                    selected_owner_email,
                    current_email,
                    content.get("1.0", "end-1c"),
                    score.get(),
                    current_date,
                )
                # print([savequery])
                mysql_connection.execute(savequery, savevalues)
                db.commit()
                mysql_connection.close()
                messagebox.showinfo("Review Property", "Review successfully submitted!")

        screen_c_rev_p = tkinter.Tk()

        screen_c_rev_p.geometry("800x600")

        # window title
        title_label = Label(
            screen_c_rev_p, text="Customer Review Property", font=(BOLD, 36)
        ).pack()

        # building treeview
        c_review_p = ttk.Treeview(screen_c_rev_p)
        tree_frame = Frame(screen_c_rev_p)
        tree_frame.pack(pady=20)

        # make scroll bar
        vertscroll = ttk.Scrollbar(tree_frame, orient="vertical")
        vertscroll.pack(fill=Y, side="right")
        c_review_p = ttk.Treeview(
            tree_frame,
            yscrollcommand=vertscroll.set,
            show="headings",
            selectmode="browse",
        )
        vertscroll.configure(command=c_review_p.yview)
        c_review_p.pack()

        # define header names from sql database
        c_review_p["columns"] = (
            "Start_Date",
            "Property_Name",
            "Owner_Email",
            "Address",
            "Customer_Email",
        )
        c_review_p["displaycolumns"] = (
            "Start_Date",
            "Property_Name",
            "Owner_Email",
            "Address",
        )

        # define column sizes
        c_review_p.column("Start_Date", width=150, minwidth=50, anchor=tkinter.CENTER)
        c_review_p.column(
            "Property_Name", width=150, minwidth=50, anchor=tkinter.CENTER
        )
        c_review_p.column("Owner_Email", width=150, minwidth=50, anchor=tkinter.CENTER)
        c_review_p.column("Address", width=150, minwidth=50, anchor=tkinter.CENTER)

        # define gui column headings based on database column headers
        c_review_p.heading(
            "Start_Date", text="Start Date", anchor=tkinter.CENTER, command=sort_by_date
        )
        c_review_p.heading(
            "Property_Name",
            text="Property Name",
            anchor=tkinter.CENTER,
            command=sort_by_property_name,
        )
        c_review_p.heading(
            "Owner_Email",
            text="Owner Email",
            anchor=tkinter.CENTER,
            command=sort_by_owner,
        )
        c_review_p.heading(
            "Address", text="Address", anchor=tkinter.CENTER, command=sort_by_address
        )

        # buttons
        submit_button = Button(screen_c_rev_p, text="Submit", command=review_property)
        submit_button.pack()
        back_button = Button(screen_c_rev_p, text="Back", command=exit_view)
        back_button.pack()

        # entry box for writing review
        score_text = Label(screen_c_rev_p, text="Score:").pack()
        score = ttk.Combobox(screen_c_rev_p, values=[1, 2, 3, 4, 5], state="readonly")
        score.pack(pady=10)
        content_text = Label(screen_c_rev_p, text="Review:")
        content_text.pack(pady=10)
        content = Text(
            screen_c_rev_p,
        )
        content.pack(fill="both", expand=True)

        check_property_needs_review()

        screen_c_rev_p.mainloop()

    # window_a_sched_f()

    # window_a_view_airlines()

    # window_a_view_airports()

    # window_a_view_customers()

    # window_a_view_owners()

    # # for testing Customer_cancel_flight:
    # current_email = 'aray@tiktok.com'
    # window_c_cancel_flight()

    # for testing Customer_review_property:
    # current_email = 'cbing10@gmail.com'
    # window_c_rev_p()

# worked by ben done 1
if True:

    """
    CUSTOMER RATE OWNER
    """
    # done 1
    if True:

        def return_possible_rate_owners():
            # create cursor and initialize
            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = (
                "select Start_Date, r.Owner_Email, r.Property_Name, concat(street,' ',city,' ',state,' ',zip) "
                "from (Reserve as r join Property as p on r.Property_Name = p.Property_Name) "
                "left outer join Customers_Rate_Owners as cro on r.Customer = cro.Customer "
                f"where score is null and was_cancelled = 0 and End_Date < '{current_date}' and r.Customer = '{current_email}'"
            )

            print(savequery)
            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()
            mysql_connection.close()
            return table_fetched

        def window_customer_rate_owner():

            try:
                screen_home.destroy()
            except:
                pass
            global screen_customer_rate_owner
            screen_customer_rate_owner = Tk()
            screen_customer_rate_owner.geometry("1100x700")
            screen_customer_rate_owner.title("Customer Rate Owner")

            # Title
            Label(screen_customer_rate_owner, text="Customer Rate Owner").grid(
                row=0, column=0, columnspan=5
            )

            # Table parameters
            global var_customer_rate_owner_list
            var_customer_rate_owner_list = return_possible_rate_owners()
            print(var_customer_rate_owner_list)

            col_names = (
                "Reservation Date",
                "Owner Email",
                "Property Name",
                "Address",
                "Rating",
            )
            num_rows = len(var_customer_rate_owner_list)
            if num_rows != 0:
                num_cols = len(var_customer_rate_owner_list[0])
            else:
                num_cols = 0
            offset = 1
            w = 25
            h = 2

            # Create Columns
            for j, name in enumerate(col_names):
                table_customer_rate_owner = Text(
                    screen_customer_rate_owner, state="normal", width=w, height=h
                )
                table_customer_rate_owner.grid(row=offset, column=j)
                table_customer_rate_owner.insert("end", name)
                table_customer_rate_owner.configure(state="disabled")
            offset += 1

            # Insert data
            for i in range(num_rows):
                for j in range(num_cols):
                    table_customer_rate_owner = Text(
                        screen_customer_rate_owner,
                        state="normal",
                        wrap=WORD,
                        width=w,
                        height=h,
                    )
                    table_customer_rate_owner.grid(row=i + offset, column=j)
                    table_customer_rate_owner.insert(
                        "end", var_customer_rate_owner_list[i][j]
                    )
                    table_customer_rate_owner.configure(state="disabled")

            # Insert textbox for customer
            global var_customer_rate_owner_score
            var_customer_rate_owner_score = []
            for i in range(num_rows):
                var_num_seat = StringVar()
                var_customer_rate_owner_score.append((i, var_num_seat))
                num_seat = Entry(screen_customer_rate_owner, textvariable=var_num_seat)
                num_seat.grid(row=i + offset, column=4, ipadx=w * 1.6, ipady=8)
            offset += num_rows

            # Two Buttons: Back and Submit
            Button(text="Back", command=exit_view_global).grid(
                row=offset, column=0, pady=(100, 0)
            )
            Button(text="Submit", command=customer_rate_owner_submit).grid(
                row=offset, column=4, pady=(100, 0)
            )
            offset += 1

            # Error Message
            global w_customer_rate_owner_error
            w_customer_rate_owner_error = Label(text="")
            w_customer_rate_owner_error.grid(row=offset, column=4)

            screen_customer_rate_owner.mainloop()

        def customer_rate_owner_submit():
            # Add the rating to the database
            valid_score = []
            for i, score in var_customer_rate_owner_score:
                if len(score.get()) != 0 and not customer_rate_owner_check_score(
                    score.get()
                ):
                    return None
                elif len(score.get()) != 0 and customer_rate_owner_check_score(
                    score.get()
                ):
                    valid_score.append(
                        (i, int(score.get()), var_customer_rate_owner_list[i][1])
                    )

            # No rating submitted
            if len(valid_score) == 0:
                w_customer_rate_owner_error.config(
                    text="Please rate at least one owner"
                )
                return None

            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()

            for i, score, owner_email in valid_score:
                savequery = f"call customer_rates_owner('{current_email}', '{owner_email}', {score}, '{current_date}')"
                mysql_connection.execute(savequery, multi=True)
                db.commit()
            mysql_connection.close()

            # Show a message for successful rating
            messagebox.showinfo(
                title="Thank You!", message="Your rating has been submitted"
            )
            screen_customer_rate_owner.destroy()
            window_home()

        def customer_rate_owner_check_score(score):
            try:
                score = int(score)
            except:
                w_customer_rate_owner_error.config(
                    text="Must enter a number for the score"
                )
                return False

            if 1 <= score <= 5:
                return True

            w_customer_rate_owner_error.config(
                text="Must enter a number between 1 and 5"
            )
            return False

    """
    OWNER ADD PROPERTY
    """
    # done 1
    if True:

        def window_owner_add_property():
            try:
                screen_home.destroy()
            except:
                pass
            global screen_owner_add_property
            screen_owner_add_property = Tk()
            screen_owner_add_property.geometry("700x700")
            screen_owner_add_property.title("Owner Add Property")

            states = [
                "AK",
                "AL",
                "AR",
                "AZ",
                "CA",
                "CO",
                "CT",
                "DC",
                "DE",
                "FL",
                "GA",
                "HI",
                "IA",
                "ID",
                "IL",
                "IN",
                "KS",
                "KY",
                "LA",
                "MA",
                "MD",
                "ME",
                "MI",
                "MN",
                "MO",
                "MS",
                "MT",
                "NC",
                "ND",
                "NE",
                "NH",
                "NJ",
                "NM",
                "NV",
                "NY",
                "OH",
                "OK",
                "OR",
                "PA",
                "RI",
                "SC",
                "SD",
                "TN",
                "TX",
                "UT",
                "VA",
                "VT",
                "WA",
                "WI",
                "WV",
                "WY",
            ]

            # Labels for the texts
            Label(text="Owner Add Property").grid(row=0, column=0, columnspan=2)
            Label(text="Name:").grid(row=1, column=0)
            Label(text="Description:").grid(row=2, column=0)
            Label(text="Street:").grid(row=3, column=0)
            Label(text="City:").grid(row=4, column=0)
            Label(text="State:").grid(row=5, column=0)
            Label(text="Zip:").grid(row=6, column=0)
            Label(text="Nearest Airport:").grid(row=7, column=0)
            Label(text="Dist To Airpot:").grid(row=8, column=0)
            Label(text="Capacity:").grid(row=9, column=0)
            Label(text="Cost:").grid(row=10, column=0)

            global var_add_property_name
            global var_add_property_description
            global var_add_property_street
            global var_add_property_city
            global var_add_property_state
            global var_add_property_zip
            global var_add_property_nearest
            global var_add_property_dist
            global var_add_property_capacity
            global var_add_property_cost

            var_add_property_name = StringVar()
            var_add_property_description = StringVar()
            var_add_property_street = StringVar()
            var_add_property_city = StringVar()
            var_add_property_state = StringVar()
            var_add_property_zip = StringVar()
            var_add_property_nearest = StringVar()
            var_add_property_dist = StringVar()
            var_add_property_capacity = StringVar()
            var_add_property_cost = StringVar()

            # Entry boxes for info
            Entry(width=35, textvariable=var_add_property_name).grid(row=1, column=1)
            Entry(width=35, textvariable=var_add_property_description).grid(
                row=2, column=1
            )
            Entry(width=35, textvariable=var_add_property_street).grid(row=3, column=1)
            Entry(width=35, textvariable=var_add_property_city).grid(row=4, column=1)
            Entry(width=35, textvariable=var_add_property_zip).grid(row=6, column=1)
            Entry(width=35, textvariable=var_add_property_nearest).grid(row=7, column=1)
            Entry(width=35, textvariable=var_add_property_dist).grid(row=8, column=1)
            Entry(width=35, textvariable=var_add_property_capacity).grid(
                row=9, column=1
            )
            Entry(width=35, textvariable=var_add_property_cost).grid(row=10, column=1)

            # Error messages
            global w_owner_add_property_name_error
            global w_owner_add_property_description_error
            global w_owner_add_property_street_error
            global w_owner_add_property_city_error
            global w_owner_add_property_state_error
            global w_owner_add_property_zip_error
            global w_owner_add_property_nearest_error
            global w_owner_add_property_dist_error
            global w_owner_add_property_capacity_error
            global w_owner_add_property_cost_error

            w_owner_add_property_name_error = Label(text="")
            w_owner_add_property_description_error = Label(text="")
            w_owner_add_property_street_error = Label(text="")
            w_owner_add_property_city_error = Label(text="")
            w_owner_add_property_state_error = Label(text="")
            w_owner_add_property_zip_error = Label(text="")
            w_owner_add_property_nearest_error = Label(text="")
            w_owner_add_property_dist_error = Label(text="")
            w_owner_add_property_capacity_error = Label(text="")
            w_owner_add_property_cost_error = Label(text="")

            w_owner_add_property_name_error.grid(row=1, column=2)
            w_owner_add_property_description_error.grid(row=2, column=2)
            w_owner_add_property_street_error.grid(row=3, column=2)
            w_owner_add_property_city_error.grid(row=4, column=2)
            w_owner_add_property_state_error.grid(row=5, column=2)
            w_owner_add_property_zip_error.grid(row=6, column=2)
            w_owner_add_property_nearest_error.grid(row=7, column=2)
            w_owner_add_property_dist_error.grid(row=8, column=2)
            w_owner_add_property_capacity_error.grid(row=9, column=2)
            w_owner_add_property_cost_error.grid(row=10, column=2)

            # Insert State dropdown menu
            var_add_property_state.set("NULL")  # default value
            airline = OptionMenu(
                screen_owner_add_property, var_add_property_state, *states
            )
            airline.grid(row=5, column=1)

            # Two buttons at the bottom
            Button(text="Cancel", command=exit_view_global).grid(
                row=11, column=0, pady=20
            )
            Button(text="Add", command=owner_add_property_add).grid(
                row=11, column=1, pady=20
            )

            screen_owner_add_property.mainloop()

        def owner_add_property_add():
            # Reset error messages
            w_owner_add_property_name_error.config(text="")
            w_owner_add_property_description_error.config(text="")
            w_owner_add_property_street_error.config(text="")
            w_owner_add_property_city_error.config(text="")
            w_owner_add_property_state_error.config(text="")
            w_owner_add_property_zip_error.config(text="")
            w_owner_add_property_nearest_error.config(text="")
            w_owner_add_property_dist_error.config(text="")
            w_owner_add_property_capacity_error.config(text="")
            w_owner_add_property_cost_error.config(text="")

            name = var_add_property_name.get()
            description = var_add_property_description.get()
            street = var_add_property_street.get()
            city = var_add_property_city.get()
            state = var_add_property_state.get()
            zip = var_add_property_zip.get()
            nearest = var_add_property_nearest.get()
            dist = var_add_property_dist.get()
            capacity = var_add_property_capacity.get()
            cost = var_add_property_cost.get()

            # Add property to the database if conditions are met
            if not owner_add_property_check_name(name):
                return None
            elif not owner_add_property_check_description(description):
                return None
            elif not owner_add_property_check_street(street):
                return None
            elif not owner_add_property_check_city(city):
                return None
            elif not owner_add_property_check_state(state):
                return None
            elif not owner_add_property_check_zip(zip):
                return None
            elif not owner_add_property_check_nearest(nearest):
                return None
            elif not owner_add_property_check_dist(dist):
                return None
            elif not owner_add_property_check_capacity(capacity):
                return None
            elif not owner_add_property_check_cost(cost):
                return None

            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = (
                f"call add_property('{name}', '{current_email}', '{description}', '{capacity}', '{cost}', "
                f"'{street}', '{city}', '{state}', '{zip}', '{nearest}', '{dist}')"
            )

            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()
                    print("result:", table_fetched)
            db.commit()
            mysql_connection.close()

            # Show a message for successful addition
            messagebox.showinfo(title="Added!", message="Your property has been added")
            screen_owner_add_property.destroy()
            window_home()

        def owner_add_property_check_name(name):
            if 0 < len(name) <= 50:
                return True

            w_owner_add_property_name_error.config(
                text="Enter a name between 1 to 50 characters"
            )
            return False

        def owner_add_property_check_description(description):
            if 0 < len(description) <= 500:
                return True

            w_owner_add_property_description_error.config(
                text="Enter a description between 1 to 500 characters"
            )
            return False

        def owner_add_property_check_street(street):
            if 0 < len(street) <= 50:
                return True

            w_owner_add_property_street_error.config(
                text="Enter a street between 1 to 50 characters with alphanumeric characters"
            )
            return False

        def owner_add_property_check_city(city):
            if 0 < len(city) <= 50:
                return True

            w_owner_add_property_city_error.config(
                text="Enter a city between 1 to 50 characters with only alphabet characters"
            )
            return False

        def owner_add_property_check_state(state):
            if state != "NULL":
                return True

            w_owner_add_property_state_error.config(text="Select a state")
            return False

        def owner_add_property_check_zip(zip):
            try:
                int(zip)
            except:
                w_owner_add_property_zip_error.config(text="Enter a valid zip code")
                return False

            if len(zip) == 5:
                return True

            w_owner_add_property_zip_error.config(text="Zip code must be 5 digits")
            return False

        def owner_add_property_check_nearest(nearest):
            db = mysql.connector.connect(**connection_config_dict)
            cursor = db.cursor()
            query = "select airport_id from Airport"
            cursor.execute(query)
            airport_list = [item[0] for item in cursor.fetchall()]
            db.close

            if (
                len(nearest) == 3
                and nearest.isalpha()
                and nearest.isupper()
                and nearest in airport_list
            ):
                return True

            w_owner_add_property_nearest_error.config(
                text="Must be a valid airport in the system with 3 uppercase letters"
            )
            return False

        def owner_add_property_check_dist(dist):
            try:
                dist = int(dist)
            except:
                w_owner_add_property_dist_error.config(text="Enter a valid number")
                return False

            if dist >= 0:
                return True

            w_owner_add_property_dist_error.config(text="Distance cannot be negative")
            return False

        def owner_add_property_check_capacity(capacity):
            try:
                capacity = int(capacity)
            except:
                w_owner_add_property_capacity_error.config(text="Enter a valid number")
                return False

            if capacity > 0:
                return True

            w_owner_add_property_capacity_error.config(
                text="Capacity must be at least 0"
            )
            return False

        def owner_add_property_check_cost(cost):
            try:
                cost = int(cost)
            except:
                w_owner_add_property_cost_error.config(text="Enter a valid number")
                return False

            if 0 <= cost <= 9999.99:
                return True

            w_owner_add_property_cost_error.config(
                text="Cost must be between 0 and 9999.99"
            )
            return False

    """
    OWNER REMOVE PROPERTY
    """
    # done 1
    if True:

        def window_owner_remove_property():
            try:
                screen_home.destroy()
            except:
                pass
            global screen_owner_remove_property
            screen_owner_remove_property = Tk()
            screen_owner_remove_property.geometry("1100x700")
            screen_owner_remove_property.title("Owner Remove Property")

            # Title
            Label(text="Owner Remove Property").grid(row=0, column=0, columnspan=5)

            # create cursor and initialize
            db = mysql.connector.connect(**connection_config_dict)
            cursor = db.cursor()
            query = (
                "select p.property_name, descr, capacity, cost, concat(street,' ',city,' ',state,' ',zip) "
                "from Property as p left outer join Reserve as r on p.Property_Name = r.Property_Name "
                f"where p.owner_email = '{current_email}' "
                "group by p.property_name"
            )

            cursor.execute(query)

            # Table parameters
            global var_owner_remove_property_list
            var_owner_remove_property_list = cursor.fetchall()
            cursor.close()
            col_names = (
                "Property Name",
                "Description",
                "Capacity",
                "Cost",
                "Address",
                "Select",
            )
            num_rows = len(var_owner_remove_property_list)
            if num_rows != 0:
                num_cols = len(var_owner_remove_property_list[0])
            else:
                num_cols = 0
            offset = 1
            w = 20
            h = 2

            # Create Columns
            for j, name in enumerate(col_names):
                table_owner_remove_property = Text(
                    screen_owner_remove_property, state="normal", width=w, height=h
                )
                table_owner_remove_property.grid(row=offset, column=j)
                table_owner_remove_property.insert("end", name)
                table_owner_remove_property.configure(state="disabled")
            offset += 1

            # Insert data
            for i in range(num_rows):
                for j in range(num_cols):
                    table_owner_remove_property = Text(
                        screen_owner_remove_property,
                        state="normal",
                        wrap=WORD,
                        width=w,
                        height=h,
                    )
                    table_owner_remove_property.grid(row=i + offset, column=j)
                    table_owner_remove_property.insert(
                        "end", var_owner_remove_property_list[i][j]
                    )
                    table_owner_remove_property.configure(state="disabled")

            # Radio button to select which flight
            global var_owner_remove_property_radio
            var_owner_remove_property_radio = IntVar()
            for i in range(num_rows):
                table_owner_remove_property = Radiobutton(
                    screen_owner_remove_property,
                    variable=var_owner_remove_property_radio,
                    value=i,
                )
                table_owner_remove_property.grid(row=i + offset, column=5)
            offset += num_rows

            # Two Buttons: Back and Submit
            Button(text="Back", command=exit_view_global).grid(
                row=offset, column=0, pady=(100, 0)
            )
            Button(text="Remove Property", command=owner_remove_property_submit).grid(
                row=offset, column=5, pady=(100, 0)
            )
            offset += 1

            screen_owner_remove_property.mainloop()

        def owner_remove_property_submit():
            # If owner has no property
            if len(var_owner_remove_property_list) == 0:
                return None

            db = mysql.connector.connect(**connection_config_dict)
            cursor = db.cursor()
            query = (
                "select p.property_name, descr, capacity, cost, concat(street,' ',city,' ',state,' ',zip) "
                "from Property as p left outer join Reserve as r on p.Property_Name = r.Property_Name "
                f"where p.owner_email = '{current_email}' and start_date <= '{current_date}' and '{current_date}' <= end_date"
            )

            cursor.execute(query)
            var_owner_remove_property_list_2 = cursor.fetchall()
            cursor.close()

            # Remove data from the database the database
            property = var_owner_remove_property_list[
                var_owner_remove_property_radio.get()
            ][0]
            for nonremovable_property in var_owner_remove_property_list_2:
                if property == nonremovable_property[0]:
                    messagebox.showerror(
                        title="Error!",
                        message="This property has an active reservation",
                    )
                    return None

            mysql_connection = db.cursor()
            savequery = f"call remove_property('{property}', '{current_email}', '{current_date}')"
            mysql_connection.execute(savequery, multi=True)
            db.commit()
            mysql_connection.close()

            # Show a message for successful removal
            messagebox.showinfo(
                title="Removed!", message="Your property has been removed"
            )
            screen_owner_remove_property.destroy()
            window_home()

    """
    OWNER RATE CUSTOMER
    """
    # done 1
    if True:

        def window_owner_rate_customer():
            try:
                screen_home.destroy()
            except:
                pass
            global screen_owner_rate_customer
            screen_owner_rate_customer = Tk()
            screen_owner_rate_customer.geometry("1100x700")
            screen_owner_rate_customer.title("Owner Rate Customer")

            # Title
            Label(text="Owner Rate Customer").grid(row=0, column=0, columnspan=5)

            # create cursor and initialize
            db = mysql.connector.connect(**connection_config_dict)
            cursor = db.cursor()
            query = (
                "select Start_Date, r.Customer, r.Property_Name, concat(street,' ',city,' ',state,' ',zip) "
                "from (Reserve as r join Property as p on r.Property_Name = p.Property_Name) "
                "left outer join Owners_Rate_Customers as orc on r.Customer = orc.Customer "
                f"where score is null and was_cancelled = 0 and End_Date < '{current_date}' and r.Owner_Email = '{current_email}'"
            )
            cursor.execute(query)

            # Table parameters
            global var_owner_rate_customer_list
            var_owner_rate_customer_list = cursor.fetchall()
            db.close()
            col_names = (
                "Reservation Date",
                "Customer Email",
                "Property Name",
                "Address",
                "Rating",
            )
            num_rows = len(var_owner_rate_customer_list)
            if num_rows != 0:
                num_cols = len(var_owner_rate_customer_list[0])
            else:
                num_cols = 0
            offset = 1
            w = 25
            h = 2

            # Create Columns
            for j, name in enumerate(col_names):
                table_owner_rate_customer = Text(
                    screen_owner_rate_customer, state="normal", width=w, height=h
                )
                table_owner_rate_customer.grid(row=offset, column=j)
                table_owner_rate_customer.insert("end", name)
                table_owner_rate_customer.configure(state="disabled")
            offset += 1

            # Insert data
            for i in range(num_rows):
                for j in range(num_cols):
                    table_owner_rate_customer = Text(
                        screen_owner_rate_customer,
                        state="normal",
                        wrap=WORD,
                        width=w,
                        height=h,
                    )
                    table_owner_rate_customer.grid(row=i + offset, column=j)
                    table_owner_rate_customer.insert(
                        "end", var_owner_rate_customer_list[i][j]
                    )
                    table_owner_rate_customer.configure(state="disabled")

            # Insert textbox for customer
            global var_owner_rate_customer_score
            var_owner_rate_customer_score = []
            for i in range(num_rows):
                var_num_seat = StringVar()
                var_owner_rate_customer_score.append((i, var_num_seat))
                num_seat = Entry(screen_owner_rate_customer, textvariable=var_num_seat)
                num_seat.grid(row=i + offset, column=4, ipadx=w * 1.6, ipady=8)
            offset += num_rows

            # Two Buttons: Back and Submit
            Button(text="Back", command=exit_view_global).grid(
                row=offset, column=0, pady=(100, 0)
            )
            Button(text="Submit", command=owner_rate_customer_submit).grid(
                row=offset, column=4, pady=(100, 0)
            )
            offset += 1

            # Error Message
            global w_owner_rate_customer_error
            w_owner_rate_customer_error = Label(text="")
            w_owner_rate_customer_error.grid(row=offset, column=4)

            screen_owner_rate_customer.mainloop()

        def owner_rate_customer_submit():
            # Add the rating to the database
            valid_score = []
            for i, score in var_owner_rate_customer_score:
                if len(score.get()) != 0 and not owner_rate_customer_check_score(
                    score.get()
                ):
                    return None
                elif len(score.get()) != 0 and owner_rate_customer_check_score(
                    score.get()
                ):
                    valid_score.append(
                        (i, int(score.get()), var_owner_rate_customer_list[i][1])
                    )

            # No rating submitted
            if len(valid_score) == 0:
                w_owner_rate_customer_error.config(
                    text="Please rate at least one owner"
                )
                return None

            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()

            for i, score, customer_email in valid_score:
                savequery = f"call owner_rates_customer('{current_email}', '{customer_email}', {score}, '{current_date}')"
                mysql_connection.execute(savequery, multi=True)
                db.commit()
            mysql_connection.close()

            # Show a message for successful rating
            messagebox.showinfo(
                title="Thank You!", message="Your rating has been submitted"
            )
            screen_owner_rate_customer.destroy()
            window_home()

        def owner_rate_customer_check_score(score):
            try:
                score = int(score)
            except:
                w_owner_rate_customer_error.config(
                    text="Must enter a number for the score"
                )
                return False

            if 1 <= score <= 5:
                return True

            w_owner_rate_customer_error.config(
                text="Must enter a number between 1 and 5"
            )
            return False


# worked by jenna
if True:

    """process data"""
    # done 1
    if True:

        def check_date(given_date):
            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = f"call process_date('{given_date}');"
            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()
                    print("result:", table_fetched)
            db.commit()
            mysql_connection.close()
            return True

        def process_date():
            global date_input
            date_input = var_date_input.get()
            w_date_input.config(text="")

            if date_input == "":
                w_date_input.config(text="the date cannot be empty")
                return None

            pattern = r"(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])"
            match = re.search(pattern, date_input)
            if match:
                print(match.group())
            else:
                print("reached")
                w_date_input.config(text="the date is an incorrect format")
                return None

            if check_date(date_input) == False:
                w_date_input.config(text="failed to update database")
                return None
            else:
                w_date_input.config(text="success")

        def window_process_date():
            try:
                screen_home.destroy()
            except:
                pass

            global screen_process_date
            screen_process_date = Tk()
            screen_process_date.geometry("700x700")
            screen_process_date.title("Admin Process Date")
            Label(
                text="Travel reservation application",
                bg="grey",
                font=("Calibri", 13),
                width=65,
            ).pack()
            Label(text="").pack()

            global var_date_input
            var_date_input = StringVar()

            Label(
                text=f"Enter the date to process and update customer locations (YYYY-MM-DD), Current date is {current_date}"
            ).pack()
            Entry(screen_process_date, textvariable=var_date_input).pack()

            Button(text="Set Date", command=process_date).pack()
            Label(text="").pack()
            Button(text="Back", command=exit_view_global).pack()

            global w_date_input
            w_date_input = Label(text="")
            w_date_input.pack()
            screen_process_date.mainloop()

    """c view flight"""
    # done 1
    if True:

        def create_flight_treeview():
            try:
                tree.delete(*tree.get_children())
            except:
                pass
            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = f"select b.Flight_Num, b.Airline_Name, b.From_Airport, b.To_Airport, b.Departure_Time, b.Arrival_Time, b.Flight_Date, a.Avail, b.Cost, b.Total from (select f.Flight_Num, f.Airline_Name, f.From_Airport, f.To_Airport, f.Departure_Time, f.Arrival_Time, f.Flight_Date, f.Cost, (Num_Seats)*(Cost) as Total from Book as bo join Flight as f on bo.Flight_Num = f.Flight_Num where Customer = '{current_email}' and Was_Cancelled = 0 group by bo.Flight_Num union select f.Flight_Num, f.Airline_Name, f.From_Airport, f.To_Airport, f.Departure_Time, f.Arrival_Time, f.Flight_Date, f.Cost, (Num_Seats)*(Cost)*0.2 from Book as bo join Flight as f on bo.Flight_Num = f.Flight_Num where Customer = '{current_email}' and Was_Cancelled = 1 group by bo.Flight_Num union select Flight_Num, Airline_Name, From_Airport, To_Airport, Departure_Time, Arrival_Time, Flight_Date, Cost, 0 from Flight where Flight_Num not in (select f.Flight_Num from Book as bo join Flight as f on bo.Flight_Num = f.Flight_Num where Customer = '{current_email}' group by bo.Flight_Num)) as b join (select coalesce((Capacity - sum(Num_Seats)),Capacity) as Avail, Flight.Flight_Num from Flight left outer join Book on Flight.Flight_Num = Book.Flight_Num where Was_Cancelled = 0 or Was_Cancelled is null group by Flight.Flight_Num) as a on b.Flight_Num = a.Flight_Num;"
            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()
                    print(table_fetched)
                    if len(table_fetched) > 0:
                        for curRow in table_fetched:
                            if curRow[7] > float(seats):
                                tree.insert("", "end", text="1", values=curRow)
                        if len(tree.get_children()) == 0:
                            return False
                        return True

                    else:
                        return False

        def intial_flight_treeview():
            try:
                tree.delete(*tree.get_children())
            except:
                pass
            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = f"select b.Flight_Num, b.Airline_Name, b.From_Airport, b.To_Airport, b.Departure_Time, b.Arrival_Time, b.Flight_Date, a.Avail, b.Cost, b.Total from (select f.Flight_Num, f.Airline_Name, f.From_Airport, f.To_Airport, f.Departure_Time, f.Arrival_Time, f.Flight_Date, f.Cost, (Num_Seats)*(Cost) as Total from Book as bo join Flight as f on bo.Flight_Num = f.Flight_Num where Customer = '{current_email}' and Was_Cancelled = 0 group by bo.Flight_Num union select f.Flight_Num, f.Airline_Name, f.From_Airport, f.To_Airport, f.Departure_Time, f.Arrival_Time, f.Flight_Date, f.Cost, (Num_Seats)*(Cost)*0.2 from Book as bo join Flight as f on bo.Flight_Num = f.Flight_Num where Customer = '{current_email}' and Was_Cancelled = 1 group by bo.Flight_Num union select Flight_Num, Airline_Name, From_Airport, To_Airport, Departure_Time, Arrival_Time, Flight_Date, Cost, 0 from Flight where Flight_Num not in (select f.Flight_Num from Book as bo join Flight as f on bo.Flight_Num = f.Flight_Num where Customer = '{current_email}' group by bo.Flight_Num)) as b join (select coalesce((Capacity - sum(Num_Seats)),Capacity) as Avail, Flight.Flight_Num from Flight left outer join Book on Flight.Flight_Num = Book.Flight_Num where Was_Cancelled = 0 or Was_Cancelled is null group by Flight.Flight_Num) as a on b.Flight_Num = a.Flight_Num;"
            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()
                    print(table_fetched)
                    if len(table_fetched) > 0:
                        for curRow in table_fetched:
                            tree.insert("", "end", text="1", values=curRow)
                        if len(tree.get_children()) == 0:
                            return False
                        return True

                    else:
                        return False

        def fetch_flights():
            global seats
            seats = var_seats_input.get()
            w_seats_input.config(text="")

            if seats == "":
                w_seats_input.config(text="please input available seats")
                return None

            if str.isdigit(seats):
                print("ok")
            else:
                w_seats_input.config(text="please enter a digit")
                return None
            if create_flight_treeview() == False:
                w_seats_input.config(text="no flights available")
                return None
            else:
                return None

        def window_customer_view_flights():
            try:
                screen_home.destroy()
            except:
                pass
            global tree
            global screen_customer_view_flights
            screen_customer_view_flights = Tk()
            screen_customer_view_flights.geometry("1000x1000")
            screen_customer_view_flights.title("View Flights")
            Label(
                text="Travel reservation application",
                bg="grey",
                font=("Calibri", 13),
                width=65,
            ).pack()
            Label(text="").pack()

            tree = ttk.Treeview(screen_customer_view_flights)

            global var_seats_input
            var_seats_input = StringVar()
            global w_seats_input
            w_seats_input = Label(text="")
            w_seats_input.pack()

            Label(text="Available Seats: ").pack()
            Entry(screen_customer_view_flights, textvariable=var_seats_input).pack()

            Button(text="Filter", command=fetch_flights).pack()
            Label(text="").pack()
            Button(text="Back", command=exit_view_global).pack()

            tree_frame = Frame(screen_customer_view_flights)
            tree_frame.pack(pady=20)
            vertscroll = ttk.Scrollbar(tree_frame, orient="vertical")
            vertscroll.pack(fill=Y, side="right")

            tree = ttk.Treeview(
                tree_frame,
                yscrollcommand=vertscroll.set,
                show="headings",
                selectmode="extended",
            )
            vertscroll.configure(command=tree.yview)
            tree["columns"] = (
                "ID",
                "Airline",
                "From",
                "To",
                "Dept.Time",
                "Arr.Time",
                "Date",
                "Available Seats",
                "Cost Per Seat",
                "Total Spent",
            )

            tree.column("# 1", anchor=CENTER, stretch=YES, width=50)
            tree.heading("# 1", text="ID")
            tree.column("# 2", anchor=CENTER, stretch=YES, width=150)
            tree.heading("# 2", text="Airline")
            tree.column("# 3", anchor=CENTER, stretch=YES, width=50)
            tree.heading("# 3", text="From")
            tree.column("# 4", anchor=CENTER, stretch=YES, width=50)
            tree.heading("# 4", text="To")
            tree.column("# 5", anchor=CENTER, stretch=YES, width=100)
            tree.heading("# 5", text="Dept.Time")
            tree.column("# 6", anchor=CENTER, stretch=YES, width=100)
            tree.heading("# 6", text="Arr.Time")
            tree.column("# 7", anchor=CENTER, stretch=YES, width=100)
            tree.heading("# 7", text="Date")
            tree.column("# 8", anchor=CENTER, stretch=YES, width=50)
            tree.heading("# 8", text="Available Seats")
            tree.column("# 9", anchor=CENTER, stretch=YES, width=100)
            tree.heading("# 9", text="Cost Per Seat")
            tree.column("# 10", anchor=CENTER, stretch=YES, width=100)
            tree.heading("# 10", text="Total Spent")
            tree.pack()

            intial_flight_treeview()
            screen_customer_view_flights.mainloop()

    """c view properties"""
    # done 0 DO SORT
    if True:

        def create_properties_treeview():
            try:
                propertiesTree.delete(*propertiesTree.get_children())
            except:
                pass
            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = f"SELECT * FROM travel_reservation_service.view_properties;"
            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()
                    print(table_fetched)
                    if len(table_fetched) > 0:
                        for curRow in table_fetched:
                            if curRow[4] >= float(minCap) and curRow[4] <= float(
                                maxCap
                            ):
                                propertiesTree.insert(
                                    "", "end", text="1", values=curRow
                                )
                        if len(propertiesTree.get_children()) == 0:
                            return False
                        return True

                    else:
                        return False

        def intial_properties_treeview():
            try:
                propertiesTree.delete(*propertiesTree.get_children())
            except:
                pass
            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = f"SELECT * FROM travel_reservation_service.view_properties;"
            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()
                    print(table_fetched)
                    if len(table_fetched) > 0:
                        for curRow in table_fetched:
                            propertiesTree.insert("", "end", text="1", values=curRow)
                        if len(propertiesTree.get_children()) == 0:
                            return False
                        return True

                    else:
                        return False

        def sort_by_cost():
            # extract values from treeview, assign to list named subset
            subset = []
            for record in propertiesTree.get_children():
                subset.append(propertiesTree.item(record)["values"])
            # if the subset is already sorted on the values in this column, reverse sort. Otherwise, sort the subset.
            if sorted([item[5] for item in subset]) == ([item[5] for item in subset]):
                subset.sort(key=lambda x: x[5] or 0, reverse=True)
                # clear tree view
                propertiesTree.delete(*propertiesTree.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    propertiesTree.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                            record[5],
                        ),
                    )
                    i += 1
            else:
                subset.sort(key=lambda x: x[5] or 0)
                # clear tree view
                propertiesTree.delete(*propertiesTree.get_children())
                # insert sorted values into treeview
                i = 0
                for record in subset:
                    propertiesTree.insert(
                        "",
                        i,
                        text="",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                            record[5],
                        ),
                    )
                    i += 1

        def fetch_properties():
            global minCap
            global maxCap

            minCap = var_minCap_input.get()
            maxCap = var_maxCap_input.get()

            w_cap.config(text="")

            if minCap == "" or maxCap == "":
                w_cap.config(text="please input a max and min capacity")
                return None

            if str.isdigit(minCap) and str.isdigit(maxCap):
                print("ok")
            else:
                w_cap.config(text="please enter a digit")
                return None
            if create_properties_treeview() == False:
                w_cap.config(text="no properties")
                return None
            else:
                return None

        def window_customer_view_properties():
            try:
                screen_home.destroy()
            except:
                pass
            global propertiesTree

            global screen_customer_view_properties
            screen_customer_view_properties = Tk()
            screen_customer_view_properties.geometry("1000x1000")
            screen_customer_view_properties.title("View Properties")
            Label(
                text="Travel reservation application",
                bg="grey",
                font=("Calibri", 13),
                width=65,
            ).pack()
            Label(text="").pack()
            screen_customer_view_properties.grid_columnconfigure(0, weight=1)
            screen_customer_view_properties.grid_rowconfigure(0, weight=1)
            # screen_customer_view_properties.grid(column = 0, row = 0, sticky = "nsew")
            propertiesTree = ttk.Treeview(screen_customer_view_properties)

            global var_minCap_input
            global var_maxCap_input

            var_minCap_input = StringVar()
            var_maxCap_input = StringVar()

            global w_cap
            w_cap = Label(text="")
            w_cap.pack()

            Label(text="Min Capacity").pack()
            Entry(screen_customer_view_properties, textvariable=var_minCap_input).pack()
            Label(text="Max Capacity").pack()
            Entry(screen_customer_view_properties, textvariable=var_maxCap_input).pack()

            Button(text="Filter", command=fetch_properties).pack()
            Label(text="").pack()
            Button(text="Back", command=window_home).pack()

            tree_frame = Frame(screen_customer_view_properties)
            tree_frame.pack(fill="both", expand=1, pady=20)
            vertscroll = ttk.Scrollbar(tree_frame, orient="vertical")
            vertscroll.pack(fill=Y, side="right")

            propertiesTree = ttk.Treeview(
                tree_frame,
                yscrollcommand=vertscroll.set,
                show="headings",
                selectmode="extended",
            )
            vertscroll.configure(command=propertiesTree.yview)
            propertiesTree["columns"] = (
                "Name",
                "Avg Rating",
                "Description",
                "Address",
                "Capacity",
                "Nightly Cost",
            )

            propertiesTree.column("# 1", anchor=CENTER, stretch=YES, width=100)
            propertiesTree.heading("# 1", text="Name")
            propertiesTree.column("# 2", anchor=CENTER, stretch=YES, width=100)
            propertiesTree.heading("# 2", text="Avg Rating")
            propertiesTree.column("# 3", anchor=CENTER, stretch=YES, width=300)
            propertiesTree.heading("# 3", text="Description")
            propertiesTree.column("# 4", anchor=CENTER, stretch=YES, width=300)
            propertiesTree.heading("# 4", text="Address")
            propertiesTree.column("# 5", anchor=CENTER, stretch=YES, width=100)
            propertiesTree.heading("# 5", text="Capacity")
            propertiesTree.column("# 6", anchor=CENTER, stretch=YES, width=50)
            propertiesTree.heading(
                "# 6", text="Cost", anchor=tkinter.CENTER, command=sort_by_cost
            )
            propertiesTree.pack(fill="both", expand=1)

            intial_properties_treeview()
            screen_customer_view_properties.mainloop()

    """c view reserved properties"""
    # done 0
    if True:

        def create_reserved_treeview():
            try:
                reservedPropertiesTree.delete(*reservedPropertiesTree.get_children())
            except:
                pass
            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = f"select Property.Property_Name, Reserve.Start_Date, Reserve.End_Date, Clients.Phone_Number, Reserve.Customer, Property.Cost, Review.Content, Review.Score from Property join Reserve join Review join Clients where Property.Property_Name = Reserve.Property_Name and Reserve.Customer = Review.Customer and Reserve.Customer = Clients.Email;"
            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()
                    if len(table_fetched) > 0:
                        for curRow in table_fetched:
                            if propertyEmail == "":
                                if curRow[0] == propertyName:
                                    reservedPropertiesTree.insert(
                                        "", "end", text="1", values=curRow
                                    )

                            if propertyName == "":
                                if curRow[4] == propertyEmail:
                                    reservedPropertiesTree.insert(
                                        "", "end", text="1", values=curRow
                                    )

                        return True
                    else:
                        return False
                else:
                    return False

        def create_initial_reserved_treeview():
            try:
                reservedPropertiesTree.delete(*reservedPropertiesTree.get_children())
            except:
                pass
            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = f"select Property.Property_Name, Reserve.Start_Date, Reserve.End_Date, Clients.Phone_Number, Reserve.Customer, Property.Cost, Review.Content, Review.Score from Property join Reserve join Review join Clients where Property.Property_Name = Reserve.Property_Name and Reserve.Customer = Review.Customer and Reserve.Customer = Clients.Email;"
            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()
                    if len(table_fetched) > 0:
                        for curRow in table_fetched:
                            reservedPropertiesTree.insert(
                                "", "end", text="1", values=curRow
                            )
                        return True
                    else:
                        return False
                else:
                    return False

        def fetch_reserved_properties():
            global propertyEmail
            global propertyName

            propertyEmail = var_propertyEmail_input.get()
            propertyName = var_propertyName_input.get()

            w_property.config(text="")

            if propertyEmail == "" and propertyName == "":
                w_property.config(text="please input an email or property name")
                return None

            if propertyEmail != "" and (
                not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", propertyEmail)
            ):
                w_property.config(text="enter valid email")
                return None

            if create_reserved_treeview() == False:
                w_property.config(text="no properties")
                return None
            else:
                return None

        def window_customer_view_reserved_properties():
            try:
                screen_home.destroy()
            except:
                pass
            global reservedPropertiesTree

            global screen_customer_view__reserved_properties
            screen_customer_view__reserved_properties = Tk()
            screen_customer_view__reserved_properties.geometry("1000x1000")
            screen_customer_view__reserved_properties.title("View Reserved Properties")
            Label(
                text="Travel reservation application",
                bg="grey",
                font=("Calibri", 13),
                width=65,
            ).pack()
            Label(text="").pack()

            screen_customer_view__reserved_properties.grid_columnconfigure(0, weight=1)
            screen_customer_view__reserved_properties.grid_rowconfigure(0, weight=1)

            reservedPropertiesTree = ttk.Treeview(
                screen_customer_view__reserved_properties
            )

            global var_propertyEmail_input
            global var_propertyName_input

            var_propertyEmail_input = StringVar()
            var_propertyName_input = StringVar()

            global w_property
            w_property = Label(text="")
            w_property.pack()

            Label(text="Owner Email:").pack()
            Entry(
                screen_customer_view__reserved_properties,
                textvariable=var_propertyEmail_input,
            ).pack()
            Label(text="Property Name:").pack()
            Entry(
                screen_customer_view__reserved_properties,
                textvariable=var_propertyName_input,
            ).pack()

            Button(text="Filter", command=fetch_reserved_properties).pack()
            Label(text="").pack()
            Button(text="Back", command=window_home).pack()

            tree_frame = Frame(screen_customer_view__reserved_properties)
            tree_frame.pack(fill="both", expand=1, pady=20)
            vertscroll = ttk.Scrollbar(tree_frame, orient="vertical")
            vertscroll.pack(fill=Y, side="right")

            reservedPropertiesTree = ttk.Treeview(
                tree_frame,
                yscrollcommand=vertscroll.set,
                show="headings",
                selectmode="extended",
            )
            vertscroll.configure(command=reservedPropertiesTree.yview)
            reservedPropertiesTree["columns"] = (
                "Property Name",
                "Start",
                "End",
                "Cust. Phone",
                "Cust. Email",
                "Cost",
                "Review",
                "Rating",
            )

            reservedPropertiesTree.column("# 1", anchor=CENTER, stretch=YES, width=100)
            reservedPropertiesTree.heading("# 1", text="Property Name'")
            reservedPropertiesTree.column("# 2", anchor=CENTER, stretch=YES, width=50)
            reservedPropertiesTree.heading("# 2", text="Start")
            reservedPropertiesTree.column("# 3", anchor=CENTER, stretch=YES, width=50)
            reservedPropertiesTree.heading("# 3", text="End")
            reservedPropertiesTree.column("# 4", anchor=CENTER, stretch=YES, width=100)
            reservedPropertiesTree.heading("# 4", text="Cust. Phone")
            reservedPropertiesTree.column("# 5", anchor=CENTER, stretch=YES, width=100)
            reservedPropertiesTree.heading("# 5", text="Cust. Email")
            reservedPropertiesTree.column("# 6", anchor=CENTER, stretch=YES, width=50)
            reservedPropertiesTree.heading("# 6", text="Cost")
            reservedPropertiesTree.column("# 7", anchor=CENTER, stretch=YES, width=100)
            reservedPropertiesTree.heading("# 7", text="Review")
            reservedPropertiesTree.column("# 8", anchor=CENTER, stretch=YES, width=50)
            reservedPropertiesTree.heading("# 8", text="Rating")
            reservedPropertiesTree.pack(fill="both", expand=1)

            create_initial_reserved_treeview()
            screen_customer_view__reserved_properties.mainloop()

    """delete owner"""
    # done 1
    if True:

        def returnLogin():
            print("reached return to login")
            try:
                screen_delete_owner.destroy()
            except:
                pass
            window_login()
            return None

        def deleteOwner(deleteEmail):
            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = f"select * from Property where Owner_Email = '{deleteEmail}'"
            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()
                    if len(table_fetched) > 0:
                        w_delete.config(
                            text="you cannot have a property under your account to delete it"
                        )
                        return None
            db.commit()
            mysql_connection.close()

            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = f"call remove_owner('{deleteEmail}');"
            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()
                    print("result:", table_fetched)
            db.commit()
            mysql_connection.close()
            returnLogin()
            return None

        def window_delete_owner():
            try:
                screen_home.destroy()
            except:
                pass

            global screen_delete_owner
            screen_delete_owner = Tk()
            screen_delete_owner.geometry("700x700")
            screen_delete_owner.title("Delete Owner Account")
            Label(
                text="Travel reservation application",
                bg="grey",
                font=("Calibri", 13),
                width=65,
            ).pack()
            Label(text="").pack()

            Label(text="Are you sure you want to delete your Owner account?").pack()

            global w_delete
            w_delete = Label(text="")
            w_delete.pack()

            Button(text="Delete", command=lambda: deleteOwner(current_email)).pack()
            Button(text="Log Out", command=returnLogin).pack()
            Label(text="").pack()
            Button(text="Back", command=exit_view_global).pack()

            screen_delete_owner.mainloop()

    """c cancel property"""
    # done 1
    if True:

        def create_tocancel_treeview():
            try:
                currentPropTree.delete(*currentPropTree.get_children())
            except:
                pass
            global cancelPropertyList
            cancelPropertyList = []
            db = mysql.connector.connect(**connection_config_dict)
            mysql_connection = db.cursor()
            savequery = f"select Reserve.Start_Date, Property.Property_Name, Property.Owner_Email, CONCAT(Property.Street, ' ', Property.City, ' ', Property.State) from Property join Reserve where Reserve.Property_Name = Property.Property_Name and Reserve.Customer = '{current_email}' and Reserve.Was_Cancelled = 0;"
            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()
                    if len(table_fetched) > 0:
                        count = 1

                        for curRow in table_fetched:
                            cancelPropertyList.append(curRow)
                            newList = []
                            for value in curRow:
                                newList.append(value)
                            currentPropTree.insert(
                                "", "end", text="1", values=[count] + newList
                            )
                            count += 1
                        if len(currentPropTree.get_children()) == 0:
                            return False
                        return True
                    else:
                        return False

        def cancel_properties():
            global resNo
            resNo = var_reserve_number.get()

            w_property.config(text="")
            print(resNo, len(cancelPropertyList))
            if (
                resNo == ""
                or not str.isdigit(resNo)
                or int(resNo) < 1
                or int(resNo) > len(cancelPropertyList)
            ):
                # print()
                w_property.config(text="please a valid property number")
                return None

            number = int(resNo)
            i_property_name = cancelPropertyList[number - 1][1]
            i_owner_email = cancelPropertyList[number - 1][2]
            i_customer_email = current_email
            i_current_date = datetime.today().strftime("%Y-%m-%d")
            dt2 = datetime.date(datetime.today())

            print(type(cancelPropertyList[number - 1][0]))

            if dt2 > cancelPropertyList[number - 1][0]:
                w_property.config(
                    text="cannot cancel a property booked for a past date"
                )
                return None

            cancelProperty = mysql.connector.connect(**connection_config_dict)
            mysql_connection = cancelProperty.cursor()
            savequery = f"call cancel_property_reservation('{i_property_name}','{i_owner_email}','{i_customer_email}','{i_current_date}');"
            results = mysql_connection.execute(savequery, multi=True)
            for cur in results:
                if cur.with_rows:
                    table_fetched = cur.fetchall()
                    print("result:", table_fetched)
            cancelProperty.commit()
            mysql_connection.close()

            if create_tocancel_treeview() == False:
                w_property.config(text="no reserved properties")

            return None

        def window_customer_cancel_property():
            try:
                screen_home.destroy()
            except:
                pass
            global currentPropTree

            global screen_customer_cancel_properties
            screen_customer_cancel_properties = Tk()
            screen_customer_cancel_properties.geometry("700x700")
            screen_customer_cancel_properties.title("Cancel Reserved Properties")
            Label(
                text="Travel reservation application",
                bg="grey",
                font=("Calibri", 13),
                width=65,
            ).pack()
            Label(text="").pack()

            global var_reserve_number
            var_reserve_number = StringVar()

            global w_property
            w_property = Label(text="")
            w_property.pack()

            Label(text="Cancel Reservation Number:").pack()
            Entry(
                screen_customer_cancel_properties, textvariable=var_reserve_number
            ).pack()

            currentPropTree = ttk.Treeview(screen_customer_cancel_properties)

            Button(text="Submit", command=cancel_properties).pack()
            Label(text="").pack()
            Button(text="Back", command=exit_view_global).pack()

            tree_frame = Frame(screen_customer_cancel_properties)
            tree_frame.pack(pady=50)
            vertscroll = ttk.Scrollbar(tree_frame, orient="vertical")
            vertscroll.pack(fill=Y, side="right")

            currentPropTree = ttk.Treeview(
                tree_frame,
                yscrollcommand=vertscroll.set,
                show="headings",
                selectmode="extended",
            )
            vertscroll.configure(command=currentPropTree.yview)
            currentPropTree["columns"] = (
                "Res. No",
                "Reservation Date",
                "Property Name",
                "Owner Email",
                "Address Rating",
            )

            currentPropTree.column("# 1", anchor=CENTER, stretch=NO, width=50)
            currentPropTree.heading("# 1", text="Res. No")
            currentPropTree.column("# 2", anchor=CENTER, stretch=NO, width=50)
            currentPropTree.heading("# 2", text="Reservation Date")
            currentPropTree.column("# 3", anchor=CENTER, stretch=NO, width=100)
            currentPropTree.heading("# 3", text="Property Name")
            currentPropTree.column("# 4", anchor=CENTER, stretch=NO, width=100)
            currentPropTree.heading("# 4", text="Owner Email")
            currentPropTree.column("# 5", anchor=CENTER, stretch=NO, width=50)
            currentPropTree.heading("# 5", text="Address Rating")

            currentPropTree.pack()

            if create_tocancel_treeview() == False:
                w_property.config(text="no reserved properties")

            screen_customer_cancel_properties.mainloop()


def window_test():
    try:
        screen_home.destroy()
    except:
        pass
    global screen_test
    screen_test = Tk()
    screen_test.geometry("700x700")
    screen_test.title("test")
    Button(text="back", command=window_home).pack()
    screen_test.mainloop()


current_user_account_type = []
current_email = ""
current_password = ""
current_date = "2021-12-15"


# main code
#############################################################
window_login()

if current_email != "":
    window_home()

#############################################
# # testing
# current_user_account_type = ['customer','owner']
# current_email = 'cbing10@gmail.com'
# current_password = ''
# current_date = '2020-10-12'


# window_customer_view_flights()
# print(return_possible_rate_owners())
