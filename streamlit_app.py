"""Streamlit app for music generator demo.
"""
import io
import os
from pathlib import Path

import streamlit as st
import openai
from music_generator.generator import generate_note,export_abc_notations_to_file,convert_midi_to_music 

st.title("Music Generator Demo based on OpenAI API")
st.write("This is a simple app that uses OpenAI GPT-3 to generate ABC music notation based on the user's natural language specification. The app then parses the response and checks whether the generated music meets the user's requirements. The generated music can be exported to a MIDI file using music21 and converted to a WAV file using fluidsynth.")

col1,col2=st.columns(2)
openai_key=col1.text_input("OpenAI API Key",type="password")

make_button=st.button("Make Music")
st.markdown("---")

path="tmp"
if "generation_success" not in st.session_state:
    st.session_state["generation_success"] = False
if os.path.exists(path) == False:
    os.mkdir(path)


if make_button:
    openai.api_key = openai_key
    with st.spinner(f"Generating music..."):
        
        
        music_topic = "GPT4發佈了，我們既興奮又害怕",
        architecture_components = {
            "第1~10秒":"開頭音樂聽起來是亢奮的",
            "第10~20秒":"音樂變得平靜",
            "第20~30秒":"音樂變得讓人驚奇",
            "第30~40秒":"音樂變得可愛與特別",
            "第40~50秒":"音樂變得緊張",
        },
        auto_components=False,
        max_attempts=1
        user_input= f"You ar a professional music composer. Please compose a music with this topic `{music_topic}`."
    
        music_generated = False
        successful_attempt_count = 0    
        failed_attempt_count = 0
        while successful_attempt_count < max_attempts:
            print(f"Attempt {successful_attempt_count}/{max_attempts}, Failed Attempt Count: {failed_attempt_count}")

            abc_notations = generate_note(user_input, architecture_components, auto_components=auto_components)

            if abc_notations is not None:
                print("Start to write the music to midi file")
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                midi_output_file = os.path.join(path, f"{timestamp}-success_music_attempt{successful_attempt_count}.mid")
                exported_midi_file = export_abc_notations_to_file(abc_notations, midi_output_file)

                if exported_midi_file is not None:
                    print(f"Music midi exported to {midi_output_file}")
                    # Start to use fluidsynth to convert midi file to wav file
                    stem_name = Path(midi_output_file).stem
                    wav_output_file = io.BytesIO()
                    convert_midi_to_music(exported_midi_file, wav_output_file)
                    successful_attempt_count += 1
                else:
                    print("Failed to export music, trying again...")
                    failed_attempt_count += 1
                    continue
            else:
                print("Failed to parse music, trying again...")
                failed_attempt_count += 1
                continue
        if successful_attempt_count > 0:
            music_generated = True
            st.success("Music generated successfully!")
            st.audio(wav_output_file)
            st.markdown("Download the audio by right-clicking on the media player")
            st.session_state["generation_success"]=True

if st.session_state["generation_success"]==True:
    try:
        for file in os.listdir(path):
            os.remove(os.path.join(path, file))
    except:
        pass             