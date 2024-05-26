import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import *
import os
import subprocess
import sys
import pysrt
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import whisper

def get_directory_path(file_path):
    return os.path.dirname(file_path)

def time_to_seconds(time_obj):
    return time_obj.hours * 3600 + time_obj.minutes * 60 + time_obj.seconds + time_obj.milliseconds / 1000


def create_subtitle_clips(subtitles, videosize,fontsize=24, font='Arial', color='yellow', debug = False):
    subtitle_clips = []

    for subtitle in subtitles:
        start_time = time_to_seconds(subtitle.start)
        end_time = time_to_seconds(subtitle.end)
        duration = end_time - start_time

        video_width, video_height = videosize

        text_clip = TextClip(subtitle.text, fontsize=fontsize, font=font, color=color, bg_color = 'black',size=(video_width*3/4, None), method='caption').set_start(start_time).set_duration(duration)
        subtitle_x_position = 'center'
        subtitle_y_position = video_height* 4 / 5

        text_position = (subtitle_x_position, subtitle_y_position)
        subtitle_clips.append(text_clip.set_position(text_position))

    return subtitle_clips

def add_subtitles_to_video (mp4filename, srtfilename):
    # Load video and SRT file
    video = VideoFileClip(mp4filename)
    subtitles = pysrt.open(srtfilename)

    begin,end= mp4filename.split(".mp4")
    output_video_file = begin+'_subtitled'+".mp4"

    print ("Output file name: ",output_video_file)

    # Create subtitle clips
    subtitle_clips = create_subtitle_clips(subtitles,video.size)

    # Add subtitles to the video
    final_video = CompositeVideoClip([video] + subtitle_clips)

    # Write output video file
    final_video.write_videofile(output_video_file)

    success = True
    return success

def format_time(seconds):
    """Convert time in seconds to SRT format (HH:MM:SS,MS)."""
    ms = int((seconds % 1) * 1000)
    seconds = int(seconds)
    mins, secs = divmod(seconds, 60)
    hrs, mins = divmod(mins, 60)
    return f"{hrs:02}:{mins:02}:{secs:02},{ms:03}"

def transcribe_audio(input_file, output_folder, language, model):
    # Load the Whisper model
    model = whisper.load_model(model)

    # Language
    result = model.transcribe(input_file, language=language)
    
    # Transcribe the audio file
    result = model.transcribe(input_file)
    
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Define the output file path
    base_name = os.path.basename(input_file)
    txt_output_file = os.path.join(output_folder, f"{os.path.splitext(base_name)[0]}.txt")
    srt_output_file = os.path.join(output_folder, f"{os.path.splitext(base_name)[0]}.srt")
    
    # Write the transcription to the output file
    with open(txt_output_file, "w") as f:
        f.write(result["text"])
    
    # Write the transcription to the .srt file
    with open(srt_output_file, "w") as f:
        for i, segment in enumerate(result["segments"]):
            start_time = segment["start"]
            end_time = segment["end"]
            text = segment["text"]

            # Format times as HH:MM:SS,MS
            start_time_formatted = format_time(start_time)
            end_time_formatted = format_time(end_time)

            f.write(f"{i+1}\n")
            f.write(f"{start_time_formatted} --> {end_time_formatted}\n")
            f.write(f"{text}\n\n")
    
    print(f"Transcription saved to: {txt_output_file} and {srt_output_file}")

    success = True

    return success
        

def select_video():
    file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    if file_path:
        selected_video_label.config(text="Selected Video: " + file_path)

def convert_to_mp3(video_file_path):
    try:
        # Ensure the file exists
        if not os.path.isfile(video_file_path):
            raise FileNotFoundError(f"The file {video_file_path} does not exist.")
        
        print(f"Attempting to load video file: {video_file_path}")
        
        # Load the mp4 file
        video = VideoFileClip(video_file_path)

        # Define the output mp3 file path
        mp3_file_path = video_file_path.replace(".mp4", ".mp3")
        
        # Extract audio from video  
        video.audio.write_audiofile(mp3_file_path)
        print(f"Audio extracted successfully to {mp3_file_path}")
        return mp3_file_path
    except Exception as e:
        print(f"Error during MP4 to MP3 conversion: {e}")
        return None

def start_process():
    if dropdown1_var.get() == "" or dropdown2_var.get() == "":
        messagebox.showerror("Error", "Please select options from both dropdowns.")
    else:
        video_file_path = selected_video_label.cget("text").replace("Selected Video: ", "")
        if video_file_path:
            print(f"Selected Video Path: {video_file_path}")
            mp3_file = convert_to_mp3(video_file_path)
            mp3_file_path = video_file_path.replace(".mp4", ".mp3")
            if mp3_file:
                output_dir = get_directory_path(mp3_file_path)
                srt_file = transcribe_audio(mp3_file_path, output_dir,  dropdown1_var.get(), dropdown2_var.get())
                if srt_file:
                    srt_file_path =  video_file_path.replace(".mp4", ".srt")
                    final_video = add_subtitles_to_video(video_file_path, srt_file_path)
                    print("test")
                    if final_video:
                        messagebox.showinfo("Success", f"Process completed successfully. Output video saved to {output_dir}")
                    else:
                        messagebox.showerror("Error", "Failed to add subtitles to video.")
                else:
                    messagebox.showerror("Error", "Whisper AI processing failed.")
            else:   
                messagebox.showerror("Error", "Failed to convert MP4 to MP3.")
        else:
            messagebox.showerror("Error", "No video file selected.")


# Create the main window
root = tk.Tk()
root.title("Simple Video Processor")
root.geometry("400x400")

# Create a frame
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

# Select Video button
select_video_btn = tk.Button(frame, text="Select Video MP4", command=select_video, width=20)
select_video_btn.grid(row=0, column=0, pady=10)

# Label to display selected video
selected_video_label = tk.Label(frame, text="Selected Video: ", wraplength=400)
selected_video_label.grid(row=1, column=0, pady=10)

# Dropdowns
options_dropdown1 = ["en", "id", "fr"]
options_dropdown2 = ["small", "medium", "large"]

# Text instructions for dropdown 1

text_dropdown1 = tk.Label(frame, text="Select Language:", font=("Arial", 12))
text_dropdown1.grid(row=2, column=0, pady=(0, 5))

# Dropdown 1
dropdown1_var = tk.StringVar()
dropdown1 = tk.OptionMenu(frame, dropdown1_var, *options_dropdown1)
dropdown1.config(width=20)
dropdown1.grid(row=3, column=0, pady=(0, 10))

# Text instructions for dropdown 2
text_dropdown2 = tk.Label(frame, text="Select Model:", font=("Arial", 12))
text_dropdown2.grid(row=4, column=0, pady=(0, 5))

# Dropdown 2
dropdown2_var = tk.StringVar()
dropdown2 = tk.OptionMenu(frame, dropdown2_var, *options_dropdown2)
dropdown2.config(width=20)
dropdown2.grid(row=5, column=0, pady=(0, 10))

# Start Button
start_btn = tk.Button(frame, text="Start", command=start_process, width=20)
start_btn.grid(row=6, column=0, pady=10)

# Run the main loop
root.mainloop()
