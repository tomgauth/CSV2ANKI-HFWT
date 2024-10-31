import streamlit as st
import pandas as pd
from services.anki_deck_creator import create_anki_deck
from services.anki_models import recall_model, recognize_model
from services.delete_files import delete_audio_files_apkg_files
import io

# Streamlit app
st.title("Simple Flashcard Generator (with Model Selection)")

# Button to delete all audio files
if st.button("Delete all audio files and deck generated"):
    delete_audio_files_apkg_files()
    st.success("All audio files deleted.")

# Input field to name the Anki deck
deck_name = st.text_input("Enter the name for your Anki deck", value="Generated Flashcards")

# Model selection: Toggle button to choose "Recall" or "Recognize"
flashcard_type = st.radio("Select flashcard type", ("Recall", "Recognize"))

# Set the model based on the selected type
if flashcard_type == "Recall":
    model = recall_model()
else:
    model = recognize_model()

# Input text field for pasting TSV (tab-separated) content
input_text = st.text_area("Paste your table data here (tab-separated)")

# Generate flashcards when the "Generate Flashcards" button is clicked
if st.button("Generate Flashcards"):
    if input_text:
        try:
            # Convert the input text (tab-separated) to a DataFrame
            data = pd.read_csv(io.StringIO(input_text), sep='\t')
            st.write("Initial data preview:")
            st.dataframe(data)

            # Generate the Anki deck using the selected model and deck name
            anki_file = create_anki_deck(data, model, deck_name)
            st.success(f"Anki Deck '{deck_name}' generated successfully.")
            b
            # Provide a download link for the generated Anki deck
            with open(anki_file, 'rb') as f:
                st.download_button(f"Download {deck_name}", f, file_name=anki_file)

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please input some text to generate flashcards.")