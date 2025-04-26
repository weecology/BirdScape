from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="birdscape",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Streamlit application for creating bird soundscapes based on geographic locations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/birdscape",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "birdscape=birdscape.__main__:main",
        ],
    },
)
