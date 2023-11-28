# Import the library after you have installed it
import piano_visualizer

# Create a piano with a midi file(s)
piano = piano_visualizer.Piano(["midi.mid"])

# Create a video with resolution/fps
video = piano_visualizer.Video((1920, 1080), 60)

# Add piano to video
video.add_piano(piano)

# Export video on multiple cores (1 for single)
video.export("check.mp4", num_cores=1, music=True)

# You can add music too! (although it is sometimes offset from video)
# video.export("your/export/path.mp4", num_cores=6, music=True)

# Progress bars should show up
# Once your video is exported it will be at the path you specified!