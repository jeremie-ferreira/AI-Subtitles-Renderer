import sys
import json
from faster_whisper import WhisperModel

def extract_word_timecodes(file_path, model_size="large-v3-turbo", output_file="timecodes.json"):
    print(f"Loading model '{model_size}'...")
    model = WhisperModel(model_size, device="cuda")

    print(f"Transcribing '{file_path}'...")
    segments, info = model.transcribe(file_path, beam_size=5, word_timestamps=True)
    words = []

    print(f"language: {info.language}")

    # data structure
    for segment in segments:
        for word in segment.words:
            words.append({
                "word": word.word,
                "start": word.start,
                "end": word.end
            })

    # save in JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(words, f, indent=4, ensure_ascii=False)

    print(f"Transcription and timecodes saved in {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <video_filepath>")
        sys.exit(1)

    input_file = sys.argv[1]
    extract_word_timecodes(input_file)
