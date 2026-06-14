import src.systems.audio as audio


def test_starts_unmuted():
    """AudioSystem empieza sin mute."""
    audio.clear_cache()
    # Resetear estado por si tests anteriores lo dejaron mutado
    if audio.is_muted():
        audio.toggle_mute()
    assert not audio.is_muted()


def test_toggle_mute_activa():
    """toggle_mute activa el mute."""
    if audio.is_muted():
        audio.toggle_mute()
    audio.toggle_mute()
    assert audio.is_muted()
    audio.toggle_mute()  # restaurar


def test_toggle_mute_doble_restaura():
    """Doble toggle restaura estado original."""
    initial = audio.is_muted()
    audio.toggle_mute()
    audio.toggle_mute()
    assert audio.is_muted() == initial


def test_play_sfx_missing_file_no_crash():
    """play_sfx con archivo inexistente no lanza excepción."""
    audio.play_sfx("audio/sfx/__nonexistent_test__.wav")


def test_play_sfx_muted_no_carga_cache():
    """play_sfx mutado no carga ni cachea el archivo."""
    audio.clear_cache()
    if not audio.is_muted():
        audio.toggle_mute()
    audio.play_sfx("audio/sfx/__nonexistent_test__.wav")
    assert "audio/sfx/__nonexistent_test__.wav" not in audio._cache
    audio.toggle_mute()  # restaurar unmuted


def test_clear_cache_vacia_diccionario():
    """clear_cache vacía el diccionario _cache."""
    audio.clear_cache()
    assert audio._cache == {}
