import streamlit as st
import folium  # For embedding Google Maps

# Define property data globally (replace with real data)
property_data = [
    {"name": "Property 1", "location": [45.5017, -73.5673], "price": 500000, "bedrooms": 3, "property_type": "House"},
    {"name": "Property 2", "location": [45.5091, -73.5521], "price": 750000, "bedrooms": 4, "property_type": "Condo"},
    {"name": "Property 3", "location": [45.4987, -73.5801], "price": 600000, "bedrooms": 3, "property_type": "Apartment"},
    {"name": "Property 4", "location": [45.5200, -73.6000], "price": 550000, "bedrooms": 2, "property_type": "House"},
    {"name": "Property 5", "location": [45.5050, -73.5900], "price": 800000, "bedrooms": 5, "property_type": "Condo"},
    {"name": "Property 6", "location": [45.5120, -73.5580], "price": 650000, "bedrooms": 4, "property_type": "House"},
    {"name": "Property 7", "location": [45.5017, -73.5673], "price": 500000, "bedrooms": 3, "property_type": "House"},
    {"name": "Property 8", "location": [45.5091, -73.5521], "price": 750000, "bedrooms": 4, "property_type": "Condo"},
    {"name": "Property 9", "location": [45.4987, -73.5801], "price": 600000, "bedrooms": 3, "property_type": "Apartment"},
    {"name": "Property 10", "location": [45.5200, -73.6000], "price": 550000, "bedrooms": 2, "property_type": "House"},
    {"name": "Property 11", "location": [45.5050, -73.5900], "price": 800000, "bedrooms": 5, "property_type": "Condo"},
    {"name": "Property 12", "location": [45.5120, -73.5580], "price": 650000, "bedrooms": 4, "property_type": "House"},
]

# Initialize filtered_properties at the beginning of the script
filtered_properties = []

# Function to filter properties based on selected criteria
def filter_properties():
    filtered_properties = []
    for property in property_data:
        # Apply filters
        if location.lower() in property["name"].lower() and \
           price_range[0] <= property["price"] <= price_range[1] and \
           property_type in property.get("property_type", "") and \
           bedrooms == property.get("bedrooms", 0):
            filtered_properties.append(property)
    return filtered_properties

# Function to sort and filter properties
def sort_and_filter_properties(properties, sort_option):
    if sort_option == "Price (Low to High)":
        properties.sort(key=lambda x: x["price"])
    elif sort_option == "Price (High to Low)":
        properties.sort(key=lambda x: x["price"], reverse=True)
    elif sort_option == "Newest":
        properties.sort(key=lambda x: x["name"])
    return properties

# Function to display properties on Google Maps with custom icons
def display_properties_on_map(properties):
    # Create a map centered on Montreal
    m = folium.Map(location=[45.5017, -73.5673], zoom_start=12)  # Montreal's coordinates

    # Define custom icon for the house marker
    house_icon = folium.CustomIcon(icon_image="house-icon.png", icon_size=(30, 30))

    for property in properties:
        folium.Marker(
            location=property["location"],
            tooltip=property["name"],
            icon=house_icon,  # Use the custom house icon
        ).add_to(m)

    return m

# Feature 1: Property Search and Filter (Extended)
st.sidebar.header("Potential UI/UX Improvement #2: Sidebar")
st.sidebar.header("Property Search")
location = st.sidebar.text_input("Location")
price_range = st.sidebar.slider("Price Range ($)", 0, 2000000, (0, 2000000))
property_type = st.sidebar.selectbox("Property Type", ["House", "Apartment", "Condo"])
bedrooms = st.sidebar.selectbox("Bedrooms", [1, 2, 3, 4, 5])

# Feature 2: Interactive Maps using Google Maps
st.header("Upcoming Sprint 4: Potential Nice-to-Have Features")
st.write("Exploring potential nice-to-have features")
st.header("Property Listings on Map")

# Display the map with property markers (updated to show filtered properties)
st.markdown("### Potential UI/UX Improvement #1 Property Locations")
st.write("Click on the markers to view property details.")
st.components.v1.html(display_properties_on_map(filtered_properties)._repr_html_(), height=500)

# Handle marker clicks
selected_property = st.empty()  # Placeholder for property details

# Function to display property details when a marker is clicked
def display_property_details(property):
    st.sidebar.write(f"Selected Property: {property['name']}")
    st.sidebar.write(f"Location: {property['location']}")
    st.sidebar.write(f"Price: ${property['price']}")
    st.sidebar.write(f"Bedrooms: {property['bedrooms']}")
    # Add more property details as needed

if st.button("Show Property Details"):
    selected_marker = st.selectbox("Select a property to view details", [property["name"] for property in filtered_properties])
    for property in filtered_properties:
        if selected_marker == property["name"]:
            selected_property.title("Property Details")
            display_property_details(property)

# Feature 3: Sort and Filter Results (Enhanced UX)
st.sidebar.header("Sort and Filter")
sort_by = st.sidebar.selectbox("Sort By", ["Price (Low to High)", "Price (High to Low)", "Newest"])

# Apply sorting and filtering
filtered_properties = filter_properties()
sorted_properties = sort_and_filter_properties(filtered_properties, sort_by)

# Display sorted and filtered property listings
st.header("Sorted and Filtered Property Listings")
if sorted_properties:
    for property in sorted_properties:
        st.write(f"Name: {property['name']}")
        st.write(f"Location: {property['location']}")
        st.write(f"Price: ${property['price']}")
        st.write(f"Bedrooms: {property['bedrooms']}")
        st.text("-------------------------------")
else:
    st.warning("No properties found matching the selected criteria.")

# Feature 4: Clear Filters (Enhanced UX)
st.sidebar.header("Potential UI/UX Improvement #3: Button to Clear Selection")
reset_filters_button = st.sidebar.button("Clear Filters")
if reset_filters_button:
    location = ""
    price_range = (0, 2000000)
    property_type = ""
    bedrooms = ""

    # Clear the selected property details
    selected_property.empty()

    # Reset the map and property listings
    filtered_properties = filter_properties()
    sorted_properties = sort_and_filter_properties(filtered_properties, sort_by)

# Feature 5: Export Filtered Data (Nice-to-Have)
st.sidebar.header("Potential UI/UX Improvement #4: Export Results to File")
if st.sidebar.button("Export Filtered Data"):
    # Assuming you want to export the filtered data to a CSV file
    export_filename = "filtered_property_data.csv"
    export_data = sorted_properties if sorted_properties else filtered_properties
    export_to_csv(export_filename, export_data)
    st.sidebar.success(f"Filtered data exported to {export_filename}")

# Function to export data to CSV
def export_to_csv(filename, data):
    import csv

    with open(filename, mode='w', newline='') as csv_file:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)