import streamlit as st
import pandas as pd
import io
import genanki
import random
from services.anki_models import recall_model, recognize_model
from services.tts_service import generate_audio  # Import audio generation function

# Define default column mappings for preprocessing
COLUMN_MAPPINGS = {
    'French': 'TargetLanguage',
    'English': 'UserLanguage',
    'English Auto': 'UserLanguage',
    'IPA': 'TargetIPA',
    'Notes': 'Notes',
    'card_type': 'card_type'
}

# Function to preprocess the DataFrame
def preprocess_flashcards(data):
    data = data.rename(columns={col: COLUMN_MAPPINGS[col] for col in data.columns if col in COLUMN_MAPPINGS})
    
    # Add missing columns as empty strings to ensure we have all required columns
    for target_col in COLUMN_MAPPINGS.values():
        if target_col not in data.columns:
            data[target_col] = ""  # Add missing columns as empty strings

    return data

# Function to create an Anki recall deck
def create_anki_deck(data, model, deck_name):
    # Preprocess data to ensure all required columns are present
    data = preprocess_flashcards(data)
    media_files = []

    deck_id = random.randrange(1 << 30, 1 << 31)
    my_deck = genanki.Deck(deck_id, deck_name)

    for index, row in data.iterrows():
        # Generate audio for each row's 'TargetLanguage' and add it to 'TargetAudio'
        target_language_text = str(row['TargetLanguage'])
        target_audio_path = ""
        
        # Generate audio if there's text in the 'TargetLanguage' field
        if target_language_text:
            try:
                target_audio_path = generate_audio(target_language_text)
                media_files.append(target_audio_path)  # Add audio file to media files
            except Exception as e:
                st.error(f"Error generating audio for row {index}: {e}")

        # Ensure that fields contain exactly 6 items, adding empty strings if necessary
        fields = [
            str(row['UserLanguage']),
            target_language_text,
            f'[sound:{target_audio_path}]' if target_audio_path else "",  # Include audio
            str(row['TargetIPA']),
            str(row['Notes']),
            str(row['card_type'])
        ]


        # Create the note with all 6 fields
        try:
            my_note = genanki.Note(
                model=model,
                fields=fields
            )
            my_deck.add_note(my_note)
        except Exception as e:
            st.error(f"Error adding note for row {index}: {e}")

    # Create the Anki package and include media files
    try:        
        my_package = genanki.Package(my_deck)
        my_package.media_files = media_files
        output_apkg = f"{deck_name.replace(' ', '_')}.apkg"
        my_package.write_to_file(output_apkg)
    except Exception as e:
        st.error(f"Error saving Anki package: {e}")

    return output_apkg