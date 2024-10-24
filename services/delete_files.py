import os

def delete_audio_files(audio_folder='audio_files'):
    """
    Supprime tous les fichiers audio dans le dossier spécifié.
    """
    if os.path.exists(audio_folder):
        for filename in os.listdir(audio_folder):
            if filename.endswith('.mp3'):
                os.remove(os.path.join(audio_folder, filename))
        print(f"Tous les fichiers audio ont été supprimés de {audio_folder}.")
    else:
        print(f"Le dossier {audio_folder} n'existe pas.")