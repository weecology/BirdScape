#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to query nearby hotspots from eBird API and find the most active one.
"""

import requests
import pandas as pd
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class HotspotInfo:
    """Data class to store hotspot information"""
    locId: str
    name: str
    latitude: float
    longitude: float
    numChecklists: int
    countryCode: str
    subnational1Code: str
    subnational2Code: str
    isHotspot: bool

@dataclass
class SpeciesInfo:
    """Data class to store species information"""
    speciesCode: str
    comName: str
    sciName: str
    category: str
    taxonOrder: int
    count: int

class EBirdHotspots:
    def __init__(self, api_key: str):
        """
        Initialize the EBirdHotspots class with an API key.
        
        Args:
            api_key (str): Your eBird API key
        """
        self.api_key = api_key
        self.base_url = "https://api.ebird.org/v2/ref/hotspot/geo"
        self.info_url = "https://api.ebird.org/v2/ref/hotspot/info"
        self.species_url = "https://api.ebird.org/v2/product/spplist"
        self.headers = {
            "X-eBirdApiToken": api_key
        }

    def get_nearby_hotspots(
        self,
        lat: float,
        lng: float,
        dist: int = 25,
        back: Optional[int] = None,
        fmt: str = "json"
    ) -> List[Dict]:
        """
        Get nearby hotspots from eBird API.
        
        Args:
            lat (float): Latitude to 2 decimal places
            lng (float): Longitude to 2 decimal places
            dist (int): Search radius in kilometers (0-500, default 25)
            back (int, optional): Only fetch hotspots visited in last N days (1-30)
            fmt (str): Response format ('json' or 'csv')
            
        Returns:
            List[Dict]: List of hotspot data
        """
        params = {
            "lat": lat,
            "lng": lng,
            "dist": dist,
            "fmt": fmt
        }
        
        if back is not None:
            params["back"] = back
            
        response = requests.get(
            self.base_url,
            headers=self.headers,
            params=params
        )
        
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code}")
            
        if fmt == "json":
            return response.json()
        else:
            return pd.read_csv(pd.StringIO(response.text))

    def get_hotspot_info(self, locId: str) -> HotspotInfo:
        """
        Get detailed information for a specific hotspot.
        
        Args:
            locId (str): The location code for the hotspot
            
        Returns:
            HotspotInfo: Detailed information about the hotspot
        """
        response = requests.get(
            f"{self.info_url}/{locId}",
            headers=self.headers
        )
        
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code}")
            
        data = response.json()
        return HotspotInfo(
            locId=data['locId'],
            name=data['name'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            numChecklists=data['numChecklists'],
            countryCode=data['countryCode'],
            subnational1Code=data['subnational1Code'],
            subnational2Code=data['subnational2Code'],
            isHotspot=data['isHotspot']
        )

    def get_hotspot_species(self, locId: str, back: int = 30) -> List[SpeciesInfo]:
        """
        Get species list for a specific hotspot.
        
        Args:
            locId (str): The location code for the hotspot
            back (int): Number of days to look back (1-30, default 30)
            
        Returns:
            List[SpeciesInfo]: List of species observed at the hotspot
        """
        # Get current date and date 30 days ago
        end_date = datetime.now().strftime('%Y/%m/%d')
        start_date = (datetime.now() - timedelta(days=back)).strftime('%Y/%m/%d')
        
        url = f"https://api.ebird.org/v2/data/obs/{locId}/recent"
        params = {
            "back": back,
            "fmt": "json"
        }
        
        response = requests.get(
            url,
            headers=self.headers,
            params=params
        )
        
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code}")
            
        observations = response.json()
        
        # Create a dictionary to store unique species with their counts
        species_dict = {}
        for obs in observations:
            species_code = obs['speciesCode']
            if species_code not in species_dict:
                species_dict[species_code] = SpeciesInfo(
                    speciesCode=species_code,
                    comName=obs['comName'],
                    sciName=obs['sciName'],
                    category=obs['category'],
                    taxonOrder=obs['taxonOrder'],
                    count=1
                )
            else:
                species_dict[species_code].count += 1
                
        return list(species_dict.values())

def main():
    # Example usage
    api_key = "YOUR_API_KEY"  # Replace with your actual API key
    
    # Initialize the class
    ebird = EBirdHotspots(api_key)
    
    # Example coordinates (Medellín, Colombia)
    lat = 6.2442
    lng = -75.5812
    
    try:
        # Get nearby hotspots
        hotspots = ebird.get_nearby_hotspots(lat, lng, dist=25)
        print(f"Found {len(hotspots)} hotspots near {lat}, {lng}")
        
        # Get detailed info for each hotspot
        hotspot_info_list = []
        for hotspot in hotspots:
            try:
                info = ebird.get_hotspot_info(hotspot['locId'])
                hotspot_info_list.append(info)
                print(f"Retrieved info for {info.name}")
            except Exception as e:
                print(f"Error getting info for {hotspot['locName']}: {e}")
        
        # Find hotspot with most checklists
        if hotspot_info_list:
            most_active = max(hotspot_info_list, key=lambda x: x.numChecklists)
            print("\nMost active hotspot:")
            print(f"Name: {most_active.name}")
            print(f"Location ID: {most_active.locId}")
            print(f"Coordinates: {most_active.latitude}, {most_active.longitude}")
            print(f"Number of checklists: {most_active.numChecklists}")
            print(f"Region: {most_active.subnational1Code}, {most_active.countryCode}")
            
            # Get species list for the most active hotspot
            print("\nSpecies observed in the last 30 days:")
            species_list = ebird.get_hotspot_species(most_active.locId)
            species_list.sort(key=lambda x: x.count, reverse=True)
            
            print("\nSpecies (sorted by frequency):")
            print(f"{'Common Name':<30} {'Scientific Name':<30} {'Count':<10}")
            print("-" * 72)
            for species in species_list:
                print(f"{species.comName:<30} {species.sciName:<30} {species.count:<10}")
        else:
            print("No hotspot information was retrieved.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 