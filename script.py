import argparse
from gtts import gTTS
import os
from nltk.corpus import wordnet
from translate import Translator

def get_meaning(word):
    synsets = wordnet.synsets(word)
    if synsets:
        return synsets[0].definition()
    else:
        return None

def get_translation(word, lang):
    translator = Translator(to_lang=lang)
    return translator.translate(word)

def get_example_sentence(word):
    synsets = wordnet.synsets(word)
    if synsets and synsets[0].examples():
        return synsets[0].examples()[0]
    else:
        return None

def main(input_file, output_folder):
    # Load the words from your file
    with open(input_file, "r") as file:
        words = file.readlines()

    # Remove any whitespace from the words
    words = [word.strip() for word in words]

    # Set the language for the pronunciations
    language = "en"

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Generate and save the pronunciations
    for word in words:
        meaning = get_meaning(word)
        translation = get_translation(word, "zh")
        example = get_example_sentence(word)
        text_en = word
        if meaning:
            text_en += f". {meaning}"
        if example:
            text_en += f". Example: {example}"
        tts_en = gTTS(text=text_en, lang=language, slow=False)
        file_path_en = f"{output_folder}/{word}_en.mp3"
        tts_en.save(file_path_en)
        print(f"Saved pronunciation and meaning for '{word}' to '{file_path_en}'")
        tts_zh = gTTS(text=translation, lang='zh-cn', slow=False)
        file_path_zh = f"{output_folder}/{word}_zh.mp3"
        tts_zh.save(file_path_zh)
        print(f"Saved Chinese translation for '{word}' to '{file_path_zh}'")
        spelling_text = ' '.join(word)
        tts_spelling = gTTS(text=spelling_text, lang=language, slow=True)
        spelling_path = f"{output_folder}/{word}_spelling.mp3"
        tts_spelling.save(spelling_path)
        print(f"Saved spelling audio for '{word}' to '{spelling_path}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate pronunciation and translation audio files.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input file containing words.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output folder where audio files will be saved.")
    args = parser.parse_args()
    main(args.input, args.output)
