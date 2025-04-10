import traci
import csv
import os
import traci.constants as tc

# GUI Mode (from environment variable)
#start_gui = os.environ.get("gui", "False")
start_gui = "True"

# Emergency Vehicle Settings
em_vid = "eme"
em_vehicle_start_time = 3000
end_time = 200000
detect_range = 80
lctime = 3
lcmode = 0b011001000101
road_id = "E6"

# Function to Get Vehicle Information
def get_vid_info(vid, step):
    acc = traci.vehicle.getAccel(vid)
    speed = traci.vehicle.getSpeed(vid)
    pos = traci.vehicle.getLanePosition(vid)
    lane = traci.vehicle.getLaneIndex(vid)
    edge_id = traci.vehicle.getRoadID(vid)
    return (step, vid, acc, speed, pos, lane, edge_id)

# Function to Extract Traffic Data from All Edges
def extract_traffic_data(step, writer):
    edge_ids = traci.edge.getIDList()
    
    for edge_id in edge_ids:
        formatted_edge_id = f"'{edge_id}"
        vehicle_ids = traci.edge.getLastStepVehicleIDs(edge_id)  # Get vehicle IDs
        
        vehicle_count = len(vehicle_ids)
        avg_speed = sum(traci.vehicle.getSpeed(vid) for vid in vehicle_ids) / vehicle_count if vehicle_count else 0
        occupancy = traci.edge.getLastStepOccupancy(edge_id) * 100
        traffic_flow = vehicle_count * avg_speed if avg_speed > 0 else 0

        print(f"Step {step}, Edge {edge_id}: Speed={avg_speed}, Count={vehicle_count}, Flow={traffic_flow}")
        
        writer.writerow([step, formatted_edge_id, avg_speed, vehicle_count, occupancy, traffic_flow])


# Function to Run SUMO Simulation
def main(road_id):
    # Vehicle Data File (Commented Out)
    # f = open('../data/data.csv', 'w')
    # writer = csv.writer(f)
    # writer.writerow(['step', 'vid', 'acc', 'speed', 'pos', 'lane', 'edge_id'])

    # Traffic Data File for All Edges
    edge_file = open('../data/all_edge_data.csv', 'w')
    edge_writer = csv.writer(edge_file)
    edge_writer.writerow(['step', 'edge_id', 'avg_speed', 'vehicle_count', 'occupancy', 'traffic_flow'])

    step = 0

    # Start SUMO
    sumo_exe = "sumo-gui" if start_gui == "True" else "sumo"
    traci.start([
        sumo_exe, "-c", "../cfg/emergency.city.sumo.cfg",
        "--lanechange.duration", "2",
        "--random",
        "--tls.actuated.jam-threshold", "3",
        "--device.bluelight.explicit", "true"
    ])

    if start_gui == "True":
        traci.gui.setSchema("View #0", "real world")

    while step < end_time:
        traci.simulationStep()

        # Extract Traffic Data from All Edges Every 50 Steps
        if step % 100 == 0 and step > 0:
            extract_traffic_data(step, edge_writer)

        # Commented Out: Adding Emergency Vehicle
        if step == em_vehicle_start_time:
            traci.vehicle.add(em_vid, "em_route", typeID="emergency_v", departSpeed="30", departLane="1")
            traci.vehicle.setParameter(em_vid, "emergency", "yes")
            traci.vehicle.setParameter(em_vid, "device.bluelight.reactiondist", str(90))
            traci.vehicle.setMaxSpeed(em_vid, 50)
            traci.vehicle.setSpeedMode(em_vid, 3)
            if start_gui == "True":
                traci.gui.trackVehicle("View #0", em_vid)
                traci.gui.setZoom("View #0", 3000)

        # Commented Out: Dynamic Traffic Light Control for Emergency Vehicle
        if step > em_vehicle_start_time:
            for tls in traci.trafficlight.getIDList():
                if em_vid in traci.vehicle.getIDList():
                    em_road = traci.vehicle.getRoadID(em_vid)
                    if em_road in traci.trafficlight.getControlledLinks(tls):
                        traci.trafficlight.setPhase(tls, 0)

        # Commented Out: Vehicle Evacuation Logic
        if step % 20 == 0 and step > em_vehicle_start_time:
            if em_vid in traci.vehicle.getIDList():
                em_info = get_vid_info(em_vid, step)
                road_id = traci.vehicle.getRoadID(em_vid)
                car_list = traci.edge.getLastStepVehicleIDs(road_id)

                for vid in car_list:
                    if vid == em_vid:
                        continue
                    
                    res = get_vid_info(vid, step)
                    traci.vehicle.setLaneChangeMode(vid, lcmode)
                    
                    # Evacuation Condition
                    if (0 < res[4] - em_info[4] < detect_range) and res[5] == em_info[5]:
                        lcsl = traci.vehicle.couldChangeLane(vid, 1)  # Left Lane
                        lcsr = traci.vehicle.couldChangeLane(vid, -1) # Right Lane
        
                        if lcsr:
                            traci.vehicle.changeLaneRelative(vid, -1, lctime)
                            print(f"Vehicle {vid} moved right to clear the way.")
                        elif lcsl:
                            traci.vehicle.changeLaneRelative(vid, 1, lctime)
                            print(f"Vehicle {vid} moved left to clear the way.")
                        else:
                            # Reduce Speed if No Lane Change Possible
                            traci.vehicle.slowDown(vid, 2, 5)
                            print(f"Vehicle {vid} reduced speed to avoid collision.")

        # Data Logging for Vehicles (Commented Out)
        # if step % 50 == 0:
        #     car_list = traci.edge.getLastStepVehicleIDs(road_id)
        #     if car_list:
        #         for vid in car_list:
        #             res = get_vid_info(vid, step)
        #             writer.writerow(res)

        if step % 500 == 0:
            # f.flush()  # Commented Out
            edge_file.flush()

        step += 1

    # f.close()  # Commented Out
    edge_file.close()

if __name__ == "__main__":
    main(road_id)
