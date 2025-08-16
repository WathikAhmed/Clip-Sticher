# Video Stitcher

Creates vertical 9:16 videos by combining a main clip (top half) with background gameplay (bottom half).

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Place your video files in the same directory:
   - `main_clip.mp4` - Your 20-second talking head/reaction clip
   - `background_clip.mp4` - Your looping gameplay footage

2. Run the script:
   ```bash
   python video_stitcher.py
   ```

3. Output will be saved as `stitched/stitched_output.mp4`

## Features

- Automatically resizes clips to fit 1080x1920 (9:16) format
- Top half: Main clip (1080x960)
- Bottom half: Background clip (1080x960, muted)
- Background clip loops/trims to match main clip duration
- Preserves audio from main clip only
- Handles file overwrite confirmation