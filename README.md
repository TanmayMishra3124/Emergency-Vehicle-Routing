# 🚨 Emergency Vehicle Routing

A smart traffic-aware emergency vehicle routing system that predicts the best path from a source to a destination using simulated traffic data. The goal is to reduce emergency response time by selecting the most efficient route based on real-time traffic conditions in a SUMO simulation environment.

---

## 📌 Project Overview

This project simulates how an emergency vehicle (like an ambulance or fire truck) can be guided through a city with heavy traffic by:
- Predicting traffic conditions on each road segment
- Estimating travel times
- Finding the most time-efficient route from a starting point to the destination

It uses real-time traffic simulation with SUMO, traffic prediction models, and a routing algorithm that selects the best path using predicted travel times.

---

## 🛠️ Features

- 🔁 Predicts traffic flow using historical traffic data
- 📍 Calculates the shortest-time path for an emergency vehicle
- 📊 Outputs total travel time and distance for the chosen path
- 🧠 Modular logic to easily plug in other models (like Dijkstra, RL, or deep learning)

---

## 🧪 How It Works

1. **Traffic Simulation** is run using SUMO with a realistic traffic scenario.
2. **Traffic Data Extraction** collects vehicle counts, speeds, and occupancy per edge.
3. **LSTM Models** predict future traffic flow on each road.
4. **Travel Time Estimation** uses predicted flow to calculate time per edge.
5. **Routing Algorithm** finds the best route using estimated times.
6. **Final Evaluation** prints best path, total time, and distance.

---

## 📦 Requirements

- pandas==1.5.3  
- numpy==1.24.2  
- matplotlib==3.7.1  
- networkx==3.1  
- scikit-learn==1.2.2  
- tensorflow==2.12.0  
- keras==2.12.0  
- traci==1.18.0



---

## 📈 Sample Output

✅ Q-Learning training complete.
🚓 Best route: J1 -> J2 -> J18 -> J3
🛣️ Edges taken: E0 -> E8 -> E9
📏 Total Distance: 2.84 km
⏱ Total Estimated Time: 12.7 seconds
