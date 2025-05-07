This project is a Python-based system that lets you control your computer’s volume using hand gestures detected via webcam. It uses OpenCV for video capture, MediaPipe for hand tracking, and Pycaw to interface with the system's audio controller.

💡 Features

Adjust volume by changing the distance between your thumb and index finger.

Automatically mute when pinky is lowered.

Live on-screen volume bar (only bar visible, no webcam feed).

Real-time performance with OpenCV + MediaPipe.

📦 Requirements

Install dependencies using pip:
pip install opencv-python mediapipe numpy pycaw comtypes

🛠 How It Works

Captures video from webcam.

Uses MediaPipe to detect hand landmarks.

Calculates distance between thumb tip and index tip.

Maps that distance to volume level (0–100%) using interpolation.

Mutes volume when pinky finger is below the ring finger (gesture for "mute").

Press q to exit.

💻 Demo Controls

Move thumb and index finger closer/farther apart to control volume.

Lower pinky finger to mute.

Raise pinky finger to unmute and adjust volume.

🧾 Files

volume_control.py: Main Python script

README.md: This file

📌 Notes

This script only shows the volume bar, not the camera feed.

Works best in well-lit environments for hand tracking.

Currently supports Windows only (due to Pycaw dependency).
