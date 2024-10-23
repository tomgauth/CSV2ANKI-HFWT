import streamlit as st
import pandas as pd
import io
import genanki
import random
from services.tts_service import generate_audio


# Function to create an Anki recall deck with simplified fields
def create_anki_deck(data, model):
    # Define the expected fields based on your table
    expected_fields = ['English', 'French', 'French Audio', 'French IPA', 'notes']
    
    deck_id = random.randrange(1 << 30, 1 << 31)
    my_deck = genanki.Deck(deck_id, 'Generated Flashcards')
    st.write(f"Debug: Initialized Anki deck with ID {deck_id}")

    # Store the list of media files (audio)
    media_files = []

    # Iterate over each row and generate flashcards
    for index, row in data.iterrows():
        fields = []
        st.write(f"Debug: Processing row {index} with data: {row.to_dict()}")

        # Add fields to the flashcard based on the table structure
        for field in expected_fields:
            # Replace NaN values with empty strings
            value = str(row[field]) if field in row and pd.notna(row[field]) else ''
            
            if field == 'French':  # Target language text (French text)
                target_language_text = value
                fields.append(target_language_text)  # Add French text to TargetLanguage field
                st.write(f"Debug: Added French text '{target_language_text}'")

            elif field == 'French Audio':  # Target language audio (French audio)
                target_language_text = str(row['French']) if 'French' in row else ''
                if target_language_text:
                    st.write(f"Debug: Generating audio for French '{target_language_text}'...")

                    # Generate the audio using the correct tts_service function call
                    try:
                        audio_file = generate_audio(target_language_text)
                        st.write(f"Debug: Audio generated and saved as {audio_file}")
                        fields.append(f'[sound:{audio_file}]')  # Add the Anki audio tag
                        media_files.append(audio_file)  # Store the file to be added to the package
                    except Exception as e:
                        st.error(f"Error generating audio for row {index}: {e}")
                else:
                    fields.append('')  # Leave empty if there's no French text
                    st.write(f"Debug: No French text found for row {index}. Skipping audio generation.")

            else:
                fields.append(value)
                st.write(f"Debug: Added field '{field}' with value '{value}'")

        # Create the note with all expected fields
        try:
            my_note = genanki.Note(
                model=model,
                fields=fields
            )
            my_deck.add_note(my_note)
            st.write(f"Debug: Added note for row {index}")
        except Exception as e:
            st.error(f"Error adding note for row {index}: {e}")

    # Create the Anki package and include media files (audio)
    try:
        my_package = genanki.Package(my_deck)
        my_package.media_files = media_files
        output_apkg = 'output_recall.apkg'
        my_package.write_to_file(output_apkg)
        st.write(f"Debug: Anki package saved as {output_apkg}")
    except Exception as e:
        st.error(f"Error saving Anki package: {e}")

    return output_apkg