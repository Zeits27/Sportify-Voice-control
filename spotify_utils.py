def get_current_playlist_id(sp):
    """Return the playlist ID if currently playing from a playlist, else None."""
    cp = sp.currently_playing()
    if not cp:
        return None
    ctx = cp.get("context")
    if ctx and ctx.get("type") == "playlist" and ctx.get("uri"):
        return ctx["uri"].split(":")[-1]
    return None


def ensure_track_in_current_playlist(sp):
    """
    If a track is playing and the context is a playlist,
    ensure the track is in that playlist (add it if missing).
    Returns a tuple: (playlist_id, playlist_name, track_id, track_name, artists, added:bool)
    """
    cp = sp.currently_playing()
    if not cp or not cp.get("item"):
        return None, None, None, None, None, False

    track = cp["item"]
    track_id = track.get("id")
    track_name = track.get("name")
    artists = ", ".join([artist["name"] for artist in track.get("artists", [])])

    if not track_id:
        return None, None, None, None, None, False

    playlist_id = get_current_playlist_id(sp)
    if not playlist_id:
        return None, None, track_id, track_name, artists, False

    playlist = sp.playlist(playlist_id, fields="name")
    playlist_name = playlist.get("name", "Unknown Playlist")

    results = sp.playlist_items(playlist_id, fields="items.track.id,total", limit=100)
    track_ids = [i["track"]["id"] for i in results["items"] if i.get("track")]

    if track_id in track_ids:
        return playlist_id, playlist_name, track_id, track_name, artists, False
    else:
        sp.playlist_add_items(playlist_id, [track_id])
        return playlist_id, playlist_name, track_id, track_name, artists, True

