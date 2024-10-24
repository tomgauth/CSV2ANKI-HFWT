import streamlit as st
import pandas as pd
import io
import genanki
import random
from services.anki_models import recall_model, recognize_model
from services.tts_service import generate_audio


# Function to create an Anki recall deck with simplified fields
def create_anki_deck(data):
    # Store the list of media files (audio)
    media_files = []

    deck_id = random.randrange(1 << 30, 1 << 31)
    my_deck = genanki.Deck(deck_id, 'Generated Flashcards')
    # st.write(f"Debug: Initialized Anki deck with ID {deck_id}")

    for index, row in data.iterrows():
        fields = [
                str(row['UserLanguage']) if 'UserLanguage' in row else '',
                str(row['TargetLanguage']) if 'TargetLanguage' in row else '',
                str(row['TargetAudio']) if 'TargetAudio' in row else '',
                str(row['TargetIPA']) if 'TargetIPA' in row else '',
                str(row['Notes']) if 'Notes' in row else '',
                str(row['card_type']) if 'card_type' in row else '',  # Add card_type field
            ]
        
        # Ensure no extra fields are added beyond the 6 required fields
        try:
            my_note = genanki.Note(
                model=model,
                fields=fields  # Pass exactly 6 fields
            )
            my_deck.add_note(my_note)
            st.write(f"Debug: Added note for row {index}")
        except Exception as e:
            st.error(f"Error adding note for row {index}: {e}")
        # st.write(f"Debug: Processing row {index} with data: {row.to_dict()}")

        # Check the flashcard type and select the appropriate model
        flashcard_type = row.get('card_type', 'Recall')  # Default to 'recall' if not specified
        if flashcard_type == 'Recognize':
            model = recognize_model()
            # st.write("Debug: Using Recognize model.")
        else:
            model = recall_model()
            # st.write("Debug: Using Recall model.")

        # Generate fields based on the selected model
        for field in ['French', 'English', 'French IPA', 'notes', 'card_type']:
            value = str(row[field]) if field in row and pd.notna(row[field]) else ''
            fields.append(value)
            # st.write(f"Debug: Added field '{field}' with value '{value}'")

        # For Recognize cards, generate audio for the front side
        if flashcard_type == 'Recognize':
            french_text = str(row['French']) if 'French' in row else ''
            if french_text:
                try:
                    audio_file = generate_audio(french_text)
                    # st.write(f"Debug: Audio generated and saved as {audio_file}")
                    fields.insert(0, f'[sound:{audio_file}]')  # Add audio to the front
                    media_files.append(audio_file)
                except Exception as e:
                    st.error(f"Error generating audio for row {index}: {e}")
            else:
                fields.insert(0, '')  # Leave empty if no French text
                # st.write(f"Debug: No French text found for row {index}. Skipping audio generation.")

        # Create the note with all fields
        try:
            my_note = genanki.Note(
                model=model,
                fields=fields
            )
            my_deck.add_note(my_note)
            # st.write(f"Debug: Added note for row {index}")
        except Exception as e:
            st.error(f"Error adding note for row {index}: {e}")

    # Create the Anki package and include media files (audio)
    try:
        my_package = genanki.Package(my_deck)
        my_package.media_files = media_files
        output_apkg = 'output_flashcards.apkg'
        my_package.write_to_file(output_apkg)
        # st.write(f"Debug: Anki package saved as {output_apkg}")
    except Exception as e:
        st.error(f"Error saving Anki package: {e}")

    return output_apkg