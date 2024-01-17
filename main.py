import streamlit as st
import pandas as pd
from haversine import haversine

# Load city data
CITY_LIST = pd.read_excel("data/worldcities.xlsx")

# Extract relevant columns
city_data = CITY_LIST[['city', 'city_ascii', 'lat', 'lng']].to_dict('records')

# Helper functions
def get_location_coords(city_name):
    for city in city_data:
        if city['city'] == city_name:
            return (city['lat'], city['lng'])

def calculate_carbon(distance):
    """A plane emmits approx. 102 g of CO2 per km"""
    return (distance * 102) / 1000

def calculate_killings(carbon):

    # animals and the amount of carbonin kgs needed to kill them
    animals = {
        "leopard": 50,
        "lion": 75,
        "buffalo": 100,
        "rhino": 200,
        "elephant": 250,
    }

    killings = {animal: 0 for animal in animals}

    sorted_animals = {k: v for k, v in sorted(animals.items(), key=lambda x: x[1], reverse=True)} # Sort animals by carbon footprint

    for animal, animal_carbon in sorted_animals.items():
        while carbon >= animal_carbon:
            killings[animal] += 1
            # print(animal)  # Uncomment this line for debugging
            carbon -= animal_carbon

    return killings

# Streamlit app
def main():
    st.set_page_config(page_title="Carbon Calc - Carbon Footprint Calculator", page_icon="🌍")

    st.title("Carbon Footprint Calculator")

    st.markdown("### Calculate the amount of carbon you emit when traveling by plane and the number of big 5 animals you kill in the process")

    st.markdown("&#8592; Input your departure and destination city and click calculate to get started")

    # Sidebar for user input
    st.sidebar.markdown("# Input Trip Details")

    dep_city = st.sidebar.selectbox("Departure City", [city['city'] for city in city_data])
    des_city = st.sidebar.selectbox("Destination City", [city['city'] for city in city_data])

    if st.sidebar.button("Calculate"):
        # Perform calculations
        loc1 = get_location_coords(des_city)
        loc2 = get_location_coords(dep_city)

        distance = haversine(loc1, loc2)
        carbon = calculate_carbon(distance)
        killings = calculate_killings(carbon)

        # Display results
        st.header("Results")
        st.subheader(f"Traveling from {dep_city} to {des_city}, you will travel a total of {distance:.2f} kms and emit {carbon:.2f} kilograms of carbon")

        st.subheader("You will Kill:")
        # line
        st.markdown("---")
        st.write(f"{killings['leopard']} Leopards")
        st.write(f"{killings['lion']} Lions")
        st.write(f"{killings['buffalo']} Buffalos")
        st.write(f"{killings['rhino']} Rhinos")
        st.write(f"{killings['elephant']} Elephants")

        st.sidebar.success("Calculations completed!")

if __name__ == "__main__":
    main()
