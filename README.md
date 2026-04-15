# Reddit Meme App

Prosta aplikacja webowa wyświetlająca losowe memy z Reddita, pobierane przez [Meme API](https://github.com/D3vd/Meme_Api).

## Uruchomienie

### Docker Compose (zalecane)

```bash
docker compose up --build
```

### Docker

```bash
docker build -t meme-webapp .
docker run -p 5050:5050 meme-webapp
```

Aplikacja dostępna pod adresem: http://localhost:5050

## Zmienne środowiskowe

| Zmienna | Domyślna | Opis |
|---------|----------|------|
| `FLASK_DEBUG` | `false` | Włącz tryb debug Flaska |
