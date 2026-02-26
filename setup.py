"""
Setup script for Jarvis Brain
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jarvis-brain",
    version="0.1.0",
    author="Jarvis Development Team",
    description="Intelligent home automation and multi-device orchestration system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/jarvis-brain",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "SpeechRecognition>=3.10.0",
        "pyttsx3>=2.90",
        "nltk>=3.8.1",
        "requests>=2.31.0",
        "aiohttp>=3.9.1",
        "pydantic>=2.5.0",
        "PyYAML>=6.0.1",
        "python-dotenv>=1.0.0",
        "Flask>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "jarvis=core.main:main",
        ],
    },
)
