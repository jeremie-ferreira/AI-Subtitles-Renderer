# AI Subtitles Renderer

AI-Subtitles-Renderer is an innovative project that combines AI-powered transcription and computer vision to deliver dynamic and visually appealing subtitles. The project uses Faster-Whisper for fast and accurate transcription and OpenCV for seamless subtitle rendering.

## Features

- **AI-Powered Transcription**: Leveraging Faster-Whisper for quick and accurate speech-to-text conversion.
- **Dynamic Subtitle Effects**: Advanced animations and styles using Python libraries like PIL and OpenCV.
- **Customizable Styles**: Define unique styles and presets for your subtitles.
- **Word-Level Highlighting**: Highlights the active word in real-time, with customizable effects.
- **Bezier-Based Animations**: Smooth animations for pop-up effects and active word transitions.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jeremie-ferreira/AI-Subtitles-Renderer.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
    - **Faster-Whisper**: For transcription.
    - **OpenCV**: For video processing.
    - **Pillow**: For advanced image rendering.
    - **DotMap**: For simplified dictionary management.
    - **NumPy**: For mathematical operations.

## Usage

1. Place your video file in the `videos/` directory.
2. Generate the transcription json:
   ```bash
   python transcribe.py videos/sample.mp4
   ```
3. Verify that `timecodes.json` has been generated
4. Choose a style preset [list below](#subtitle-styles)
5. 
   ```bash
   python main.py videos/sample.mp4 videos/sample_subs.mp4 timecodes.json --style=spectre
   ```
4. Output video with subtitles will be saved as `videos/sample_subs.mp4`

## Subtitle Styles

**Spectre**: A sleek, lowercase white text with a bold black outline and a glowing animated background rectangle for emphasis.

**Vibe**: A sharp, uppercase white text with thick black strokes, accented by a bold yellow active color and a prominent shadow effect.

**Spark**: A playful, uppercase comic-style text with thick black outlines, vibrant blue active color, and a strong shadow effect for impact.

**Cozy**: A cozy, uppercase white text with thick black strokes, a solid black rounded background rectangle, and a pink active color for charm.

**Pure**: A clean, uppercase black text on a white rounded rectangle background, with no stroke or shadow, creating a minimalist and modern look.

## How It Works

1. **Transcription**: Faster-Whisper generates a timestamped transcription of the audio.
2. **Rendering**: Subtitles are rendered frame-by-frame with customizable animations and effects.
3. **Output**: A new video is created with the subtitles embedded.

## Configuration

### Adding New Styles
To add a new style:

1. Define it in the `styles.py` file
2. Customize its appearance and animations.
3. Add it in the Renderer constructor in `renderer.py`

## Roadmap
- **Word-by-Word Appearance**: Each word appears on screen precisely as it is pronounced in the audio.
- **Color Change**: Implement dynamic color transitions for text to highlight active words or add visual emphasis.
- **Shadow Effect**: Add customizable text shadows to create depth and improve readability.
- **Define Style by Arguments**: Allow users to define text styles dynamically using arguments (e.g., font, color, stroke, shadow, and background properties).

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- **Faster-Whisper** for transcription.
- **OpenCV** and **Pillow** for rendering.
- All open-source contributors and libraries that made this possible.


