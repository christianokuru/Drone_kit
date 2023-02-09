import dronekit
import time

vehicle = dronekit.connect("tcp:127.0.0.1:5760", wait_ready=True)

def pre_flight_check(vehicle):
    checks = [
        ("Armed", vehicle.armed),
        ("Valid GPS fix", vehicle.gps_0.fix_type >= 2),
        ("Battery level", vehicle.battery.level >= 30),
        ("Compass health", vehicle.compass.is_healthy),
    ]

    results = [check[1] for check in checks]
    
    if not all(results):
        for check in checks:
            if not check[1]:
                print(f"{check[0]} check failed.")
        return False
    
    print("Pre-flight check complete. Vehicle is ready for takeoff.")
    return True

def fly_to_coordinates(vehicle, coordinates):
    for coord in coordinates:
        vehicle.simple_goto(coord)
        
        while vehicle.mode.name=="GUIDED":
            print("Current location: Latitude = %s Longitude = %s" % (vehicle.location.global_frame.lat, vehicle.location.global_frame.lon))
            time.sleep(1)
    
    time.sleep(300)

def lift_drone(vehicle):
    print("Lifting drone 10 feet into the air...")
    vehicle.simple_takeoff(10)  # Lift the drone 10 feet into the air.
    while True:
        print("Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= 10 * 0.95:
            print("Drone has reached target altitude.")
            break
        time.sleep(1)

def land_drone(vehicle):
    print("Landing drone...")
    vehicle.mode = dronekit.VehicleMode("LAND")
    while vehicle.location.global_relative_frame.alt > 0:
        print("Altitude: ", vehicle.location.global_relative_frame.alt)
        time.sleep(1)
    print("Drone has landed successfully.")


if pre_flight_check(vehicle):
    lift_drone(vehicle)
    time.sleep(5)
    num_coords = int(input("Enter the number of coordinates to fly to: "))
    
    coordinates = []
    for i in range(num_coords):
        lat = float(input(f"Enter the latitude for coordinate {i + 1}: "))
        lon = float(input(f"Enter the longitude for coordinate {i + 1}: "))
        coordinates.append((lat, lon))
    
    fly_to_coordinates(vehicle, coordinates)
    land_drone(vehicle)
else:
    print("Aborting takeoff.")
