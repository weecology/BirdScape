# BirdScape

BirdScape is a Streamlit application that allows users to explore bird species and create audio soundscapes based on geographic locations. Users can select a location on Earth, view a list of bird species in that area, and generate an immersive audio experience.

## Features

- Interactive map for location selection
- Bird species database integration
- Audio soundscape generation
- User-friendly interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/birdscape.git
cd birdscape
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
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
│   └── config.py       # Configuration settings
├── tests/              # Test directory
├── docs/               # Documentation
├── requirements.txt    # Project dependencies
└── setup.py           # Package setup file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
