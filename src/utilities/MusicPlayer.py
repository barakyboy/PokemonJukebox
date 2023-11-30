from pydub import AudioSegment
from pydub.playback import play
from midi2audio import FluidSynth
import os

class MusicPlayer:
    """
    A class that is responsible for playing music in real time
    """


    def play_mp3(self, mp3_abs_path: str):
        """
        Plays an mp3 file in mp3_abs_path
        :param mp3_abs_path:  the mp3 file path that you would like to be played
        """

        audio = AudioSegment.from_file(mp3_abs_path, format="mp4")
        play(audio)

    def play_midi_and_delete(self, midi_abs_path: str, soundfont=None):
        """
        Plays a midi file in midi_abs_path. ALSO DELETES THE MIDI FILE
        :param midi_abs_path:  the mp3 file path that you would like to be played
        :param soundfont: a soundfont to be used by fluidsynth for synthesis. Default if None
        """

        # set soundfont
        if soundfont is None:
            fs = FluidSynth()
        else:
            fs = FluidSynth(soundfont)

        fs.play_midi(midi_abs_path)
        os.remove(midi_abs_path)




