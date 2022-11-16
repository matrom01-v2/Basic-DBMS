from asyncio.windows_events import NULL
from distutils.log import error
from time import sleep
from os import system, name
import mysql.connector 
import sys
import os
import re

def clear_screen():
    if name == 'nt':
        system('cls')

    else:
        system('clear')



def login():
    print("=====================")
    print("Welcome to your DBMS!")
    print("=====================\n")

    logged_in = False
    
    while(not logged_in):
        hst = input("Please input hostname: ")
        dtbs = input("Please enter name of database: ")
        usrnm = input("Username: ")
        pswrd = input("Password: ")

        #####################################
        ## CHANGE TO VARIABLES!!!!!!!!!!!!!!!
        #####################################
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="balladeno1ingminor",
                database="abc_media"
            )
            global mycursor
            mycursor = mydb.cursor()

            logged_in = True
            print(f"\nSuccessful login! Weclome to {dtbs}!")
            print("=======================================")
            sleep(2)
            clear_screen()
            main()
            if(mydb.is_connected()):
                mydb.close()
                mycursor.close()
                print("MySQL connection is closed")
        except Exception:
            print("Uh oh, there was a problem connecting. Try logging in again.\n")
        



def main():
    # mycursor.execute("SHOW tables;")
    # print(mycursor)

    # for x in mycursor:
    #     print(x)
    clear_screen()
    print("Main menu")
    print("--------------------------------\n")
    print("\n1. Display all the digital displays.\n"
           "2. Search digital displays given a scheduler system\n"
           "3. Insert a new digital display\n"
           "4. Delete a digital display\n"
           "5. Update a digital display\n"
           "6. Logout\n")
    option = input("Enter number for option: ")
    option = int(option)

    if(option == 1):
        display_all()
    if(option == 2):
        search()
    if(option == 3):
        insert()
    if(option == 4):
        delete()
    if(option == 5):
        update()
    if(option == 6):
        logout()





def display_all():
    print("you selected 1")
    sleep(2)
    main()

def search():
    type = input("Please type the digital display scheduler system: ")
    type = type.lower()

    while(type != "random" and type != "smart" and type != "virtue"):
        print("\nThat is not a valid scheduler system!")
        type = input("Please type the digital display scheduler system: ")
        type = type.lower()


    mycursor.execute(f"select * from digitaldisplay where schedulerSystem = '{type}';")
    myresults = mycursor.fetchall()
    for x in myresults: 
            print(x)

    print("\n1. Search again\n"
            "2. return to main menu\n")

    option = input()
    option = int(option)

    if(option == 1):
        search()
    elif(option == 2):
            main()
    else:
        print("Not a valid input!")
        print("Defaulting to main menu")
        main()
        print()
        

def insert():
    print("you selected 3")
    sleep(2)
    main()

def delete():
    print("you selected 4")
    sleep(2)
    main()

def update():
    print("you selected 5")
    sleep(2)
    main()

def logout():
    print("you selected 6\n")
    print("Are you sure you want to logout?")
    answer = input("Enter \"yes\" to logout or \"no\" to return to main: ")

    if(answer == "yes"):
        print("\nLogging out. See you next time!")
        for i in range(0, 4):
            print("*")
            sleep(1)
        clear_screen()
        login()
    else:
        main()
    



login()
