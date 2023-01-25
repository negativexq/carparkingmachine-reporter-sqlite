from datetime import datetime
import math
import sqlite3
import os
import sys

class ParkedCar:
    def __init__(self, id, license_plate, check_in, check_out=None, parking_fee=0.0):
        self.id = id
        self.license_plate = license_plate
        self.check_in = check_in
        self.check_out = check_out
        self.parking_fee = parking_fee
class CarParkingMachine:
    instances = []  # class-level variable to store all the CarParkingMachine instances
    def __init__(self,id, capacity=10, hourly_rate=2.50):
        self.capacity = capacity
        self.id = id
        self.hourly_rate = hourly_rate
        self.parked_cars = {}
        self.logger = CarParkingLogger(id)
        self.db_conn = sqlite3.connect(os.path.join(sys.path[0], 'carparkingmachine.db'))
        self.db_conn.execute(
            """CREATE TABLE IF NOT EXISTS parkings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_parking_machine TEXT NOT NULL,
                license_plate TEXT NOT NULL,
                check_in TEXT NOT NULL,
                check_out TEXT DEFAULT NULL,
                parking_fee NUMERIC DEFAULT 0 
            );"""
        )
        CarParkingMachine.instances.append(self)

    def check_in(self, license_plate:str, time=datetime.now()) -> bool:
        for instance in CarParkingMachine.instances:
            if license_plate in instance.parked_cars:
                return False
        car = ParkedCar(self.id, license_plate, time)
        parked_car = self.insert(car)
        if self.capacity <= len(self.parked_cars):
            return False
        elif parked_car is not None:
            self.parked_cars[license_plate] = parked_car
            return True
        else:
            return False

    def check_out(self, license_plate: str) -> float:
        if license_plate in self.parked_cars:
            parking_fee = self.get_parking_fee(license_plate)
            car = self.parked_cars[license_plate]
            car.check_out = datetime.now()
            car.parking_fee = parking_fee
            self.update(car)

            # Remove the car from the parked_cars dictionary
            self.parked_cars.pop(license_plate)

            return parking_fee
        else:
            parking_fee = self.get_parking_fee(license_plate)
            now=datetime.now()
            self.db_conn.execute("UPDATE parkings SET check_out=?, parking_fee=? WHERE license_plate=?",
            (now, parking_fee, license_plate,)
            )

            self.db_conn.commit()


            return parking_fee


    def get_parking_fee(self, license_plate: str) -> float:
        if license_plate in self.parked_cars:
            car = self.parked_cars[license_plate]
            current_time = datetime.now()
            duration = current_time - car.check_in

            hourly_rate = self.hourly_rate
            max_fee = 24 * hourly_rate 
            duration_hours = math.ceil(duration.total_seconds() / 3600)
            parking_fee = min(duration_hours * hourly_rate, max_fee)

            return parking_fee
        else:
            # Connect to the database
            cursor = self.db_conn.execute("SELECT * FROM parkings WHERE license_plate=?", (license_plate,))
            row = cursor.fetchone()

            if row is not None:
                # The license plate was found in the database
                # Extract the check_in time and hourly rate from the database row
                check_in_str = row[3]
                hourly_rate = self.hourly_rate
                check_in = datetime.strptime(check_in_str, '%Y-%m-%d %H:%M:%S.%f')

                # Calculate the duration and parking fee
                current_time = datetime.now()
                duration = current_time - check_in
                max_fee = 24 * hourly_rate 
                duration_hours = math.ceil(duration.total_seconds() / 3600)
                parking_fee = min(duration_hours * hourly_rate, max_fee)

                return parking_fee
            


    def find_by_id(self, id) -> ParkedCar:
        cursor = self.db_conn.execute(
            "SELECT * FROM parkings WHERE id=?", (id,)
        )
        row = cursor.fetchone()
        if row is not None:
            return ParkedCar(*row)
        else:
            return None

    def find_last_checkin(self, license_plate: str) -> int:
        cursor = self.db_conn.execute(
            "SELECT id FROM parkings WHERE license_plate=? AND check_out IS NULL",
            (license_plate,)
        )
        row = cursor.fetchone()
        if row is not None:
            return row[0]
        else:
            return None
    def insert(self, parked_car: ParkedCar) -> ParkedCar:
        cursor = self.db_conn.execute(
            "INSERT INTO parkings (car_parking_machine, license_plate, check_in) VALUES (?, ?, ?)",
            (self.id, parked_car.license_plate, parked_car.check_in)
        )
        parked_car.id = cursor.lastrowid
        self.db_conn.commit()
        return parked_car

    def update(self, parked_car: ParkedCar) -> None:
        self.db_conn.execute(
            "UPDATE parkings SET check_out=?, parking_fee=? WHERE id=?",
            (parked_car.check_out, parked_car.parking_fee, parked_car.id)
        )
        self.db_conn.commit()

class CarParkingLogger:
    def __init__(self, cpm_id):
        self.cpm_id = cpm_id

    def log_check_in(self, license_plate):
        now = datetime.now()
        timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
        log_line = f"{timestamp};cpm_name={self.cpm_id};license_plate={license_plate};action=check-in"
        print(log_line)

    def log_check_out(self, license_plate, fee):
        now = datetime.now()
        timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
        log_line = f"{timestamp};cpm_name={self.cpm_id};license_plate={license_plate};action=check-out;parking_fee={fee}"
        print(log_line)

def main():
    print("""[I] Check-in car by license plate
[O] Check-out car by license plate
[Q] Quit program:""")  
    parking_machine = CarParkingMachine(id="North", capacity=10, hourly_rate=2.50)
    parking_logger = CarParkingLogger(cpm_id=parking_machine.id)
    while True:
        user_input = input().lower()
        if user_input == "i":
            license_plate = input()
            if parking_machine.check_in(license_plate) == True:
                print("License registered")
                parking_logger.log_check_in(license_plate)
            else:
                print("Capacity reached")                
        elif user_input == "o":
            license_plate = input()
            if license_plate not in parking_machine.parked_cars:
                print("Car not found")
            else:
                parking_fee = parking_machine.check_out(license_plate)
                print(f"Parking fee: {parking_fee}")
                parking_logger.log_check_out(license_plate, parking_fee)
        elif user_input == "c":
            print(f"Capacity: {parking_machine.capacity}")
            print(f"Number of cars: {len(parking_machine.parked_cars)}")
        elif user_input == "q":
            break

if __name__ == "__main__":
    main()