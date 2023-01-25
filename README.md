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

# Carparkingreports.py

This file contains functions that generate various reports on the parked cars in the car parking system.

## Functions
- `generate_parked_cars_report(machine_name, from_date, to_date)`: generates a CSV report of all the parked cars in the specified car parking machine within the specified date range.
- `generate_total_fee_report(from_date, to_date)`: generates a CSV report of the total parking fees for each car parking machine within the specified date range.
- `generate_complete_parkings_report()`: generates a CSV report for each car, containing all their complete parkings in the car parking system.

## Usage

```python
#To generate a report of all the parked cars in a specific car parking machine within a date range, call the function 
generate_parked_cars_report("carparkingmachine1", "2022-01-01", "2022-02-01")

#To generate a report of the total parking fees for each car parking machine within a date range, call the function 
generate_total_fee_report("2022-01-01", "2022-02-01")

#To generate a report for each car, containing all their complete parkings in the car parking system, call the function 
generate_complete_parkings_report()

Note: These functions assume that the data is stored in JSON files, named after the corresponding car parking machine.

The generated reports will be in CSV format and will be saved in the current directory.
```

## Authors

* **[Ömer Faruk KOÇ]** - [Github](https://github.com/negativexq)

