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


###########################################################
# LOGIN
# This function begins with a prompt 
# for the user to login, and will verify login information
# at any point, invlaid information will prompt
# the user to relog in.
###########################################################
def login():
    clear_screen()
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
           "2. Search Digital Displays given a Scheduler System\n"
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


###########################################################
# DISPLAY_ALL
# This function displays all Digital Displays
# using a helper function. See showAllDisplays
# - Mateo Romero
###########################################################
def display_all():
    clear_screen()
    print("====================\n", "Digital Displays")
    print("====================\n")
    sleep(1)

    showAllDisplays()

    print("--------------------------")
    print("1. See detailed Mondel info")
    print("2. return to Main menu")
    option = int(input("\nEnter number for option: "))

    # ask for input to see digital display or return to main menu
    if option == 1:
        selection = int(input("Enter the model number for desired model: "))
        mycursor.execute("select * from Model where modelNo = %s", (selection,))
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
    print("====================\n", "Search")
    print("====================\n")
    print("Schedular Systems: Smart, Virtue, Random\n")
    type = input("Please type the digital display scheduler system you want to search: ")
    type = type.lower()

    while(type != "random" and type != "smart" and type != "virtue"):
        print("\nThat is not a valid scheduler system!")
        type = input("Please type the digital display scheduler system: ")
        type = type.lower()


    mycursor.execute("select * from digitaldisplay where schedulerSystem = %s;",(type,))
    myresults = mycursor.fetchall()
    print(f"\n\"{type}\" Digital Displays")
    print(f"-------------------------")

    showAllDisplays()

    print("\n\nMenu options:")
    print("\n1. Search again\n"
            "2. Return to Main Menu\n")

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


###########################################################
# INSERT
# This function handles users inputing a new Digital Display
# and prompts users to enter a new mdoel if required
# - Joey Troyer
###########################################################
def insert():
    print("====================\n", "Insert")
    print("====================\n")

    print("To insert a new digit display please type")
    serialNo = int(input("serialNo number: "))

    #check if digitaldisplay model number already exists
    mycursor.execute("select * from digitaldisplay where serialNo = %s;" % (serialNo))
    myresults = mycursor.fetchall()

    if(len(myresults) != 0):
        print("digital display serial number already exists!\n")
        insert()
        return

    #get rest of the info needed to insert digital dispay
    modelNo = int(input("model number: "))
    schsys = input("Scheduler System: ")


    #check if model has a model with that model number
    mycursor.execute("select * from model where modelNo = %s;" % (modelNo))
    myresults = mycursor.fetchall()

    #if there no model with that model number then call function to create one
    if(len(myresults) == 0):
        print("\nYou need to insert a new model first")
        insertModel(modelNo)

    #insert digital display
    mycursor.execute("insert into digitaldisplay values(%s,%s,%s);", (serialNo,schsys,modelNo))

    print("\n---All Digital Displays---")
    showAllDisplays()

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
    clear_screen()
    print("====================\n", "Delete")
    print("====================\n")

    showAllDisplays()

    print("--------------------------")
    print("1. Delete a Digital Display")
    print("2. Return to Main menu")
    option = input("\n\nEnter number for option: ")
    option = int(option)

    if(option == 1):
        print("To delete a digital display please enter")
        serialNo = input("serial Number: ")


        # Check for Valid input
        notValid = True 
        while(notValid):
            if (not serialNo.isdigit()):
                print("Oops! That was invalid input")
                serialNo = input("Please enter Serial Number for digital display: ")
            else:
                notValid = False


        modelNo = input("model number: ")

        # Check for Valid input
        notValid = True 
        while(notValid):
            if (not modelNo.isdigit()):
                print("Oops! That was invalid input")
                modelNo = input("Please enter model Number for digital display: ")
            else:
                notValid = False

        #delete digitaldisplay
        try:
            mycursor.execute("delete from digitaldisplay where serialNo = %s;" , (serialNo,))
            print("succesfully deleted digital display")
        except Exception:
             print("An error occured while deleteing digital display! Please try again\n")
             delete()


        #check if model number coresponds to any other digital displays
        try:
            mycursor.execute("select * from digital display where modelNo = %s;" % (modelNo,))
            myresults = mycursor.fetchall()
        except Exception:
            print("error checking for corresponding models")
            delete()

        #if not other digitaldisplays have that model delete the model
        if(len(myresults) == 0):
            try:
                mycursor.execute("Delete from model where modelNo = %s;" % (modelNo,))
                print("succesfully deleted corresponding model")
            except Exception:
                print("An error occured while deleteing model!\n")


        showAllDisplays()


        print("\n==== models ====")
        mycursor.execute("select * from model;")

        myresults = mycursor.fetchall()

        count = 1
        for x in myresults:
            print(count)
            print(f"Model Number:\t {x[0]}")
            print(f"Width:\t {x[1]}")
            print(f"Height:\t {x[2]}")
            print(f"Weight:\t {x[3]}")
            print(f"Depth:\t {x[4]}")
            print(f"Screen Size:\t{x[5]}\n")
            count += 1
    
    # rerturn to main menu option   
    elif(option == 2):
        main()
    else:
        print("Not a valid input!") 
        sleep(1)
        delete()


##############################################################
# UPDATE
# This function handles the users wanting to update
# a Digital Display. It also handles checking for valid input
# - Mateo Romero
###############################################################
def update():
    clear_screen()
    print("====================\n", "Update")
    print("====================\n")

    print("Available Digital Displays:")
    mycursor.execute("select * from digitalDisplay")
    myresults = mycursor.fetchall()

    counter = 1

    # fetch model numbers
    for x in myresults:
        print(counter,":\nSerial Number: ", x[0], "\nSchedular System: ",x[1], "\nModel: ", x[2], "\n")
        counter += 1
    print("--------------------------")
    print("1. Update a Digital Display")
    print("2. Return to Main menu")
    option = input("\n\nEnter number for option: ")
    option = int(option)


    # UPDATE A DIGITAL DISPLAY
    if(option == 1):
        sernum = input("Please enter Serial Number for updated digital display: ")

        # Check for Valid input
        notValid = True 
        while(notValid):
            if (not sernum.isdigit()):
                print("Oops! That was invalid input")
                sernum = input("Please enter Serial Number for updated digital display: ")
            else:
                notValid = False
        
        # update options
        print("What would you like to update?")
        print("\n1. Serial Number\n"
            "2. Schedular System\n"
            "3. Model Number\n")
        upoption = input("\n\nEnter number for option: ")
        upoption = int(upoption)


        if(upoption == 1):
            newser = input("Enter new Serial Number: ")

            # check for valid input
            notValid = True
            while(notValid):
                if (not sernum.isdigit()):
                    print("Oops! That was invalid input")
                    newser = input("Enter new Serial Number: ")
                else:
                    notValid = False
            
            # update the serialNo
            mycursor.execute("update digitalDisplay set serialNo = %s where serialNo = %s", (newser, sernum))
            showAllDisplays()
            option = input("\n\nEnter 1 to return to Update: ") # force to go back to update
            option = int(option)
            if(option == 1):
                update()
            else:
                main()

        # UPDATE SCHEDULAR SYSTEM
        elif(upoption==2):
            newsys = input("Enter new Schedular System: ")
            newsys = newsys.lower()

            # check for valid input
            notValid = True
            while(notValid):
                # if (newsys != "smart" or newsys != "virtue" or newsys != "random" ):
                if newsys not in ('smart', 'virtue', 'random'):
                    print("Oops! That was invalid input")
                    newsys = input("Enter new Scheduler System: ")
                    newsys = newsys.lower()
                else:
                    notValid = False

            # update scheduler system 
            mycursor.execute("update digitalDisplay set schedulerSystem = %s where serialNo = %s", (newsys, sernum))
            showAllDisplays()
            option = input("\n\nEnter 1 to return to Update: ")
            option = int(option)
            if(option == 1):
                update()
            else:
                main()

        # UPDATE MODEL NUMBER
        elif(upoption==3):
            newmod = input("Enter new Model Number: ")

            # check for valid input
            notValid = True
            while(notValid):
                if (not newmod.isdigit()):
                    print("Oops! That was invalid input")
                else:
                    notValid = False
            
            # update the model number
            mycursor.execute("update digitalDisplay set modelNo = %s where serialNo = %s", (newmod, sernum))
            showAllDisplays()
            option = input("\n\nEnter 1 to return to Update: ")
            option = int(option)
            if(option == 1):
                update()
            else:
                main()

        else:
            print("That is not a valid option")
            sleep(1)
            update()    

    # rerturn to main menu option   
    elif(option == 2):
        main()
    else:
        print("Not a valid input!") 
        sleep(1)
        update()


###########################################################
# LOGOUT 
# This function verifies users want to logout 
# and does so, returning user to the login function
###########################################################
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


###########################################################
# INSERT
# This functions handles new insertions into MODEl
# if the user wanted to add a Digital Display
###########################################################
def insertModel(modelNo):
    print("To insert a new model please type")
    width = input("Width: ")
    height = input("height: ")
    weight = input("Weight: ")
    depth = input("Depth: ")
    scrnSize = input("Screen Size: ")

    try:
        mycursor.execute("insert into model values(%s,%s,%s,%s,%s,%s);", (modelNo, width, height, weight, depth, scrnSize))
    except Exception: 
        print("invalid input! Try again")
        insertModel()


###########################################################
# SHOWALLDISPLAYS
# This is a simple helper function that
# displays all the digital displays when needed
###########################################################
def showAllDisplays():
    print("\nCurrent Digital Displays:")
    mycursor.execute("select * from digitaldisplay;")

    counter = 1
    for x in mycursor:
        print(counter,".\n Serial Number: ", x[0], "\n\tSchedular System: ",x[1], "\n\tModel Number: ", x[2])
        counter += 1
        
login()

