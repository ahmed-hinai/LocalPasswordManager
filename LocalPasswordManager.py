### IMPORTS ###
import sys
import os, signal
import subprocess
import json
from getpass import getpass
import time
from pathlib import Path
#Create store directory
password_store_filename = str(Path.home())+"/Scripts/LocalPasswordManager/passwordStore.json"
os.makedirs(os.path.dirname(password_store_filename), exist_ok=True)


state = True

def mainMenu():

    subprocess.run('figlet -f small "Password Manager"', shell=True)
    options_list = ['gen to generate a random secure password', 'add to add a new account', 'list to list currently stored passwords', 'account name to retrieve password', 'clear to clear password from clipboard', 'remove to remove account','exit to exit' ]

    print("---------------------------------------------------")
    print("USE:\n")
    for i in range(len(options_list)):
        print("| {}".format(options_list[i])+"")
    print("---------------------------------------------------\n")
mainMenu()
def generatePassword(show_password):
    if not show_password:
        random_string = subprocess.getoutput('openssl rand -base64 15 | grep -v "ب"') #why did i add this letter? check later
        subprocess.run('echo '+str(random_string)+' | xclip -selection clipboard', shell=True)
        print("Password generated and copied to your clipboard")
    else:
        randomString = subprocess.getoutput('openssl rand -base64 15 | grep -v "ب"')
        subprocess.run('echo '+str(random_string)+' | xclip -selection clipboard', shell=True)
        print("Password: "+str(random_string)+" generated and copied to your clipboard")


def addAccount():
    password_map = {}
    with open(password_store_filename,'r') as file:
        password_map = json.loads(file.read())
        print('Account name?')
        new_account = input()
        assert len(new_account) != 0, "account name length cannnot be zero"
        print('Account password?')
        new_password = getpass()
        assert len(new_password) != 0, "password length cannot be zero" 
        password_map[new_account] = new_password
    with open(password_store_filename,'w') as file:
        file.write(json.dumps(password_map))
        print("Password added.")

def listAccounts():
    password_map = {}
    with open(password_store_filename,'r') as file:
        password_map = json.loads(file.read())
        account_list = [account for account in password_map.keys()]
        print("---------------------------------------------------")
        for i in range(len(account_list)):
            print("| {0:10}".format(account_list[i])+"")
        print("---------------------------------------------------")

def removeAccount():
    password_map = {}
    with open(password_store_filename, 'r') as file:
        password_map = json.loads(file.read())
        account_name = input("Account name: ")
        if account_name in password_map:
            print("Account exists, are you sure you want to remove it? (y/n)")
            if input() == 'y':
                password = getpass()
                if password == password_map[account_name]:
                    del password_map[account_name]
                    print("Account removed.")
                else:
                    print("Wrong password. Account was not removed.")
        else:
            print("No matching account name.")

    with open(password_store_filename,'w') as file:
        file.write(json.dumps(password_map))

def getPassword(command):
    password_map = {}            
    with open(password_store_filename,'r') as file:
        password_map = json.loads(file.read())
    if '-c' not in command:
        try:

            if command in password_map:
                print("copied to clipboard!")
                subprocess.run('echo '+str(password_map[command])+' | xclip -selection clipboard', shell=True)
            else:
                print("Sorry I don't know what that means")
                mainMenu()
        except Exception as e:
            print("Password was not copied")
            print(e)
            
    else:
        try:
            int(command[-1]) is int
            if command[:command.index('-c')-1] in password_map:
                subprocess.run('echo '+str(password_map[command[:command.index('-c')-1]])+' | xclip -selection clipboard', shell=True)
                time_until_clear = command[command.index('-c')+3:]
                print('Copied to clipboard. Clear and exit in '+str(time_until_clear)+' seconds')
                time.sleep(int(time_until_clear))
                subprocess.run('echo "" | xclip -selection clipboard', shell=True)
                time.sleep(0.5)
                state = False
                os.kill(os.getppid(), signal.SIGHUP)
            else:
                print("Sorry I don't know what that means")
                mainMenu()
        except:
            if command[:-3] in password_map:
                subprocess.run('echo '+str((password_map[command[:-3]]))+' | xclip -selection clipboard', shell=True)
                print('Copied to clipboard. No time given, Clear and exit in 20 seconds')
                time.sleep(int(20))
                subprocess.run('echo "" | xclip -selection clipboard', shell=True)
                time.sleep(0.5)
                state = False
                os.kill(os.getppid(), signal.SIGHUP)
            else:
                print("Sorry I don't know what that means")
                mainMenu()

while state == True:
    command = str(input())

    try:
        match command:
            case 'gen':
                if '-s' not in command:
                    generatePassword(False)
                if '-s' in command:
                    generatePassword(True)

            case 'add':
                addAccount()

            case "list":
                listAccounts()

            case "remove":
                removeAccount() 

            case "clear":
                subprocess.run('echo "" | xclip -selection clipboard', shell=True)
                print("Password cleared from clipboard")

            case 'exit':
                state = False
                os.kill(os.getppid(), signal.SIGHUP)
                break

            case "clear and exit":
                subprocess.run('echo "" | xclip -selection clipboard', shell=True)
                print("Password cleared from clipboard")
                time.sleep(1)
                state = False
                os.kill(os.getppid(), signal.SIGHUP)
                break

            case 'hello':
                print('Hi')
            case 'hi':
                print('hello')

            case _:
                getPassword(command)


    except Exception as e:
        print("Sorry something wasn't quite right, try again.")
        print(e)


def main():
    pass
if __name__ == "__main__": main()
