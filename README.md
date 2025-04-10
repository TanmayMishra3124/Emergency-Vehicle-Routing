# emergency-vehicle-routing

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

