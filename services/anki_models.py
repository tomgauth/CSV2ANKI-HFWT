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
            }
            .user_language {
                color: #373f51;
                font-size: 32px;
                font-weight: 700;
            }
            .target_language {
                font-size: 30px;
                font-weight: 700;
            }
            .target_audio {
                margin-top: 10px;
            }
            .target_ipa {
                font-size: 22px;
            }
            .notes {
                font-size: 20px;
                margin-top: 10px;
            }
            .copyright {
                font-size: 10px;
                margin-top: 15px;
                color: #00afb9;
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
            }
            .target_audio {
                margin-top: 10px;
            }
            .target_language {
                font-size: 30px;
                font-weight: 700;
            }
            .user_language {
                color: #373f51;
                font-size: 32px;
                font-weight: 700;
            }
            .target_ipa {
                font-size: 22px;
            }
            .notes {
                font-size: 20px;
                margin-top: 10px;
            }
            .copyright {
                font-size: 10px;
                margin-top: 15px;
                color: #00afb9;
            }
        '''
    )