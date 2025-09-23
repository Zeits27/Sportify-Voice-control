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
    Returns a tuple: (playlist_id, track_id, added:bool)
    """
    cp = sp.currently_playing()
    if not cp or not cp.get("item"):
        return None, None, False

    track = cp["item"]
    track_id = track.get("id")
    if not track_id:
        return None, None, False

    playlist_id = get_current_playlist_id(sp)
    if not playlist_id:
        return None, track_id, False

    # Check if track already exists in playlist
    results = sp.playlist_items(playlist_id, fields="items.track.id,total", limit=100)
    track_ids = [i["track"]["id"] for i in results["items"] if i.get("track")]

    if track_id in track_ids:
        return playlist_id, track_id, False  # nothing added
    else:
        sp.playlist_add_items(playlist_id, [track_id])
        return playlist_id, track_id, True
