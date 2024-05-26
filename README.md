# Speech Recognition using Whisper AI in Python

This desktop application can choose a desired file (.mp4) from local file path to make it a subtitle to be in it.

## Set Up

### Git

* Download this git to your desire local place

### Python

* Go to : https://www.python.org/downloads/
* Download and install the app.
* Check in the command prompt.
* Type `python -v`.

### Whisper AI, Pysrt, moviepy, tkinter, moviepy==2.0.0.dev2, imageio==2.25.1

* Open command prompt.
* Type `pip install openai-whisper pysrt tk moviepy, imageio==2.25.1, moviepy==2.0.0.dev2`

### PyTorch Installation

* Go to : [https://packaging.python.org/guides/tool-recommendations/](https://pytorch.org/get-started/locally/)
* Choose the specification you desire.

![title](PyTorch.jpg)

* Copy the command after choosing the selection.
* Run command prompt (windows) then paste the command.

### ffmpeg installation 

* Go to : https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z
* Extract the file.
* Go to environment variable, on system variables, choose path and click edit.
* Click new button. then paste the file path of ffmpeg with bin dir (Examples : `C:\ffmpeg\bin`)

### Chocolatey, imageMagick installation 

* Go to : https://chocolatey.org/install
* Choose individual and copy the command.

  ![title](Chocolatey.jpg)

* Open windows PowerShell as Administrator.
* Paste the command and wait for download.
* Then run `choco install imagemagick`
* All should be done
  
### imageMagick changes

* Open PowerShell as Administrator
* Locate the policy.xml File: On Windows, ImageMagick’s configuration files are typically located in a directory like C:\Program Files\ImageMagick-6.9.12-Q16 or similar. You will need to find the exact path where policy.xml is located.
* then run `(Get-Content -Path "C:\Path\To\ImageMagick-6.x.y\policy.xml") -replace 'none', 'read,write' | Set-Content -Path "C:\Path\To\ImageMagick-6.x.y\policy.xml"` Where `"C:\Path\To\ImageMagick-6.x.y\policy.xml"` is your policy.xml path in the ImageMagick Folder


## Running the program

* You can use command prompt or Visual studio code to run the program.
  
### Command Prompt
* Go to the path directory.
* Type `python main.py`
* The app should be popped up.

### Microsoft Visual Studio
* Open the `main.py`.
* Run the code, then the app will be pop up

## Using the program

* The program should be look like this
  
![type](Application.png)

* First you need to select the video (.mp4) from your local drive
* Then you choose language and model (Both must be filled)
  
* After that click start button, there will be a new file that contain audio file (.mp3), subtitle file (.srt), and text file (.txt)
* The new video that had been added the subtitle will be named `"file name"+subtitle.mp4`
