import streamlit as st
import pandas as pd
import io
import genanki
import random
from services.anki_models import recall_model, recognize_model
from services.tts_service import generate_audio  # Import audio generation function

COLUMN_MAPPINGS = {
    'French': 'TargetLanguage',
    'IPA': 'TargetIPA',
    'Notes': 'Notes',
    'card_type': 'card_type'
}


def preprocess_flashcards(data):
    # Check if 'English' column is present; if not, display an error in Streamlit and stop
    if 'English' not in data.columns:
        st.error("Error: The 'English' column is required as the UserLanguage. Please include this column in your data.")
        return None  # Return None to indicate processing should stop

    # Rename columns based on the mappings
    data = data.rename(columns={col: COLUMN_MAPPINGS[col] for col in data.columns if col in COLUMN_MAPPINGS})
    
    # Set UserLanguage to English column
    data['UserLanguage'] = data['English']

    # Drop unnecessary columns
    data = data.drop(columns=['English'], errors='ignore')

    # Add missing columns as empty strings to ensure we have all required columns
    for target_col in COLUMN_MAPPINGS.values():
        if target_col not in data.columns:
            data[target_col] = ""  # Add missing columns as empty strings

    return data


# Function to create an Anki recall deck with debug print statements
def create_anki_deck(selected_language, data, model, deck_name):
    # Preprocess data to ensure all required columns are present
    data = preprocess_flashcards(data)
    if data is None:
        return None  # Exit if data preprocessing failed due to missing columns

    media_files = []

    # Check the DataFrame after preprocessing
    print("Processed DataFrame (first few rows):")
    print(data.head())

    # Initialize the Anki deck
    deck_id = random.randrange(1 << 30, 1 << 31)
    my_deck = genanki.Deck(deck_id, deck_name)
    print(f"Initialized Anki deck with ID: {deck_id} and name: {deck_name}")

    # Iterate over each row in the DataFrame to create flashcards
    for index, row in data.iterrows():
        # Check contents of essential columns
        target_language_text = str(row['TargetLanguage'])
        user_language_text = str(row['UserLanguage'])
        print(f"Row {index} - UserLanguage: '{user_language_text}', TargetLanguage: '{target_language_text}'")

        # Placeholder for audio generation; replace with actual function if needed
        target_audio_path = ""
        if target_language_text:
            try:
                target_audio_path = generate_audio(selected_language, target_language_text)  # Simulated audio path for testing
                media_files.append(target_audio_path)
                print(f"Audio path '{target_audio_path}' added to media_files")
            except Exception as e:
                st.error(f"Error generating audio for row {index}: {e}")
                print(f"Error generating audio for row {index}: {e}")

        # Set up fields array with exactly 6 elements as expected by the model
        fields = [
            user_language_text,
            target_language_text,
            f'[sound:{target_audio_path}]' if target_audio_path else "",  # Include audio if generated
            str(row.get('TargetIPA', "")),
            str(row.get('Notes', "")),
            str(row.get('card_type', ""))
        ]

        # Print out the fields to verify the final content being added to Anki
        print(f"Fields for row {index}: {fields}")

        # Create the Anki note with the fields, ensuring that it fits the model's expectations
        try:
            my_note = genanki.Note(
                model=model,
                fields=fields
            )
            my_deck.add_note(my_note)
            print(f"Note added successfully for row {index}")
        except Exception as e:
            st.error(f"Error adding note for row {index}: {e}")
            print(f"Error adding note for row {index}: {e}")

    # Create and save the Anki package with media files
    try:
        my_package = genanki.Package(my_deck)
        my_package.media_files = media_files
        output_apkg = f"{deck_name.replace(' ', '_')}.apkg"
        my_package.write_to_file(output_apkg)
        print(f"Anki package saved as: {output_apkg}")
    except Exception as e:
        st.error(f"Error saving Anki package: {e}")
        print(f"Error saving Anki package: {e}")

    return output_apkg
