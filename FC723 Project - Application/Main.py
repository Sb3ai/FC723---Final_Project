# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 17:07:12 2026

@author: bu3li
"""

# Imported libaries
import random
import sqlite3
import string
from pathlib import Path



# Global variables used to build the aircraft seating map
rows = ["A","B","C","D","E","F"]
seat_numbers = range(1,81)

storage_seats = {
    "77D","78D",
    "77E", "78E",
    "77F", "78F"
} # These seats cannot be booked

# The database file will be created inside the same folder as main.py
database_path = Path(__file__).with_name("bookings.db")

def create_database():
    """
    Creates the bookings database table if it does not already exist.
    The table scores teh booking reference, customer details, and the seat linked to the booking.
    """
    
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_reference TEXT PRIMARY KEY,
            passport_number TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            seat_row TEXT NOT NULL,
            seat_column INTEGER NOT NULL,
            seat_code TEXT NOT NULL UNIQUE
        )
    """)
    connection.commit()
    connection.close()
    
def create_seat_map():
    """
    This function is to create the aircraft seating map.
    F = free seat
    S = Storage area
    """
    seat_map = {}
    
    for row in rows:
        for number in seat_numbers:
            seat_code = f"{number}{row}"
            
            if seat_code in storage_seats:
                seat_map[seat_code] = "S"
            else:
                seat_map[seat_code] = "F"
        
    return seat_map

def load_existing_bookings(seat_map):
    # Loads the existing bookings from the database to the seat map
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    
    cursor.execute("SELECT booking_reference, seat_code FROM bookings")
    bookings = cursor.fetchall()
    
    connection.close()
    
    for booking_reference, seat_code in bookings:
        if seat_code in seat_map and seat_map[seat_code] == "F":
            seat_map[seat_code] = booking_reference

def booking_reference_exists(booking_reference):
    """
    Checks whether a booking reference already exists in the database.
    """

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT booking_reference FROM bookings WHERE booking_reference = ?",
        (booking_reference,)
    )

    result = cursor.fetchone()
    connection.close()

    return result is not None


def generate_booking_reference():
    """
    Generates a unique booking reference.

    The algorithm uses uppercase letters and digits.
    It creates an 8-character reference, then checks the database.
    If the reference already exists, it generates another one.
    """

    characters = string.ascii_uppercase + string.digits

    while True:
        booking_reference = ""

        for i in range(8):
            booking_reference += random.choice(characters)

        if not booking_reference_exists(booking_reference):
            return booking_reference


def get_customer_details():
    """
    Gets customer details needed for a booking.
    """

    passport_number = input("Enter passport number >> ").strip()
    first_name = input("Enter first name >> ").strip()
    last_name = input("Enter last name >> ").strip()

    if passport_number == "" or first_name == "" or last_name == "":
        print("Customer details cannot be empty.")
        return None

    return passport_number, first_name, last_name


def save_booking_details(booking_reference, passport_number, first_name, last_name, seat_code):
    """
    Saves customer booking details into the database.
    """

    seat_row = seat_code[-1]
    seat_column = int(seat_code[:-1])

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO bookings (
                booking_reference,
                passport_number,
                first_name,
                last_name,
                seat_row,
                seat_column,
                seat_code
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            booking_reference,
            passport_number,
            first_name,
            last_name,
            seat_row,
            seat_column,
            seat_code
        ))

        connection.commit()
        connection.close()
        return True

    except sqlite3.IntegrityError:
        connection.close()
        print("This booking could not be saved because the seat or reference already exists.")
        return False


def delete_booking_details(booking_reference):
    """
    Deletes booking details from the database when a seat is freed.
    """

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM bookings WHERE booking_reference = ?",
        (booking_reference,)
    )

    connection.commit()
    connection.close()

def show_menu(): # User command line interface menu to view options
    print("\n========== Apache Airlines Seat Booking System ==========")
    print("[1] Check availability of seat")
    print("[2] Book a seat")
    print("[3] Free a seat")
    print("[4] Show booking status")
    print("[5] Find first available seat by row")
    print("[6] Exit program")

def get_seat_code():
    """
    Gets and validates a full seat code from the user.
    A valid seat code contains a seat number from 1 to 80
    followed by a row letter from A to F, for example 1A or 77D.
    """

    seat_code = input("Enter seat code, for example 1A or 80F >> ").strip().upper()

    if len(seat_code) < 2:
        print("Invalid seat code. Please enter a seat such as 1A or 77D.")
        return None

    seat_number = seat_code[:-1]
    seat_row = seat_code[-1]

    if seat_row == "X":
        print("This is an aisle, not a seat.")
        return None

    if seat_row not in rows:
        print("Invalid row. Please enter a row from A to F.")
        return None

    if not seat_number.isdigit():
        print("Invalid seat number. Please enter a number from 1 to 80.")
        return None

    seat_number = int(seat_number)

    if seat_number < 1 or seat_number > 80:
        print("Invalid seat number. Please enter a number from 1 to 80.")
        return None

    return f"{seat_number}{seat_row}"

def check_availability(seat_map): # Checks whether a selected seat is free or booked or unavailable.
    seat_code = get_seat_code()
    
    if seat_code is None: # Simple condition to check if seat_code is valid or not.
        return
    
    status = seat_map[seat_code]
    
    if status == "F":
        print(f"Seat {seat_code} is available.")
    elif status == "R":
        print(f"Seat {seat_code} is already booked.")
    elif status == "S":
        print(f"Seat {seat_code} is a storage area and cannot be booked.")

def book_seat(seat_map):
    """
    Books a selected seat if the current status is F.
    The function prevents bookings on reserved seats and storage spaces.
    """
    seat_code = get_seat_code()
    
    if seat_code is None:
        return
    
    status = seat_map[seat_code]
    
    if status == "S":
        print(f"Seat {seat_code} is a storage area and cannot be booked.")
        return

    if status != "F":
        print(f"Seat {seat_code} is already booked.")
        print(f"Booking reference: {status}")
        return
    
    customer_details = get_customer_details()

    if customer_details is None:
        return
    passport_number, first_name, last_name = customer_details
    booking_reference = generate_booking_reference()

    booking_saved = save_booking_details(
        booking_reference,
        passport_number,
        first_name,
        last_name,
        seat_code
    )

    if booking_saved:
        seat_map[seat_code] = booking_reference
        print(f"Seat {seat_code} has been booked successfully.")
        print(f"Booking reference: {booking_reference}")



def free_seat(seat_map):
    """
    Frees a reserved seat by changing its status from R back to F.
    The function does not allow storage spaces to be changed.
    """
    seat_code = get_seat_code()

    if seat_code is None:
        return

    status = seat_map[seat_code]

    if status == "F":
            print(f"Seat {seat_code} is already free.")
    elif status == "S":
        print(f"Seat {seat_code} is a storage area and cannot be freed.")
    else:
        booking_reference = status
        seat_map[seat_code] = "F"
        delete_booking_details(booking_reference)
        print(f"Seat {seat_code} has been freed successfully.")
        print(f"Booking reference {booking_reference} was removed from the database.")

        
def print_row_status(seat_map, row): # Prints one row of the aircraft in smaller sections.

    print(f"\nRow {row}:")

    for start in range(1, 81, 20):
        end = start + 19
        seats = []

        for number in range(start, end + 1):
            seat_code = f"{number}{row}"
            seats.append(f"{seat_code}:{seat_map[seat_code]}")

        print("  ".join(seats))


def show_booking_status(seat_map): #Shows the full booking status of the aircraft.
    #Also shows a summary count of free, booked, and storage seats.

    print("\n========== Booking Status ==========")
    print("F = Free | R = Reserved | S = Storage | X = Aisle")

    print_row_status(seat_map, "A")
    print_row_status(seat_map, "B")
    print_row_status(seat_map, "C")

    print("\nAisle:")
    print("X " * 80)

    print_row_status(seat_map, "D")
    print_row_status(seat_map, "E")
    print_row_status(seat_map, "F")

    free_count = 0
    booked_count = 0
    storage_count = 0

    for status in seat_map.values():
        if status == "F":
            free_count += 1
        elif status == "R":
            booked_count += 1
        elif status == "S":
            storage_count += 1

    print("\n========== Seat Summary ==========")
    print(f"Free seats: {free_count}")
    print(f"Booked seats: {booked_count}")
    print(f"Storage spaces: {storage_count}")



def find_available_seat_by_row(seat_map):
    """
    Finds the first available seat in a selected row.
    This is an extra airline booking feature.
    It helps the user quickly find a free seat without checking seats manually.
    """

    row = input("Enter preferred row (A-F): ").strip().upper()

    if row not in rows:
        print("Invalid row. Please enter a row from A to F.")
        return

    for number in seat_numbers:
        seat_code = f"{number}{row}"

        if seat_map[seat_code] == "F":
            print(f"The first available seat in row {row} is {seat_code}.")
            return

    print(f"There are no available seats in row {row}.")
    
def main(): # Runs the main program

    create_database()
    seat_map = create_seat_map()
    load_existing_bookings(seat_map)
    
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            check_availability(seat_map)
        elif choice == "2":
            book_seat(seat_map)
        elif choice == "3":
            free_seat(seat_map)
        elif choice == "4":
            show_booking_status(seat_map)
        elif choice == "5":
            find_available_seat_by_row(seat_map)
        elif choice == "6":
            print("Thank you for using Apache Airlines Seat Booking System.")
            break
        else:
            print("Invalid option. Please choose a number from 1 to 6.")


if __name__ == "__main__":
    main()