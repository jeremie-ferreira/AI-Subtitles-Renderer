import json
import subprocess
import sys
import argparse
from renderer import Renderer
import cv2

# Load subtitles from a JSON file
def load_subtitles_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

# Group words
def group_words(words, max):
    grouped_words = []
    current_group = []
    count = 0

    for i, word in enumerate(words):
        current_group.append(word)
        sentence_ending = word["word"][-1] in [".", "!", "?"]
        next_pause = (
            i < len(words) - 1
            and words[i + 1]["start"] - words[i]["end"] > 0.001
        )

        # Group after max words, a sentence ending, or a noticeable pause
        if count == max or sentence_ending or next_pause:
            grouped_words.append({
                "words": current_group,
                "sentence": "".join(w["word"] for w in current_group),
                "start": current_group[0]["start"],
                "end": current_group[-1]["end"]
            })
            current_group = []
            count = 0
        else:
            count += 1
    return grouped_words

# Generate subtitles for a video
def main(input_video, output_video, subtitles_json, style):
    # Load subtitles
    words = load_subtitles_from_json(subtitles_json)
    grouped_words = group_words(words, 5)

    # Load the input video
    cap = cv2.VideoCapture(input_video)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Configure the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    temp_video = "temp_no_audio.mp4"
    out = cv2.VideoWriter(temp_video, fourcc, fps, (frame_width, frame_height))

    renderer = Renderer(style, (frame_width // 2, frame_height // 2 + 100))

    # Process each frame and add subtitles
    frame_index = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame index to time in seconds
        current_time = frame_index / fps

        # Check if there are subtitles to display
        for group in grouped_words:
            if group["start"] <= current_time <= group["end"]:
                frame = renderer.draw_subtitle(frame, group['sentence'], group['words'], current_time)
                break

        # Write the processed frame to output video
        out.write(frame)
        frame_index += 1

    # Release resources
    cap.release()
    out.release()

    # Merge the original audio with the new video
    final_output = output_video
    command = ["ffmpeg", "-y", "-i", temp_video, "-i", input_video, "-c:v", "copy", "-c:a", "aac", "-map", "0:v:0", "-map", "1:a:0", final_output]
    subprocess.run(command)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script.py <input_video> <output_video> <subtitles_json>")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Add subtitles to your video")
    parser.add_argument("input_video", help="Input video path")
    parser.add_argument("output_video", help="Output video path")
    parser.add_argument("subtitles_json", help="Subtitle JSON file path")
    parser.add_argument("--style", default="hustle", help="Subtitle style (hustle, phantom)")
    
    args = parser.parse_args()
    main(args.input_video, args.output_video, args.subtitles_json, args.style)
