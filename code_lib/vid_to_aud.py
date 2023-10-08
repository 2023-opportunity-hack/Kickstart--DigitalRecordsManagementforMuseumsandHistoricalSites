from moviepy.editor import VideoFileClip

def convert_video_to_audio(input_video, output_audio):
    # Load the video clip
    video_clip = VideoFileClip(input_video)

    # Extract the audio from the video
    audio_clip = video_clip.audio

    # Write the audio to an output file (e.g., MP3)
    audio_clip.write_audiofile(output_audio)

if __name__ == "__main__":
    input_video = "D:\Python\Hackathon\Kobayashi Video Final.mp4"  # Replace with the path to your video file
    output_audio = "output_audio.mp3"  # Replace with the desired output audio file name

    convert_video_to_audio(input_video, output_audio)
