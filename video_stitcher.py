#!/usr/bin/env python3
"""
Video Stitcher - Creates vertical 9:16 videos by combining a main clip (top) with background gameplay (bottom)
"""

import os
from moviepy.editor import VideoFileClip, CompositeVideoClip

def load_and_resize_video(video_path, target_size):
    """Load video and resize to target dimensions"""
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    clip = VideoFileClip(video_path)
    return clip.resize(target_size)

def loop_or_trim_video(video, target_duration):
    """Loop or trim video to match target duration"""
    if video.duration >= target_duration:
        return video.subclip(0, target_duration)
    else:
        # Calculate how many loops needed
        loops_needed = int(target_duration / video.duration) + 1
        looped = video.loop(loops_needed)
        return looped.subclip(0, target_duration)

def create_split_video(top_clip, bottom_clip, output_path):
    """Create final vertical video with top and bottom clips"""
    # Check if output file exists
    if os.path.exists(output_path):
        response = input(f"Output file '{output_path}' already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Operation cancelled.")
            return False
    
    # Position clips vertically
    top_positioned = top_clip.set_position(('center', 0))
    bottom_positioned = bottom_clip.set_position(('center', 960))
    
    # Composite final video
    final_video = CompositeVideoClip([top_positioned, bottom_positioned], size=(1080, 1920))
    
    # Write output
    final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
    
    # Clean up
    top_clip.close()
    bottom_clip.close()
    final_video.close()
    
    return True

def main():
    """Main function to process video files"""
    try:
        # Input files
        main_clip_path = "main_clip.mp4"
        background_clip_path = "background_clip.mp4"
        output_path = "stitched_output.mp4"
        
        print("Loading main clip...")
        main_clip = load_and_resize_video(main_clip_path, (1080, 960))
        main_duration = main_clip.duration
        
        print("Loading background clip...")
        background_clip = load_and_resize_video(background_clip_path, (1080, 960))
        
        print("Processing background clip...")
        # Remove audio and adjust duration
        background_clip = background_clip.without_audio()
        background_clip = loop_or_trim_video(background_clip, main_duration)
        
        print("Creating final video...")
        success = create_split_video(main_clip, background_clip, output_path)
        
        if success:
            print(f"Video successfully created: {output_path}")
            print(f"Duration: {main_duration:.2f} seconds")
            print(f"Resolution: 1080x1920 (9:16)")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()