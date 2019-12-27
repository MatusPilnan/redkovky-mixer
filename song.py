import os
import pathlib
import re

import mp3_tagger


class Song:
    def __init__(self, filename) -> None:
        super().__init__()
        assert filename.lower().endswith('.mp3'), "Only .mp3 files are supported."
        self.filename = filename
        self.mp3 = mp3_tagger.MP3File(filename)
        self.mp3.set_version(mp3_tagger.VERSION_2)
        self.title = self.mp3.song
        self.artist = self.mp3.artist
        if self.artist[-1] == '\0':
            self.artist = self.artist[:-1]
        if self.title[-1] == '\0':
            self.title = self.title[:-1]

    def to_dict(self, short_filename=False):
        filename = self.filename
        if short_filename:
            filename = self.short_filename
        return dict(title=self.title, artist=self.artist, filename=filename, song=self)

    def update_file_position(self, position):
        new_name = re.sub("^[^a-zA-Z]*", "{0:0=3d}".format(position) + "_", self.short_filename)
        new_name = self.filename.replace(self.short_filename, new_name)
        os.rename(self.filename, new_name)
        self.filename = new_name
        print(new_name)

    @property
    def short_filename(self):
        return str(pathlib.Path(self.filename).parts[-1])
