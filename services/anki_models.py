import genanki

# Language-agnostic recall model
def recall_model():
    return genanki.Model(
        1607392319,  # Unique model_id
        'Hack French With Tom Recall',
        fields=[
            {'name': 'UserLanguage'},  # User's language
            {'name': 'TargetLanguage'},  # Target language being learned
            {'name': 'TargetAudio'},  # Audio for target language
            {'name': 'TargetIPA'},  # IPA for the target language
            {'name': 'Notes'},  # Additional notes
            {'name': 'card_type'}
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '''
                    <div class="user_language">{{UserLanguage}}</div>
                ''',
                'afmt': '''
                    <div class="target_audio">{{TargetAudio}}</div>
                    <div class="target_language">{{TargetLanguage}}</div>
                    <div class="target_ipa">{{TargetIPA}}</div>
                    <div class="notes">{{Notes}}</div>
                    <div class="notes">{{card_type}}</div>
                    <div class="copyright">©HackFrenchWithTom</div>
                ''',
            },
        ],
        css='''
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;700&display=swap');
.card {
    background-color: #eeebd0;
    color: #0b2027;
    font-family: 'Quicksand', sans-serif;
    text-align: center; /* Centering the text */
    padding: 20px; /* Optional: Adding padding to create space within the card */
}

.user_language {
    color: #373f51;
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 20px; /* Added vertical space */
}

.target_language {
    font-size: 30px;
    font-weight: 700;
    margin-bottom: 20px; /* Added vertical space */
}

.target_audio {
    margin-top: 20px; /* Increased space above the audio */
}

.target_ipa {
    font-size: 22px;
    margin-top: 20px; /* Added vertical space */
}

.notes {
    font-size: 20px;
    margin-top: 20px; /* Increased space between notes and other elements */
}

.copyright {
    font-size: 10px;
    margin-top: 25px; /* Increased space above the copyright */
    color: #00afb9;
}

/* Optional: Center other block elements like audio or images */
.target_audio, .target_ipa, .notes {
    margin: 0 auto; /* Center block elements */
}
        '''
    )


def recognize_model():
    return genanki.Model(
        9807392321,  # Unique model_id
        'Language-Agnostic Recognize',
        fields=[
            {'name': 'UserLanguage'},
            {'name': 'TargetLanguage'},
            {'name': 'TargetAudio'},
            {'name': 'TargetIPA'},
            {'name': 'Notes'},
            {'name': 'card_type'}
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '''
                    <div class="target_audio">{{TargetAudio}}</div>
                ''',
                'afmt': '''
                    <div class="target_language">{{TargetLanguage}}</div>
                    <div class="user_language">{{UserLanguage}}</div>
                    <div class="target_ipa">{{TargetIPA}}</div>
                    <div class="notes">{{Notes}}</div>
                    <div class="notes">{{card_type}}</div>
                    <div class="copyright">©HackFrenchWithTom www.hackfrenchwithtom.com</div>
                ''',
            },
        ],
        css='''
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;700&display=swap');
.card {
    background-color: #eeebd0;
    color: #0b2027;
    font-family: 'Quicksand', sans-serif;
    text-align: center; /* Centering the text */
    padding: 20px; /* Optional: Adding padding to create space within the card */
}

.user_language {
    color: #373f51;
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 20px; /* Added vertical space */
}

.target_language {
    font-size: 30px;
    font-weight: 700;
    margin-bottom: 20px; /* Added vertical space */
}

.target_audio {
    margin-top: 20px; /* Increased space above the audio */
}

.target_ipa {
    font-size: 22px;
    margin-top: 20px; /* Added vertical space */
}

.notes {
    font-size: 20px;
    margin-top: 20px; /* Increased space between notes and other elements */
}

.copyright {
    font-size: 10px;
    margin-top: 25px; /* Increased space above the copyright */
    color: #00afb9;
}

/* Optional: Center other block elements like audio or images */
.target_audio, .target_ipa, .notes {
    margin: 0 auto; /* Center block elements */
}
        '''
    )