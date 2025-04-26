import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

# Create necessary directories
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# API Configuration
BIRD_API_KEY = os.getenv("BIRD_API_KEY", "")
BIRD_API_URL = os.getenv("BIRD_API_URL", "https://api.example.com/birds")

# Application Settings
DEFAULT_SOUNDSCAPE_DURATION = 60  # seconds
MAX_SOUNDSCAPE_DURATION = 300  # seconds
DEFAULT_MAP_ZOOM = 2
DEFAULT_MAP_CENTER = [20, 0]  # latitude, longitude

# Audio Settings
AUDIO_FORMAT = "mp3"
SAMPLE_RATE = 44100
CHANNELS = 2  # stereo

# Cache Settings
CACHE_DIR = DATA_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)
CACHE_EXPIRY = 3600  # 1 hour in seconds
