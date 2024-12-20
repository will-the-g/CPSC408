#imports
from helper import helper
from db_operations import db_operations
from datetime import datetime

#global variables
db_ops = db_operations(host="localhost", user="root", password="", database="rideshare")
db_ops.create_tables()
db_ops.populate_tables()


def start():
    print('''Select one of the following:
          1. I do not have an account
          2. I have a rider account
          3. I have a driver account
          4. Exit
          ''')
    return helper.get_choice([1,2,3,4])

def createAccount():
    print("Would you like to create a driver(Enter 1) or rider(Enter 2) account: ")
    choice = helper.get_choice([1,2])
    next_ID_query = "SELECT COUNT(*) FROM accounts;"
    next_ID = db_ops.single_record(next_ID_query) + 1
    # since were not allowing users to delete accounts, we can just take the total # of accounts and add 1
    password = input("Enter to password you want for you're account: ")
    add_account_query = '''INSERT INTO accounts (id, password) VALUES (%s, %s);'''
    db_ops.modify_query_params(add_account_query, (next_ID, password))
    if choice == 1:
        # also add info to driverAccounts table if driverAccount
        add_driverAccount_query = '''INSERT INTO driverAccounts (driverID) VALUES (%s);'''
        db_ops.modify_query_params(add_driverAccount_query, (next_ID,))
    print(f"Account Created! Your ID is {next_ID}")





# function for logging into an account
def login():
    # grabs ID and makes sure its an integer greater than 0
    account_id = input("Enter your ID:")
    while account_id.isdigit() is False:
        account_id = input("Enter a integer greater than 0 for your ID: ")
    account_id = int(account_id)
    # grabs the account info with the given ID
    id_query = f'SELECT * FROM accounts WHERE id = "{account_id}";'
    account_info = db_ops.single_row(id_query)
    # checks if the account with the given ID exists
    if not account_info:
        print(f'ID: {account_id} does not exist, Enter a different id')
        return
    # gets the stored password and compares it to the given password
    stored_password = account_info[1]
    while True:
        attempt = input("What is your password? ")
        if attempt == stored_password:
            return account_id
        else:
            print('Wrong Password, enter 0 to leave, 1 to continue')
            choice = helper.get_choice([0,1])
            if choice == 0:
                return -1
    
        
# checks if the given account id is a driver or rider by checking if it exists in the driverAccount table
# Parameters: account_id of the user. driver is a boolean to print a certain message only if a rider is trying to login as a driver but not vice-versa
def driver_check(account_id, driver):
    id_check_query = f'SELECT * FROM driverAccounts WHERE driverID = {account_id}'
    id_check = db_ops.single_row(id_check_query)
    if id_check is None:
        if driver:
            print("Account is not a driver! Make a new account to become a driver")
        return False
    else:
        return True
    
# options for someone with a driver account to do. Parameters: account_id of user
def driver_functions(account_id):
    choice = 0
    while choice != 4:
        print('''Select one of the following:
            1. View Rating
            2. View Rides
            3. Activate/Deactive Driver Mode
            4. Log Out ''')
        choice = helper.get_choice([1,2,3,4])
        match choice:
            case 1:
                # Returns all rides with the given driverID
                rating_query = f'SELECT averageRating FROM driverAccounts WHERE driverID = {account_id}'
                print("Average rating:", db_ops.single_record(rating_query))
            case 2:
                # checks if any rides exist yet
                rides_count_query = f"SELECT COUNT(*) FROM rides WHERE driverID = {account_id}"
                count = db_ops.single_record(rides_count_query)
                if (count > 0):
                    # grabs all the rides and prints them nicely
                    rides_query = f"SELECT * FROM rides WHERE driverID = {account_id}"
                    rides = db_ops.select_query(rides_query)
                    for ride in rides:
                        print(f'''
                        Ride ID = {ride[0]}, 
                        Driver ID = {ride[1]},
                        Rider ID = {ride[2]},
                        Date Time = {ride[3].strftime("%Y-%m-%d %H:%M:%S")},
                        Pick Up Location = {ride[4]},
                        Drop Off Location = {ride[5]},    
                        Rating = {ride[6] if ride[6] != 0 else "No Rating Yet"}
                    ''')
                else:
                    print("No rides recorded")
            case 3:
                # switches the isActive boolean in the table for given driverID
                activation_query = f'UPDATE driverAccounts SET isActive = NOT isActive WHERE driverID = {account_id}'
                db_ops.modify_query(activation_query)
                # returns what the new isActive boolean in the table for given driverID to print out to user
                status_query = f'SELECT isActive FROM driverAccounts WHERE driverID = {account_id}'
                status = db_ops.single_record(status_query)
                if status:
                    print('Driver mode activated!')
                else:
                    print('Driver mode deactivated!')
            case 4:
                # does nothing since it will break out of while loop if choice = 4
                pass

# various functions that can be performed by the rider
# Parameters: account_id of the user
def rider_functions(account_id):
    choice = 0
    while choice != 4:
        print('''Select one of the following:
          1. View Rides
          2. Find a driver
          3. Rate my driver
          4. Log Out ''')
        choice = helper.get_choice([1,2,3,4])
        match choice:
            case 1:
                # Displays all rides to the user
                # first checks if any rides exist yet
                rides_count_query = f"SELECT COUNT(*) FROM rides WHERE riderID = {account_id}"
                count = db_ops.single_record(rides_count_query)
                if (count > 0):
                    # prints all existing rides if any
                    rides_query = f"SELECT * FROM rides WHERE riderID = {account_id}"
                    rides = db_ops.select_query(rides_query)
                    for ride in rides:
                        print(f'''
                        Ride ID = {ride[0]}, 
                        Driver ID = {ride[1]},
                        Rider ID = {ride[2]},
                        Date Time = {ride[3].strftime("%Y-%m-%d %H:%M:%S")},
                        Pick Up Location = {ride[4]},
                        Drop Off Location = {ride[5]},    
                        Rating = {ride[6] if ride[6] != 0 else "No Rating Yet"}
                    ''')
                else:
                    print("No rides recorded")
            case 2:
                # selects a random driverID from the driverAccounts table
                get_driver_ids_query = 'SELECT driverID FROM driverAccounts WHERE isActive = TRUE ORDER BY RAND() LIMIT 1;'
                driver_id = db_ops.single_record(get_driver_ids_query)
                # grabs the total rides to be able get the next rideID for the new Ride
                total_rides_query = 'SELECT COUNT(*) FROM rides;'
                total_rides = db_ops.single_record(total_rides_query)
                # tells who they are driven by and gets the pickup/dropoff location from user
                print(f'You will be driven by driver id = {driver_id}')
                pickup = input('Input the pick up location: ')
                dropoff = input('Input the drop off location: ')
                # adds ride to rides table
                add_ride_query = f'''INSERT INTO rides (rideID, driverID, riderID, startDateTime, pickup, dropoff) 
                            VALUES ({total_rides + 1}, {driver_id}, {account_id}, '{datetime.now()}', '{pickup}', '{dropoff}');'''
                db_ops.modify_query(add_ride_query)
                print("Ride Added! ")
            case 3:
                # gets the most recent ride with the given riderID
                recent_ride_query = f'SELECT * FROM rides WHERE rideID = (SELECT MAX(rideID) FROM rides WHERE riderID = {account_id});'
                ride = db_ops.select_query(recent_ride_query)[0]
                # checks with user to see if info is correct
                print("Is this information correct?(Yes = 1, No = 2): ")
                print(f'''
                        Ride ID = {ride[0]}, 
                        Driver ID = {ride[1]},
                        Rider ID = {ride[2]},
                        Date Time = {ride[3].strftime("%Y-%m-%d %H:%M:%S")},
                        Pick Up Location = {ride[4]},
                        Drop Off Location = {ride[5]},    
                        Rating = {ride[6] if ride[6] != 0 else "No Rating Yet"}
                        ''')
                choice = helper.get_choice([1,2])

                if choice == 1:
                    # Info is correct and asks the user for an integer rating 1-5
                    print('What is the rating you want to give to your most recent ride. Enter whole number 1-5')
                    rating = helper.get_choice([1,2,3,4,5])
                    # updates the rating with most recent rideID
                    change_rating_query = f'UPDATE rides SET rating = {rating} WHERE rideID = {ride[0]}'
                    db_ops.modify_query(change_rating_query)
                    # updates the averageRating and ratingCount of the driver in the driverAccounts table
                    get_driver_average_info_query = f'SELECT averageRating, ratingCount FROM driverAccounts WHERE driverID = {ride[1]}'
                    get_driver_average_info = db_ops.single_row(get_driver_average_info_query)
                    # update the average by taking the current average times the current count, adding the new rating. Then divide by the count+1
                    update_driver_average_info_query = f'''UPDATE driverAccounts
                    SET averageRating = {(float(get_driver_average_info[0]) * get_driver_average_info[1] + rating) / (get_driver_average_info[1] + 1)},
                    ratingCount = {get_driver_average_info[1] + 1} 
                    WHERE driverID = {ride[1]}'''
                    db_ops.modify_query(update_driver_average_info_query)
                    print('Rating Added! ')
                else:
                    # info is the wrong ride, so user will input the ID of a different ride they want to rate
                    rideID = input('Input the ID of the ride (integer greater than 0): ')
                    # makes sure its a integer greater than 0 
                    while rideID.isdigit() is False:
                        rideID = input('Input the ID of the ride (integer greater than 0): ')
                    # converts to int
                    rideID = int(rideID)
                    # checks if the ride with the given rideID exists
                    existance_check_query = f'SELECT * FROM rides WHERE rideID = {rideID}'
                    existance_check = db_ops.select_query(existance_check_query)[0]
                    if existance_check and int(existance_check[2]) == account_id:
                        # asks if the info is correct
                        print("Is the following information correct? (1: Yes, 2: No)")
                        print(f'''
                        Ride ID = {existance_check[0]}, 
                        Driver ID = {existance_check[1]},
                        Rider ID = {existance_check[2]},
                        Date Time = {existance_check[3].strftime("%Y-%m-%d %H:%M:%S")},
                        Pick Up Location = {existance_check[4]},
                        Drop Off Location = {existance_check[5]},    
                        Rating = {existance_check[6] if existance_check[6] != 0 else "No Rating Yet"}
                        ''')
                        choice = helper.get_choice([1,2])
                        if choice == 1:
                            # gets integer rating 1-5
                            print('What is the rating you want to give to your most recent ride. Enter whole number 1-5')
                            rating = helper.get_choice([1,2,3,4,5])
                            # changes the given rating of the given rideID
                            change_rating_query = f'UPDATE rides SET rating = {rating} WHERE rideID = {rideID}'
                            db_ops.modify_query(change_rating_query)
                            # updates the averageRating and ratingCount of the driverID of the given rideID
                            get_driver_average_info_query = f'SELECT averageRating, ratingCount FROM driverAccounts WHERE driverID = {existance_check[1]}'
                            get_driver_average_info = db_ops.single_row(get_driver_average_info_query)
                            update_driver_average_info_query = f'''UPDATE driverAccounts 
                            SET averageRating = {(float(get_driver_average_info[0]) * get_driver_average_info[1] + rating) / (get_driver_average_info[1] + 1)},
                            ratingCount = {get_driver_average_info[1] + 1} 
                            WHERE driverID = {ride[1]}'''
                            db_ops.modify_query(update_driver_average_info_query)
                        else:
                            # restarts from rider function selection screen if it's not correct
                            pass
                    else:
                        if float(existance_check[2]) != account_id:
                            print('You are not the rider for the given rideID')
                        else:
                            print('The ride with the given rideID does not exist.')
                    

            case 4:
                pass

# start
while True:
    choice = start()
    match (choice):

        
        case 1:
            # makes an account
            createAccount()

        
        case 2:
            # log into a rider account
            account_id = login()
            # checks if the given id is above 0 (-1 is password fail) and checks if it's a rider account by returning false to the driver_check() method
            if account_id > 0 and not driver_check(account_id, False):
                print('Login complete')
                rider_functions(account_id)

        
        case 3:
            # log into a driver account
            account_id = login()
            # does same as above but checks if it returns true to the driver_check() method
            if account_id > 0 and driver_check(account_id, True):
                print('Login complete')
                driver_functions(account_id)
        case 4:
            break


db_ops.destructor()
