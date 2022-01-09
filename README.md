# Posture Watcher
Posture Watcher uses machine learning to alert you when your posture is
unfavorable.

## Demo
[![Thumbnail of YouTube video demo](https://img.youtube.com/vi/NH4ArIK9g18/0.jpg)](https://www.youtube.com/watch?v=NH4ArIK9g18)


## How does this work?
You set your base or desired posture and the app does the rest. Specifically,
it's checking for the devience from that base posture and it uses a moving
average to decide if you have gone over a predefined threshold.

## Motivation
I sit at my desk all day and I always find myself sitting in an unfavorable
posture. I came across the "Pose" component of the Mediapipe library and built
the core of this project in a weekend.

**This project very much is a work in progress.** Some of the things I plan to
add in the future include:
* Database support for storing deviance over time
* Some frontend interface for viewing useful information

## Running the application
1. Clone the application.
```
git clone https://github.com/Doxify/posture-watcher
```
2. Create a virtual environment and install the requirements.
```bash
python3 -m venv venv             # creating the virtual environment
source ./venv/bin/activate       # activating it
pip install -r requirements.txt  # installing dependencies
```
3. Launch the application.
```bash
python3 app.py
```
4. Once the application launches, follow the instructions on the window the pops
   up.
