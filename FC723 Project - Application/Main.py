# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 17:07:12 2026

@author: bu3li
"""

# Global variables used to build the aircraft seating map
rows = ["A","B","C","D","E","F"]
seat_numbers = range(1,81)

storage_seats = {
    "77D","78D",
    "77E", "78E",
    "77F", "78F"
} # These seats cannot be booked

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
    
    
    if status == "F":
        seat_map[seat_code] = "R"
        print(f"Seat {seat_code} has been booked successfully.")
    elif status == "R":
        print(f"Seat {seat_code} is already booked.")
    elif status == "S":
        print(f"Seat {seat_code} is a storage area and cannot be booked.")


def free_seat(seat_map):
    """
    Frees a reserved seat by changing its status from R back to F.
    The function does not allow storage spaces to be changed.
    """
    seat_code = get_seat_code()

    if seat_code is None:
        return

    status = seat_map[seat_code]

    if status == "R":
        seat_map[seat_code] = "F"
        print(f"Seat {seat_code} has been freed successfully.")
    elif status == "F":
        print(f"Seat {seat_code} is already free.")
    elif status == "S":
        print(f"Seat {seat_code} is a storage area and cannot be freed.")
        
        
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

    seat_map = create_seat_map()

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