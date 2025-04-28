# BirdScape

BirdScape is a Streamlit application that allows users to explore bird species and create audio soundscapes based on geographic locations. Users can select a location on Earth, view a list of bird species in that area, and generate an immersive audio experience.

## Features

- Interactive map for location selection
- eBird API integration for real-time bird species data
- Audio soundscape generation using NatureLM-audio
- User-friendly interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Weecology/BirdScape/birdscape.git
cd birdscape
```

2. Install uv (if not already installed):
```bash
pip install uv
```

3. Create a virtual environment and install dependencies using uv:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

4. Set up your eBird API key:
   - Create an account at https://ebird.org/
   - Request an API key at https://ebird.org/api/keygen
   - Create a `.env` file in the project root and add your API key:
     ```
     EBIRD_API_KEY=your_api_key_here
     ```

## Usage

To run the application:

```bash
streamlit run birdscape/app.py
```

## Project Structure

```
birdscape/
├── birdscape/           # Main package directory
│   ├── __init__.py     # Package initialization
│   ├── __main__.py     # Main entry point
│   ├── app.py          # Streamlit application
│   ├── utils.py        # Utility functions
│   ├── config.py       # Configuration settings
│   └── ebird_hotspots.py # eBird API integration
├── tests/              # Test directory
├── docs/               # Documentation
├── requirements.txt    # Project dependencies
└── setup.py           # Package setup file
```

## Dependencies

This project uses several key dependencies:

- **NatureLM-audio**: A multimodal audio-language foundation model for bioacoustics, used for bird sound generation and analysis. [GitHub Repository](https://github.com/earthspecies/NatureLM-audio)
- **eBird API**: For accessing real-time bird observation data and species lists
- **Streamlit**: For building the web interface
- **Folium**: For interactive map visualization
- **uv**: Fast Python package installer and resolver

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
