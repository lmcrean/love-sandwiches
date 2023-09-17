import json
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user. 
    """

    while True: # True
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")
  
        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")

        if validate_data(sales_data): # if validate_data(sales_data) == True:
            print("Data is valid!")
            break # break out of the while loop if data is valid

    return sales_data
  
def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int, or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
            print(f"Invalid data: {e}, please try again.\n")
            return False # return False if errors are raised.
    
    return True # return True if no errors are raised. This means that the function will return True if the try block is successful. If unsuccessful, the except block will run and return False. For example, if the user enters 5 numbers instead of 6, the except block will run and return False.

def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided.
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales") # access the sales worksheet
    sales_worksheet.append_row(data) # append the data provided as a new row at the bottom of the sales worksheet
    print("Sales worksheet updated successfully.\n")

def update_surplus_worksheet(data):
    """
    Update surplus worksheet, add new row with the list data provided.
    """
    print("Updating surplus worksheet...\n")
    surplus_worksheet = SHEET.worksheet("surplus") # access the surplus worksheet
    surplus_worksheet.append_row(data) # append the data provided as a new row at the bottom of the surplus worksheet
    print("Surplus worksheet updated successfully.\n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values() # access the stock worksheet and get all values
    stock_row = stock[-1] # get the last row of data from the stock worksheet. -1 is the index of the last item in a list. This number is chosen because the last row of data in the stock worksheet is the most recent data.

    surplus_data = [] # create an empty list called surplus_data


    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus) # append the surplus value to the surplus_data list
        print(f"Surplus for item: {surplus}\n")
    print(surplus_data)

def main():
    """
    Run all program functions
    """
    data = get_sales_data() # call the get_sales_data function and store the returned data in a variable called data
    sales_data = [int(num) for num in data] # convert the data provided by the user into integers. num is a variable that represents each item in the list data. 
    update_sales_worksheet(sales_data) # call the update_sales_worksheet function and pass in the sales_data list as an argument. This will add the sales_data list as a new row in the sales worksheet.
    calculate_surplus_data(sales_data) # call the calculate_surplus_data function and pass in the sales_data list as an argument. This will calculate the surplus data for each item type.
    new_surplus_data = calculate_surplus_data(sales_data) # call the calculate_surplus_data function and pass in the sales_data list as an argument. This will calculate the surplus data for each item type and store the returned data in a variable called new_surplus_data.
    update_surplus_worksheet(new_surplus_data) # call the update_surplus_worksheet function and pass in the new_surplus_data list as an argument. This will add the new_surplus_data list as a new row in the surplus worksheet.
    print(new_surplus_data) # print the new_surplus_data list to the terminal

print("Welcome to Love Sandwiches Data Automation")

main() # call the main function to run the program. Must be below the function definition.