# main.py
import streamlit as st
import pandas as pd
from services.anki_deck_creator import create_anki_deck
from services.anki_models import recall_model, recognize_model
from services.delete_files import delete_audio_files
import io



st.session_state

# Define default column names and their corresponding target names
DEFAULT_COLUMNS = {
    'French': 'TargetLanguage',
    'English': 'UserLanguage',
    'English Auto': 'UserLanguage',
    'IPA': 'TargetIPA',
    'Notes': 'Notes'
}

# Function to match columns from user input to required columns
def match_columns(df):
    # Create a new DataFrame with expected columns
    matched_df = pd.DataFrame()
    
    # Iterate through each required column and check if it exists in the input DataFrame
    for default_col, target_col in DEFAULT_COLUMNS.items():
        if default_col in df.columns:
            matched_df[target_col] = df[default_col]
        else:
            matched_df[target_col] = ""  # Add empty column if missing
    
    return matched_df


# Streamlit app
st.title("Simple Flashcard Generator (with Model Selection)")

# Button to delete all audio files
if st.button("Delete all audio files"):
    delete_audio_files()
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
            raw_data = pd.read_csv(io.StringIO(input_text), sep='\t')

            # Match columns and adjust DataFrame structure
            data = match_columns(raw_data)

            # Display the DataFrame preview
            st.write("Here is your matched table:")
            st.dataframe(data)

            # Generate the Anki deck using the selected model and deck name
            anki_file = create_anki_deck(data, model, deck_name)
            st.success(f"Anki Deck '{deck_name}' generated successfully.")
            
            # Provide a download link for the generated Anki deck
            with open(anki_file, 'rb') as f:
                st.download_button(f"Download {deck_name}", f, file_name=anki_file)

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please input some text to generate flashcards.")