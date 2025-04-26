import os
from pathlib import Path
import requests
from typing import List, Tuple, Optional, Union
import logging
import numpy as np
from datetime import datetime, timedelta
from NatureLM.models import NatureLM
from NatureLM.infer import Pipeline
from .ebird_hotspots import EBirdHotspots, HotspotInfo, SpeciesInfo
from .config import (
    EBIRD_API_KEY,
    EBIRD_HOTSPOT_RADIUS,
    EBIRD_LOOKBACK_DAYS,
    EBIRD_MAX_HOTSPOTS
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize eBird client
try:
    ebird_client = EBirdHotspots(EBIRD_API_KEY)
except Exception as e:
    logger.error(f"Failed to initialize eBird client: {str(e)}")
    ebird_client = None

class NatureLMManager:
    """Manager class for NatureLM model and pipeline operations."""
    
    def __init__(self, model_path: str = "EarthSpeciesProject/NatureLM-audio", device: str = "cuda"):
        """
        Initialize the NatureLM manager.
        
        Args:
            model_path (str): Path to the model on HuggingFace
            device (str): Device to run the model on ('cuda' or 'cpu')
        """
        self.model_path = model_path
        self.device = device
        self.model = None
        self.pipeline = None
        self._initialize_model()
    
    def _initialize_model(self) -> None:
        """Initialize the NatureLM model and pipeline."""
        try:
            self.model = NatureLM.from_pretrained(self.model_path)
            self.model = self.model.eval().to(self.device)
            self.pipeline = Pipeline(model=self.model)
            logger.info("NatureLM model initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize NatureLM model: {str(e)}")
            raise RuntimeError(f"Failed to initialize NatureLM model: {str(e)}")
    
    def process_audio(
        self,
        audio_paths: Union[str, List[str], np.ndarray, List[np.ndarray]],
        queries: Union[str, List[str]],
        window_length_seconds: float = 10.0,
        hop_length_seconds: float = 10.0
    ) -> List[str]:
        """
        Process audio files using the NatureLM pipeline.
        
        Args:
            audio_paths: Path(s) to audio file(s) or numpy array(s)
            queries: Query or list of queries for the model
            window_length_seconds: Length of audio window in seconds
            hop_length_seconds: Hop length between windows in seconds
            
        Returns:
            List[str]: List of model responses
        """
        if not self.pipeline:
            raise RuntimeError("NatureLM pipeline not initialized")
        
        try:
            results = self.pipeline(
                audio_paths,
                queries,
                window_length_seconds=window_length_seconds,
                hop_length_seconds=hop_length_seconds
            )
            return results
        except Exception as e:
            logger.error(f"Failed to process audio: {str(e)}")
            raise RuntimeError(f"Failed to process audio: {str(e)}")
    
    def generate_bird_sound(
        self,
        species_name: str,
        duration_seconds: float = 10.0,
        output_path: Optional[str] = None
    ) -> Optional[str]:
        """
        Generate a bird sound for a given species.
        
        Args:
            species_name: Name of the bird species
            duration_seconds: Duration of the generated sound in seconds
            output_path: Optional path to save the generated audio
            
        Returns:
            Optional[str]: Path to the generated audio file if successful
        """
        if not self.pipeline:
            raise RuntimeError("NatureLM pipeline not initialized")
        
        try:
            query = f"Generate a {species_name} bird call"
            results = self.pipeline(
                [species_name],
                [query],
                window_length_seconds=duration_seconds,
                hop_length_seconds=duration_seconds
            )
            
            if results and output_path:
                output_path = Path(output_path)
                output_path.parent.mkdir(exist_ok=True)
                # TODO: Save the generated audio to output_path
                return str(output_path)
            
            return results[0] if results else None
            
        except Exception as e:
            logger.error(f"Failed to generate sound for {species_name}: {str(e)}")
            return None

# Initialize global NatureLM manager
try:
    naturelm_manager = NatureLMManager()
except Exception as e:
    logger.error(f"Failed to initialize global NatureLM manager: {str(e)}")
    naturelm_manager = None

def get_bird_species(latitude: float, longitude: float) -> List[dict]:
    """
    Get bird species for a given location using eBird API.
    
    Args:
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
        
    Returns:
        List[dict]: List of bird species with their information
    """
    if not ebird_client:
        raise RuntimeError("eBird client not initialized")
    
    try:
        # Get nearby hotspots
        hotspots = ebird_client.get_nearby_hotspots(
            lat=latitude,
            lng=longitude,
            dist=EBIRD_HOTSPOT_RADIUS,
            back=EBIRD_LOOKBACK_DAYS
        )
        
        if not hotspots:
            logger.warning(f"No hotspots found near {latitude}, {longitude}")
            return []
        
        # Get species list for the most active hotspot
        most_active = max(hotspots, key=lambda x: x.numChecklists)
        species_list = ebird_client.get_hotspot_species(
            most_active.locId,
            back=EBIRD_LOOKBACK_DAYS
        )
        
        # Convert to list of dictionaries
        return [
            {
                "name": species.comName,
                "scientific_name": species.sciName,
                "count": species.count
            }
            for species in species_list
        ]
        
    except Exception as e:
        logger.error(f"Failed to get bird species: {str(e)}")
        return []

def create_soundscape(bird_species: List[dict], duration: int = 60) -> str:
    """
    Create a soundscape from bird species using NatureLM-audio.
    
    Args:
        bird_species (List[dict]): List of bird species
        duration (int): Duration of the soundscape in seconds
        
    Returns:
        str: Path to the generated audio file
    """
    if not naturelm_manager:
        raise RuntimeError("NatureLM manager not initialized")
    
    # Generate bird sounds for each species
    sound_files = []
    for species in bird_species:
        try:
            sound_path = naturelm_manager.generate_bird_sound(
                species['name'],
                duration_seconds=duration,
                output_path=f"output/{species['name'].replace(' ', '_')}.mp3"
            )
            if sound_path:
                sound_files.append(sound_path)
        except Exception as e:
            logger.error(f"Failed to generate sound for {species['name']}: {str(e)}")
    
    # Combine sounds into a soundscape
    output_path = Path("output") / "soundscape.mp3"
    output_path.parent.mkdir(exist_ok=True)
    
    # TODO: Implement sound mixing logic
    return str(output_path)

def validate_location(latitude: float, longitude: float) -> bool:
    """
    Validate if the given coordinates are within reasonable bounds.
    
    Args:
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
        
    Returns:
        bool: True if coordinates are valid, False otherwise
    """
    return -90 <= latitude <= 90 and -180 <= longitude <= 180

def download_bird_sound(species_name: str) -> Optional[str]:
    """
    Download bird sound for a given species using NatureLM-audio.
    
    Args:
        species_name (str): Name of the bird species
        
    Returns:
        Optional[str]: Path to the downloaded audio file if successful, None otherwise
    """
    if not naturelm_manager:
        raise RuntimeError("NatureLM manager not initialized")
    
    return naturelm_manager.generate_bird_sound(
        species_name,
        duration_seconds=10.0,
        output_path=f"output/{species_name.replace(' ', '_')}.mp3"
    )
