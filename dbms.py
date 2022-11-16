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

print("=====================")
print("Welcome to your DBMS!")
print("=====================")

logged_in = False

while(not logged_in):
    hst = input("Please input hostname: ")
    dtbs = input("Please enter name of database: ")
    usrnm = input("Username: ")
    pswrd = input("Password: ")

    try:
        mydb = mysql.connector.connect(
            host=hst,
            user=usrnm,
            password=pswrd,
            database=dtbs
        )
        mycursor = mydb.cursor()
        logged_in = True
    except Exception:
        print("Uh oh, there was a problem connecting. Try logging in again.\n")
        

print(f"\nSuccessful login! Weclome to '{dtbs}!")
print("=======================================")

sleep(3)
clear_screen()




def main():
    mycursor.execute("SHOW tables;")
    print(mycursor)

    for x in mycursor:
        print(x)

main()