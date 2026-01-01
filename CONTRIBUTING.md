# Contributing to Secure4Home HomeAssistant Integration

Vielen Dank für dein Interesse, zu diesem Projekt beizutragen!

## Entwicklungsumgebung einrichten

1. **Repository klonen:**
   ```bash
   git clone https://github.com/Meyblaubaer/secure4home-homeassistant.git
   cd secure4home-homeassistant
   ```

2. **Virtual Environment erstellen:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # oder
   venv\Scripts\activate  # Windows
   ```

3. **Dependencies installieren:**
   ```bash
   pip install -r requirements_dev.txt
   ```

## Code-Style

- Verwende **Black** für Code-Formatierung
- Verwende **Pylint** für Linting
- Verwende **Type Hints** wo möglich
- Docstrings im Google-Style Format

```python
def example_function(param: str) -> bool:
    """Short description of function.

    Args:
        param: Description of param.

    Returns:
        Description of return value.
    """
    return True
```

## Testing

### API Tests

```bash
cd custom_components/secure4home
python3 test_api_standalone.py
```

### Integration Tests

1. Kopiere die Integration in deine HomeAssistant Testinstanz
2. Aktiviere Debug-Logging:
   ```yaml
   logger:
     default: warning
     logs:
       custom_components.secure4home: debug
   ```
3. Teste alle Funktionen manuell

## Pull Request Guidelines

1. **Fork** das Repository
2. Erstelle einen **Feature Branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit** deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. **Push** zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen **Pull Request**

### PR Checklist

- [ ] Code folgt dem Projekt-Style
- [ ] Alle Tests laufen erfolgreich
- [ ] Neue Features sind dokumentiert
- [ ] README.md wurde aktualisiert (falls nötig)
- [ ] CHANGELOG.md wurde aktualisiert

## Bug Reports

Beim Erstellen eines Bug Reports, bitte folgende Informationen angeben:

- **HomeAssistant Version**
- **Integration Version**
- **Beschreibung des Problems**
- **Schritte zur Reproduktion**
- **Erwartetes Verhalten**
- **Tatsächliches Verhalten**
- **Logs** (mit Debug-Level, Passwörter entfernen!)

## Feature Requests

Feature Requests sind willkommen! Bitte beschreibe:

- **Use Case** - Warum ist das Feature nützlich?
- **Vorgeschlagene Implementation** - Wie könnte es umgesetzt werden?
- **Alternativen** - Welche Alternativen gibt es?

## API Reverse Engineering

Falls du neue API-Endpoints entdeckst:

1. Dokumentiere den Endpoint
2. Füge ein Beispiel-Response hinzu (JSON)
3. Teste mit `test_api_standalone.py`
4. Erstelle einen PR mit der Dokumentation

## Code of Conduct

- Sei respektvoll und konstruktiv
- Hilf anderen bei Problemen
- Teile dein Wissen

## Fragen?

Öffne ein [Issue](https://github.com/Meyblaubaer/secure4home-homeassistant/issues) oder starte eine [Discussion](https://github.com/Meyblaubaer/secure4home-homeassistant/discussions).

Vielen Dank für deine Unterstützung! 🙏
