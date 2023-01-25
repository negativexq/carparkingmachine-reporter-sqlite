# carparkingmachine-reporter-sqlite

# Parking Machine

This is a class-based Python program that simulates a parking machine. The program allows users to check-in and check-out cars, and calculate the parking fee based on the duration of the parking. The program also uses a SQLite database to keep track of all the parked cars, and a logger to log all the parking transactions.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3
- SQLite3

### Installing

- Clone the repository to your local machine
- Install the required modules using pip:


## Using the program

The program has two main classes: `ParkedCar` and `CarParkingMachine`.

`ParkedCar` class represents a parked car, and it has the following attributes:
- `id`: id of the car parking machine where the car is parked
- `license_plate`: license plate number of the car
- `check_in`: check-in time of the car
- `check_out`: check-out time of the car (default: None)
- `parking_fee`: parking fee of the car (default: 0.0)

`CarParkingMachine` class represents a parking machine, and it has the following attributes:
- `capacity`: maximum capacity of the parking machine (default: 10)
- `id`: id of the parking machine
- `hourly_rate`: hourly rate of the parking machine (default: 2.50)
- `parked_cars`: dictionary of parked cars, where the keys are the license plate numbers, and the values are the `ParkedCar` objects
- `logger`: a logger object to log all the parking transactions
- `db_conn`: a SQLite3 connection object to the parking machine database

The `CarParkingMachine` class has the following methods:
- `check_in(license_plate: str, time=datetime.now()) -> bool`: allows a car to check-in to the parking machine. It returns `True` if the car is successfully checked-in, and `False` otherwise.
- `check_out(license_plate: str) -> float`: allows a car to check-out of the parking machine. It returns the parking fee of the car.
- `get_parking_fee(license_plate: str) -> float`: calculates and returns the parking fee of the car.

## Authors

* **[Ömer Faruk KOÇ]** - [Github](https://github.com/negativexq)

