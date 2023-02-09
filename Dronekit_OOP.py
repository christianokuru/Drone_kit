import dronekit
import time

class Drone:
    def __init__(self):
        self.vehicle = dronekit.connect("tcp:127.0.0.1:5760", wait_ready=True)
    
    def pre_flight_check(self):
        checks = [
            ("Armed", self.vehicle.armed),
            ("Valid GPS fix", self.vehicle.gps_0.fix_type >= 2),
            ("Battery level", self.vehicle.battery.level >= 30),
            ("Compass health", self.vehicle.compass.is_healthy),
        ]

        results = [check[1] for check in checks]

        if not all(results):
            for check in checks:
                if not check[1]:
                    print(f"{check[0]} check failed.")
            return False

        print("Pre-flight check complete. Vehicle is ready for takeoff.")
        return True
    
    def fly_to_coordinates(self, coordinates):
        for coord in coordinates:
            self.vehicle.simple_goto(coord)
            while self.vehicle.mode.name=="GUIDED":
                print("Current location: Latitude = %s Longitude = %s" % (self.vehicle.location.global_frame.lat, self.vehicle.location.global_frame.lon))
                time.sleep(1)
        time.sleep(300)
    
    def lift_drone(self):
        print("Lifting drone 10 feet into the air...")
        self.vehicle.simple_takeoff(10)
        while True:
            print("Altitude: ", self.vehicle.location.global_relative_frame.alt)
            if self.vehicle.location.global_relative_frame.alt >= 10 * 0.95:
                print("Drone has reached target altitude.")
                break
            time.sleep(1)
    
    def land_drone(self):
        print("Landing drone...")
        self.vehicle.mode = dronekit.VehicleMode("LAND")
        while self.vehicle.location.global_relative_frame.alt > 0:
            print("Altitude: ", self.vehicle.location.global_relative_frame.alt)
            time.sleep(1)
        print("Drone has landed successfully.")


drone = Drone()

if drone.pre_flight_check():
    drone.lift_drone()
    time.sleep(5)
    num_coords = int(input("Enter the number of coordinates to fly to: "))
    coordinates = []
    for i in range(num_coords):
        lat = float(input(f"Enter the latitude for coordinate {i + 1}: "))
        lon = float(input(f"Enter the longitude for coordinate {i + 1}: "))
        coordinates.append((lat, lon))
    drone.fly_to_coordinates(coordinates)
    drone.land_drone()
else:
    print("Aborting takeoff.")
