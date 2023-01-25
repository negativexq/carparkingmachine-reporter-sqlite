import csv
import json
import os

def generate_parked_cars_report(machine_name, from_date, to_date):
    # read the JSON file for the specified car parking machine
    with open(f"{machine_name}.json", "r") as f:
        parked_cars = json.load(f)
    # filter the list of parked cars by the specified date range
    filtered_cars = [car for car in parked_cars if from_date <= car["check_in"] <= to_date]
    # write the filtered list to a CSV file
    with open(f"parkedcars_{machine_name}_from_{from_date}_to_{to_date}.csv", "w", newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["license_plate", "checked_in", "checked_out", "parking_fee"])
        for car in filtered_cars:
            writer.writerow([car["license_plate"], car["check_in"], car["check_out"], car["parking_fee"]])

def generate_total_fee_report(from_date, to_date):
    # get the names of all car parking machine JSON files
    machine_names = [f.split(".")[0] for f in os.listdir() if f.endswith(".json")]
    # initialize a dictionary to store the total fees for each car parking machine
    total_fees = {machine_name: 0 for machine_name in machine_names}
    # read the JSON files for each car parking machine and update the total fees
    for machine_name in machine_names:
        with open(f"{machine_name}.json", "r") as f:
            parked_cars = json.load(f)
        for car in parked_cars:
            if from_date <= car["check_in"] <= to_date:
                total_fees[machine_name] += car["parking_fee"]
    # write the total fees to a CSV file
    with open(f"totalfee_from_{from_date}_to_{to_date}.csv", "w", newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["car_parking_machine", "total_parking_fee"])
        for machine_name, fee in sorted(total_fees.items(), key=lambda item: item[1], reverse=True):
            writer.writerow([machine_name, fee])

def generate_complete_parkings_report():
    # get a list of all the unique license plates in the JSON files
    license_plates = set()
    for f in os.listdir():
        if f.endswith(".json"):
            with open(f, "r") as f:
                parked_cars = json.load(f)
            for car in parked_cars:
                license_plates.add(car["license_plate"])

    # generate a report for each license plate
    for license_plate in license_plates:
        # get the names of all car parking machine JSON files
        machine_names = [f.split(".")[0] for f in os.listdir() if f.endswith(".json")]
        # initialize a list to store the complete parkings for the specified car
        complete_parkings = []
        # read the JSON files for each car parking machine and add the complete parkings to the list
        for machine_name in machine_names:
            with open(f"{machine_name}.json", "r") as f:
                parked_cars = json.load(f)
            for car in parked_cars:
                if car["license_plate"] == license_plate and "check_out" in car:
                    complete_parkings.append({
                        "car_parking_machine": machine_name,
                        "check_in": car["check_in"],
                        "check_out": car["check_out"],
                        "parking_fee": car["parking_fee"]
                    })
        # write the complete parkings to a CSV file
        with open(f"all_parkings_for_{license_plate}.csv", "w", newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(["car_parking_machine", "check_in", "check_out", "parking_fee"])
            for parking in complete_parkings:
                writer.writerow([parking["car_parking_machine"], parking["check_in"], parking["check_out"], parking["parking_fee"]])


def main():
    print("[P] Report all parked cars during a parking period for a specific parking machine")
    print("[F] Report total collected parking fee during a parking period for all parking machines")
    print("[C] Report all complete parkings over all parking machines for a specific car")
    print("[Q] Quit program")
    while True:
        choice = input().lower()
        if choice == "p":
            
            machine_name, from_date, to_date = input().split(",")
            generate_parked_cars_report(machine_name, from_date, to_date)
        elif choice == "f":
            
            from_date, to_date = input().split(",")
            generate_total_fee_report(from_date, to_date)
        elif choice == "c":
            generate_complete_parkings_report()
        elif choice == "q":
            break
        else:
            print("Invalid input")

if __name__ == "__main__":
    main()