

class Song:
    def __init__(self, **kwargs):
        self.title = kwargs.get("title")
        self.artist = kwargs.get("artist")
        self.art = kwargs.get("art_link")
        self.category = kwargs.get("category")
        self.download_link = kwargs.get("download_link", None)
        self.type = kwargs.get("track")
        