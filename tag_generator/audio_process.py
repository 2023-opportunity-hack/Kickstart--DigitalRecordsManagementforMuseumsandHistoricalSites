from moviepy.editor import VideoFileClip
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub import AudioSegment
import text_process
import shutil

def convert_video_to_audio(input_video, output_audio):
    # Load the video clip
    video_clip = VideoFileClip(input_video)

    # Extract the audio from the video
    audio_clip = video_clip.audio

    # Write the audio to an output file (e.g., MP3)
    audio_clip.write_audiofile(output_audio)

def transcribe_audio(path):
    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio_listened = r.record(source)
        # try converting it to text
        text = r.recognize_google(audio_listened)
    return text

def get_large_audio_transcription_on_silence(path):
    """Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks"""
    # open the audio file using pydub
    sound = AudioSegment.from_file(path)

    # split audio sound where silence is 500 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )

    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        try:
            text = transcribe_audio(chunk_filename)
        except sr.UnknownValueError as e:
            print("Error:", str(e))
        else:
            text = f"{text.capitalize()}. "
            # print(chunk_filename, ":", text)
            whole_text += text
    # return the text for all chunks detected
    # os.removedirs("audio-chunks")
    shutil.rmtree('audio-chunks')
    return whole_text

def mp3_to_wav(file_path):
    # convert mp3 file to wav
    print("ENtered mp3to wav")
    print("File path is ",file_path)
    sound = AudioSegment.from_mp3(file_path)
    sound.export("temp.wav", format="wav")
    print("Completed converting to wav")

def audio_process(file_path,extension):
    
    if extension in [".mp4"]:
        print("Processing a video file")
        convert_video_to_audio(file_path, "temp.mp3")
        mp3_to_wav("temp.mp3")
        os.remove("temp.mp3")
        print("Succesfully removed temp.mp3")

    if extension in [".mp3"]:
        print("Processing a mp3 file")
        mp3_to_wav(file_path)
    
    print("Transcribing the audio file")
    transcripts = get_large_audio_transcription_on_silence("temp.wav")
    os.remove("temp.wav")
    # return text_process.text_process(transcripts)
    text_file = open("Output.txt", "w")
    text_file.write(transcripts)
    text_file.close()

    output = text_process.text_process("Output.txt")
    os.remove("Output.txt")
    return output
 


    


