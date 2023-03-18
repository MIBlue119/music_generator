# Music Generator

This is a simple app that uses OpenAI GPT-3 to generate ABC music
notation based on the user's natural language specification. The app
then parses the response and checks whether the generated music meets
the user's requirements. The generated music can be exported to a MIDI
file using music21 and converted to a WAV file using fluidsynth.

## Installation

`pip install -r requirements.txt`


## Usage

`python -m music_generator.app`


## Credits

It uses OpenAI GPT-3 for music generation, music21 for parsing ABC music notation, and fluidsynth for converting MIDI files to WAV files.
