

from colorama import Fore, Back, Style
import time
import random
from operator import itemgetter



# import mysql.connector
# from mysql.connector import Error


def importfromdatabase():



    ## OBTAIN ALL DATA FROM SQL DATABASE

    using_sql_database = False # when taking data directly from sql database -> True 
    sql_data = [] # this list will contain all arays with data from sql database.

    if using_sql_database == True: ## this section will be commented since this syntax in not correct
        print("using sql_database")
        try:
            connection = mysql.connector.connect(host='',
                                                database='',
                                                user='',
                                                password='')

            sql_select_Query = "select * from Bluetooth_devices"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()
            print("Total number of rows in Laptop is: ", cursor.rowcount)
            
            

        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
                print("MySQL connection is closed")
                
                
        for line in records:
            sql_data_list = []
            for entity in line:
                sql_data_list.append(entity)
            
            #sql_data_list = list(str.split((items))) # convert each line from string entities to 1 list entity
            sql_data.append(sql_data_list)

    else:
        f = open('Testdatasql.txt', 'r') # open sql data file file
        lines = f.readlines() # copy all data into local memo
        f.close # close the file.

        for line in lines:
            sql_data_list = list(str.split((line))) # convert each line from string entities to 1 list entity
            sql_data.append(sql_data_list) # append this new list to the general sql_data list
        #sql_data.pop(0) # remove the first entry (names of column)    
        
        #print("sql_data = \n\n ", sql_data)

    #random.shuffle(sql_data) # for testing purposes

    sql_data = sorted(sql_data, key=itemgetter(0)) # sort data for increased speed
    #print(sql_data)
    #print("\n\n random sql_data = ", sql_data)
    index_found = 0
    found = False
    UIM = [] # unidentified measurements
    matches = [] # this will store all matched entities

    starttime = time.time()

    while len(sql_data) > 0: # for all entries in sql_data:   # time,name, mac, gemac
        measurement = sql_data[0]
        print("Measurement: \n",measurement)
        #print("\nsearching for match of: ", measurement, "size: ", len(sql_data))
        searched_entry = measurement
        if len(sql_data) == 1:
            #print("\t no match shall be found, uneven #measurements")
            pass
        sql_data.pop(0) # remove the searched entry from the sql table
        #print("\t removed this entry from sql_table into local memory: table size:", len(sql_data))
        index_found = 0
        while len(sql_data) > 0: # rec_measurement in sql_data: # for each entry in sql_table (minus the one we are searching)
            if index_found < len(sql_data): 
                rec_measurement = sql_data[index_found]
                found = False
                #print("\t looking at entry: ", index_found, "data: ", rec_measurement)
                if searched_entry[0] == rec_measurement[0]: # check if the time stamps are equal
                    #print("\t equal time stamps")
                    if searched_entry[3] == rec_measurement[2]: # check if the found mac is the advertised mac by this entry
                        #print("\t\t found mac == advertised mac by this entry")
                        if rec_measurement[3] == searched_entry [2]: # if the entries found mac equals the mac of the initial entry
                            #print("\t\t\t entries found mac equals the mac of initial entry")
                            found = True
                            #print(Fore.GREEN + "\t\t\t match found with: ", rec_measurement)
                            #print(Fore.WHITE)
                            match = []
                            match.append(measurement[1]) # append the names of the measurements together
                            match.append(rec_measurement[1]) # append the names of the measurements together
                            match.append(rec_measurement[0]) # append the time
                            match.append(measurement[4])
                            print(match, "\n")
                            #print("\t\t\t adding", match, "to the matches list") # append the names of the match to total matches
                            matches.append(match) # add these names as an entry into a list
                if found == True: # if a match was found
                    #print("\t removing", sql_data[index_found], "from sql_table")    
                    sql_data.pop(index_found)
                    break # we can stop searching for this entry
                else: # if not
                    #print("\t no match, start looking at next entry for a match")
                    index_found = index_found + 1 # we start searching in the next entry
            else:
                #print(Fore.RED + "\t\tno match found for: ", measurement, "adding entry to UIM")
                #print(Fore.WHITE) 
                UIM.append(measurement)
                break
        #print("\t\t size of sql table = ", len(sql_data))


    #print(UIM)

    return matches

if __name__ == '__main__':
    importfromdatabase()
