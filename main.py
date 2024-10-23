import streamlit as st
import pandas as pd
from services.anki_deck_creator import create_anki_deck
from services.anki_models import recall_model, recognize_model
import io


# Streamlit app
st.title("Simple Flashcard Generator (with Debugging)")

# Input text field for pasting TSV (tab-separated) content
input_text = st.text_area("Paste your table data here (tab-separated)")

# Button to trigger the generation of the Anki deck
if st.button("Generate Flashcards"):
    if input_text:
        try:
            # Convert the input text (tab-separated) to a DataFrame
            data = pd.read_csv(io.StringIO(input_text), sep='\t')
            st.write("Debug: Table successfully parsed into DataFrame.")
            st.write("Here is your table:")
            st.dataframe(data)

            # Hardcoded model to recall_model (you can define recall_model elsewhere)
            model = recall_model()
            st.write("Debug: Recall model initialized.")

            # Generate the Anki deck using the recall model
            anki_file = create_anki_deck(data, model)
            st.success(f"Anki Deck generated: {anki_file}")
            
            # Provide a download link for the generated Anki deck
            with open(anki_file, 'rb') as f:
                st.download_button('Download Anki Deck', f, file_name=anki_file)

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please input some text to generate flashcards.")