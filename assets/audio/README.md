# Audio assets — Starfall

Este directorio está vacío en el repositorio. Agregar archivos de audio manualmente.

## Formatos

- SFX: `.wav` (sin compresión, baja latencia)
- Música: `.ogg` (comprimido, menor tamaño)

## Fuentes recomendadas (licencia libre)

- **OpenGameArt** — opengameart.org — CC0/CC-BY, amplia variedad
- **Freesound** — freesound.org — variedad, requiere cuenta gratuita
- **itch.io** — buscar "free sfx pack" o "chiptune music"

## Archivos esperados

| Ruta | Evento |
|------|--------|
| `sfx/shoot.wav` | Disparo del player |
| `sfx/impact.wav` | Bala impacta enemigo |
| `sfx/explosion.wav` | Enemigo o boss muere |
| `sfx/powerup.wav` | Player recoge power-up |
| `sfx/player_hit.wav` | Player recibe daño |
| `sfx/game_over.wav` | Pantalla game over |
| `sfx/boss_hit.wav` | Boss recibe daño |
| `music/gameplay.ogg` | Música de fondo en loop |

Si los archivos no están presentes, el juego arranca sin audio sin ningún crash.
