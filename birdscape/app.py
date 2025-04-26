import streamlit as st
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np
from pydub import AudioSegment
import os
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="BirdScape",
    page_icon="🐦",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🐦 BirdScape")
    st.markdown("""
    Welcome to BirdScape! Select a location on the map to discover bird species and create a soundscape.
    """)
    
    # Create two columns for the layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create a map centered on the world
        m = folium.Map(location=[20, 0], zoom_start=2)
        
        # Add a marker for the selected location
        if 'selected_location' in st.session_state:
            folium.Marker(
                location=st.session_state.selected_location,
                popup="Selected Location"
            ).add_to(m)
        
        # Display the map
        folium_static(m)
        
        # Add location input
        location_input = st.text_input("Enter a location (city, country):")
        if location_input:
            try:
                geolocator = Nominatim(user_agent="birdscape")
                location = geolocator.geocode(location_input)
                if location:
                    st.session_state.selected_location = [location.latitude, location.longitude]
                    st.success(f"Location found: {location.address}")
                else:
                    st.error("Location not found. Please try again.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with col2:
        st.header("Bird Species")
        # Placeholder for bird species list
        st.info("Select a location to see bird species in the area.")
        
        st.header("Soundscape Controls")
        # Placeholder for soundscape controls
        st.info("Configure your soundscape settings here.")

if __name__ == "__main__":
    main()
