from asyncio.windows_events import NULL
from distutils.log import error
from time import sleep
from os import system, name
from getpass import getpass
import mysql.connector 
import sys
import os
import re

def clear_screen():
    if name == 'nt':
        system('cls')

    else:
        system('clear')


##################
# Log in function
##################

def login():
    print("=====================")
    print("Welcome to your DBMS!")
    print("=====================\n")

    logged_in = False # flag for successful login
    
    while(not logged_in):
        hst = input("Please input hostname: ")
        dtbs = input("Please enter name of database: ")
        usrnm = input("Username: ")
        pswrd = getpass("Password: ")

        try:
            mydb = mysql.connector.connect(
                host=hst,
                user=usrnm,
                password=pswrd, 
                database=dtbs
            )
            global mycursor
            mycursor = mydb.cursor() # set cursor for collecting tuples

            logged_in = True # 
            print(f"\nSuccessful login! Weclome to {dtbs}!")
            print("=======================================")
            sleep(2)
            clear_screen()
            main()

            # close connection when done
            if(mydb.is_connected()):
                mydb.close()
                mycursor.close()
                print("MySQL connection is closed")
        except Exception:
            print("Uh oh, there was a problem connecting. Try logging in again.\n")
        



def main():

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
    clear_screen()
    print("====================\n", "Digital Displays")
    print("====================\n")
    sleep(1)

    mycursor.execute("select * from digitalDisplay")
    myresults = mycursor.fetchall()

    counter = 1

    # fetch model numbers
    for x in myresults:
        print(counter,":\nModel: ", x[0], "\nSchedular System: ",x[1], "\nSerial Number: ", x[2], "\n")
        counter += 1
    print("--------------------------")
    print("1. See detailed Mondel info")
    print("2. return to Main menu")
    option = int(input("\nEnter number for option: "))

    # ask for input to see digital display or return to main menu
    if option == 1:
        selection = int(input("Enter the model number for desired model: "))
        mycursor.execute(f"select * from Model where modelNo = {selection}")
        print()

        myresults = mycursor.fetchall()

        if myresults == NULL:
            print("No model found!")
        
        # get all detailed info for selected digital display
        for x in myresults:
            print(f"Model Number:\t {x[0]}")
            print(f"Width:\t {x[1]}")
            print(f"Height:\t {x[2]}")
            print(f"Weight:\t {x[3]}")
            print(f"Depth:\t {x[4]}")
            print(f"Screen Size:\t{x[5]}")
        
        print("\nMenu:\n")
        print("1. Return to Digital Displays")
        print("2. Return to Main Menu")

        option = int(input("Enter number for option: "))

        if option == 1:
            display_all()
        else:
            main()
    
    else:
        main()
#end display_all





def search():
    clear_screen()
    type = input("Please type the digital display scheduler system: ")
    type = type.lower()

    while(type != "random" and type != "smart" and type != "virtue"):
        print("\nThat is not a valid scheduler system!")
        type = input("Please type the digital display scheduler system: ")
        type = type.lower()


    mycursor.execute(f"select * from digitaldisplay where schedulerSystem = '{type}';")
    myresults = mycursor.fetchall()
    print(f"\n\"{type}\" Digital Displays")
    print(f"-------------------------")

    count = 1
    for x in myresults: 
            print(f"{count}. Serial Number: ", x[0])
            print(f"\tModel Number: ", x[2],"\n")
            count+=1

    print("\n\nMenu options:")
    print("\n1. Search again\n"
            "2. return to main menu\n")

    option = input("\n\nEnter number for option: ")
    option = int(option)

    if(option == 1):
        search()
    elif(option == 2):
            main()
    else:
        print("Not a valid input!")
        print("Defaulting to main menu")
        sleep(1)
        main()
        print()
# end search        




def insert():
    print("you selected 3")

    print("To insert a new digit display please type")
    modelNo = int(input("Model number: "))

    #check if digitaldisplay model number already exists
    mycursor.execute(f"select * from digitaldisplay where modelNo = {modelNo};")
    myresults = mycursor.fetchall()

    if(len(myresults) != 0):
        print("digital display Model number already exists!\n")
        insert()
        return

    #get rest of the info needed to insert digital dispay
    serialNo = int(input("Serial number: "))
    schsys = input("Scheduler System: ")


    #check if model has a model with that model number
    mycursor.execute(f"select * from model where modelNo = {modelNo};")
    myresults = mycursor.fetchall()

    #if there no model with that model number then call function to create one
    if(len(myresults) == 0):
        print("\nYou need to insert a new model first")
        insertModel(modelNo)

    #insert digital display
    mycursor.execute(f"insert into digitaldisplay values({serialNo},'{schsys}',{modelNo});")

    print("\n---All Digital Displays---")
    mycursor.execute(f"select * from digitaldisplay;")

    counter = 1
    for x in mycursor:
        print(counter,". Model: ", x[0], "\n\tSchedular System: ",x[1], "\n\tSerial Number: ", x[2])
        counter += 1

    print("\n1. Insert again\n"
            "2. return to main menu\n")

    option = int(input())

    if(option == 1):
        insert()
    elif(option == 2):
            main()
    else:
        print("Not a valid input!")
        print("Defaulting to main menu")
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
        return
    
def insertModel(modelNo):
    print("To insert a new model please type")
    width = input("Width: ")
    height = input("height: ")
    weight = input("Weight: ")
    depth = input("Depth: ")
    scrnSize = input("Screen Size: ")

    try:
        mycursor.execute(f"insert into model values({modelNo},{width},{height},{weight},{depth},{scrnSize});")
    except Exception: 
        print("invalid input! Try again")
        insertModel()
        
login()

