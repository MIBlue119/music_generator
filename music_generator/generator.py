"""Defines the model generator related functions.
"""
from pathlib import Path
from music_generator.utils import  (
                    parse_text_response,
                    get_model_selection,
                    format_prompt,
                    generate_openai_completion,
                    parse_abc_notations)

from music_generator.config import AppConfig

def generate_note(prompt, duration_details=None, auto_components=False):
    components_text = ""
    
    if auto_components:
        components_text = "Use appropriate design automatically."
    elif duration_details is not None:
        components_text = "Include following duration designs:"
        for duration, config in duration_details.items():
            if len(config) > 0:
                components_text += f"{duration} with {config} design.\n"
            else:
                components_text += f"{duration}\n"

    full_prompt = f"{prompt}\n\n. {components_text}.\n Please export the music design with ABC notation.Your notation response must start with code block '```abc' and ended with '```' ."
    
    formated_prompt = format_prompt(full_prompt, text_engine=AppConfig.TEXT_ENGINE)
    api_settings ={
        **get_model_selection(AppConfig.TEXT_ENGINE),
        **formated_prompt,
        "n": 1, 
        "max_tokens" :AppConfig.TEXT_ENGINE_MAX_TOKENS,               
        "temperature":AppConfig.TEXT_ENGINE_TEMPERATURE,
        "presence_penalty" : 2
    }
    response = generate_openai_completion(text_engine=AppConfig.TEXT_ENGINE, api_settings=api_settings)
    parsed_response =  parse_text_response(response, text_engine=AppConfig.TEXT_ENGINE)
    parsed_response = parse_abc_notations(parsed_response)

    return parsed_response

def export_abc_notations_to_file(abc_notations, output_file):
    if abc_notations is None:
        return None
    try:
        import music21
        score = music21.stream.Score()
        tune = music21.converter.parse(abc_notations)
        score.insert(0, tune)
        score.write('midi', fp=output_file)
        return output_file
    except Exception as e:
        print(e)
        return None

def convert_midi_to_music(midi_file, exported_audio_path):
    """Use fluidsynth to convert midi file to wav file
    """
    import pretty_midi
    import numpy as np
    from scipy.io import wavfile
    # Ref: https://github.com/andfanilo/streamlit-midi-to-wav/blob/main/app.py#LL64
    midi_data = pretty_midi.PrettyMIDI(midi_file)
    audio_data = midi_data.fluidsynth(fs=44100)
    audio_data = np.int16(
        audio_data / np.max(np.abs(audio_data)) * 32767 * 0.9
    )  # -- Normalize for 16 bit audio https://github.com/jkanner/streamlit-audio/blob/main/helper.py
    wavfile.write(exported_audio_path, 44100, audio_data)


def generate_music(music_topic, architecture_components, auto_components=False, max_attempts=5):
    """Generate music with given topic and architecture components

    Args:
        music_topic (str): The topic of the music
        architecture_components (dict): The architecture components of the music
        auto_components (bool, optional): Whether to use auto components. Defaults to False.
        max_attempts (int, optional): The max attempts to generate music. Defaults to 5.
    """
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
            midi_output_file = f"{timestamp}-success_music_attempt{successful_attempt_count}.mid"
            exported_midi_file = export_abc_notations_to_file(abc_notations, midi_output_file)

            if exported_midi_file is not None:
                print(f"Music midi exported to {midi_output_file}")
                # Start to use fluidsynth to convert midi file to wav file
                stem_name = Path(midi_output_file).stem
                wav_output_file = f"{stem_name}.wav"
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
            

