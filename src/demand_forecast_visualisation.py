import folium
from folium.plugins import HeatMapWithTime
import demand_forecasting as df
import numpy as np
import os
import params

def main():
    # Assuming df.demand_forecasting() returns the provided 9x15 matrix (9 bus stops, 15 hours)
    demand_forecast = df.demand_forecasting()[0]

    # Convert to numpy array for easier manipulation
    data_np = np.array(demand_forecast)

    # Find min and max values in the array
    min_val = data_np.min()
    max_val = data_np.max()

    # Normalize the data, round to 4sf
    normalized_data = np.round((data_np - min_val) / (max_val - min_val), 4)

    # Convert back to a list if needed
    normalized_data_list = normalized_data.tolist()
    print(normalized_data_list)

    # Initialize map with a standard theme (OpenStreetMap as a fallback)
    m = folium.Map(
        location=params.NUS_COORDINATES, 
        zoom_start=15, 
        control_scale=True,
        tiles="Cartodb dark_matter"
    )

    # Coordinates for each bus stop with names (sorted by alphabetical order of bus stop name)
    bus_stops = sorted(params.BUS_STOP_COORDINATES.items(), key=lambda pair: pair[0])

    # Adjusting specific labels position
    adjusted_bus_stops = {
        "Kent Ridge MRT / Opp Kent Ridge MRT": (0, 25),  
        "UHC / Opp UHC": (0, 15),  
        "LT27 / S17": (0, 15), 
        "BIZ2 / Opp HSSML": (0, 10),  
        "LT13 / Ventus": (0, 10),  
        "UTown": (0, 15),
        "COM3": (0, 10),
        "PGP": (0, 15),
        "IT / CLB": (0, 15)
    }

    # Add bus stop names as DivIcons (simple HTML text)
    for name, coords in bus_stops:
        # Check if the bus stop has an adjusted position
        offset = adjusted_bus_stops.get(name, (0, 0))

        folium.Marker(
            location=coords,
            icon=folium.DivIcon(
                icon_size=(90, 36),  # Adjust size to fit the text
                icon_anchor=(45, 18 + offset[1]),  # Adjust position based on the offset (vertical shift)
                html=f'<div style="font-size: 7px; font-weight: bold; color: black; background: #ffffff; padding: 2px 5px; border-radius: 5px; text-align: center;">{name}</div>'
            )
        ).add_to(m)

    # Prepare data for HeatMapWithTime 
    heat_data = []
    for hour in range(15):  # 15 hours
        hour_data = []
        for stop_index, (name, coords) in enumerate(bus_stops):
            demand = normalized_data_list[stop_index][hour]  # Get demand at this stop and hour

            # Add this data point to the heat_data for visualization in each hourly interval
            hour_data.append([coords[0], coords[1], demand])

        # Append hour data to heat_data
        heat_data.append(hour_data)

    # Add HeatMapWithTime to animate demand over time
    HeatMapWithTime(
        data=heat_data, 
        radius=20, 
        auto_play=True,
        max_opacity=0.8
    ).add_to(m)

    # Add title to map
    map_title = "Demand Forecasting Timelapse"
    title_html = '<h3 style="position: absolute; left:40vw; top:1rem; z-index: 100000; font-size: 20px; color: white; font-family: Cambria, Cochin, Georgia, Times, serif;"><b>{}</b></h3>'.format(
        map_title)
    m.get_root().html.add_child(folium.Element(title_html))

    # Save the map as an HTML file
    m.save(os.path.join(os.path.dirname(__file__), f"../visualisations/timelapses/demand_heatmap.html"))
    
if __name__ == "__main__":
    main()