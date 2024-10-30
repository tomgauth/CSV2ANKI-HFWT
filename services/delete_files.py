import os
import glob

def delete_audio_files():
    """
    Deletes all .mp3 files in the current directory.
    """
    for file_path in glob.glob("*.mp3"):
        os.remove(file_path)
    print("All .mp3 files have been deleted.")