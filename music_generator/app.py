"""Main file for the music generator application.

A music generator app

1. According to user's natural language specification to call the open ai gpt3 to generate ABC music notation
2. The app would parse the response and check whether the generated music is fulfill user's needed
3. Use music21 to parse the ABC music notation and export to midi file
4. Use fluidsynth to convert midi file to wav file
"""
from music_generator.generator import generate_music

def main():
    music_topic = "GPT4發佈了，我們既興奮又害怕"
    max_attempts = 5
    architecture_components = {
        "第1~10秒":"開頭音樂聽起來是亢奮的",
        "第10~20秒":"音樂變得平靜",
        "第20~30秒":"音樂變得讓人驚奇",
        "第30~40秒":"音樂變得可愛與特別",
        "第40~50秒":"音樂變得緊張",
    }
    generate_music(
        music_topic = music_topic, 
        architecture_components = architecture_components, 
        auto_components=False, 
        max_attempts=max_attempts
    )
    

if __name__ == '__main__':
    main()
