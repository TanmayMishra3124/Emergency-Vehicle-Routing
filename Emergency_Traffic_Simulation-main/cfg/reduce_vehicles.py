import xml.etree.ElementTree as ET

# Load XML
tree = ET.parse('output.trips3_original.xml')
root = tree.getroot()

# Get all vehicle elements
vehicles = root.findall('vehicle')

# Calculate half the vehicles to keep
num_to_keep = len(vehicles) // 3

# Remove the rest
for vehicle in vehicles[num_to_keep:]:
    root.remove(vehicle)

# Save the updated XML
tree.write('output.trips3.xml')

print(f"Reduced vehicles by 50%. Saved as 'output.trips3.xml'")
