from dotenv import load_dotenv
import os
from pytube import YouTube
from src.utilities.Exceptions import TooManyFilesError

load_dotenv()


class MusicDownloader:
    """
    A class that is responsible for safely downloading ogg files
    """
    OGG_DIR = os.getenv('OGG_DIR')  # the path to the directory housing ogg files
    MAX_LENGTH = 10  # maximum length of song
    SEC_IN_MIN = 60
    MAX_VIDS_IN_DIR = 10  # maximum number of videos that can be stored
    TEMPLATE_VID_NAME = 'mus'  # basis for naming of music file
    MUSIC_FILE_FORMAT = 'ogg'  # the format in which music is saved

    def download_youtube_link(self, link: str):
        """
        Downloads a youtube link, and saves it as a music file. Returns its absolute poth.
        Throws up TooManyFIlesError if there are too many files in OGG_DIR
        :param link: a youtube link.
        :return: the absolute path of the downloaded link
        """

        # check size of directory
        files = [f for f in os.listdir(self.OGG_DIR) if os.path.isfile(os.path.join(self.OGG_DIR, f))]
        file_count = len(files)

        # if too many files, throw up error
        if file_count >= self.MAX_VIDS_IN_DIR:
            raise TooManyFilesError(f"Error: the directory already has at least {self.MAX_VIDS_IN_DIR} files")

        # define video download
        yt = YouTube(link)
        video = yt.streams.filter(only_audio=True).first()

        # download video file
        out_file = video.download(output_path=self.OGG_DIR)

        # change to music format
        for i in range(self.MAX_VIDS_IN_DIR):

            candidate_filename = os.path.join(self.OGG_DIR, f'{self.TEMPLATE_VID_NAME}{i}.{self.MUSIC_FILE_FORMAT}')
            # if name of music file does not exist, create that music file
            if not os.path.exists(candidate_filename):

                # convert file name and type
                os.rename(out_file, candidate_filename)

                # convert to absolute file path
                abs_path = os.path.abspath(candidate_filename)

                return abs_path








