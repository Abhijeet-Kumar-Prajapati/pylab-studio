"""
Music library module containing song mappings and related functionality.
"""

# Dictionary mapping song names to their URLs
Music = {
    "shape of you": "https://www.youtube.com/watch?v=JGwWNGJdvx8",
    "despacito": "https://www.youtube.com/watch?v=kJQP7kiw5Fk",
    "believer": "https://www.youtube.com/watch?v=7wtfhZwyrcc",
    "perfect": "https://www.youtube.com/watch?v=2Vv-BfVoq4g",
    "faded": "https://www.youtube.com/watch?v=60ItHLz5WEA"
}

def get_song_url(song_name):
    """
    Get the URL for a song name.
    Returns None if song is not found.
    """
    return Music.get(song_name.lower())
