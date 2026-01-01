# Secure4Home HomeAssistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/Meyblaubaer/secure4home-homeassistant.svg)](https://github.com/Meyblaubaer/secure4home-homeassistant/releases)
[![License](https://img.shields.io/github/license/Meyblaubaer/secure4home-homeassistant.svg)](LICENSE)

HomeAssistant Custom Integration für Secure4Home / Blaupunkt Alarmanlagen.

> **Topics**: `homeassistant` `home-automation` `secure4home` `blaupunkt` `alarm-system` `hacs` `custom-integration` `smart-home` `home-assistant-component`

## Features

- **Alarm Control Panel** - Vollständige Kontrolle über Arm/Disarm/Home Modi
- **System Health Monitoring** - Binary Sensors für Tamper, AC Power, Battery
- **Signal Monitoring** - Sensors für RSSI und GSM Signal Strength
- **Multi-Area Support** - Unterstützung für mehrere Alarm-Bereiche
- **Automatische Updates** - Polling alle 30 Sekunden

## Unterstützte Geräte

Diese Integration wurde entwickelt und getestet mit:
- Blaupunkt Q-Series Alarmanlagen
- Secure4Home App v2.15.12
- API Endpoint: `https://eu.bphomeconnect.com/REST/v2/`

## Installation

### HACS (empfohlen)

1. Öffne HACS in HomeAssistant
2. Klicke auf "Integrations"
3. Klicke auf das Menü (⋮) oben rechts
4. Wähle "Custom repositories"
5. Füge diese Repository-URL hinzu: `https://github.com/Meyblaubaer/secure4home-homeassistant`
6. Kategorie: "Integration"
7. Klicke "Add"
8. Suche nach "Secure4Home" und installiere es
9. Starte HomeAssistant neu

### Manuelle Installation

1. Kopiere den `custom_components/secure4home` Ordner in dein HomeAssistant `config/custom_components/` Verzeichnis
2. Starte HomeAssistant neu

## Konfiguration

1. Gehe zu **Einstellungen** → **Geräte & Dienste**
2. Klicke **+ INTEGRATION HINZUFÜGEN**
3. Suche nach "Secure4Home"
4. Gib deine Zugangsdaten ein:
   - **Benutzername**: Dein Secure4Home Benutzername
   - **Passwort**: Dein Secure4Home Passwort

## Entities

Nach erfolgreicher Einrichtung werden folgende Entities erstellt:

### Alarm Control Panel
- `alarm_control_panel.secure4home_area_1` - Hauptalarm-Steuerung

### Binary Sensors (System Health)
- `binary_sensor.secure4home_tamper` - Sabotage-Alarm
- `binary_sensor.secure4home_ac_power` - Stromversorgung Status
- `binary_sensor.secure4home_battery` - Batterie Status

### Sensors (Signal)
- `sensor.secure4home_signal_strength` - RSSI Signalstärke
- `sensor.secure4home_gsm_signal` - GSM Signalstärke

## Verwendung

### Alarm Control Panel Karte

```yaml
type: alarm-panel
entity: alarm_control_panel.secure4home_area_1
states:
  - arm_away
  - arm_home
```

### Automatisierung Beispiel

```yaml
alias: Benachrichtigung bei Alarm
trigger:
  - platform: state
    entity_id: alarm_control_panel.secure4home_area_1
    to: armed_away
action:
  - service: notify.mobile_app
    data:
      message: "🔒 Alarm wurde scharf geschaltet!"
```

### Tamper Alarm

```yaml
alias: Sabotage-Alarm
trigger:
  - platform: state
    entity_id: binary_sensor.secure4home_tamper
    to: "on"
action:
  - service: notify.mobile_app
    data:
      message: "⚠️ SABOTAGE-ALARM erkannt!"
      title: "Sicherheitswarnung"
```

## Troubleshooting

### Logging aktivieren

Füge in `configuration.yaml` hinzu:

```yaml
logger:
  default: warning
  logs:
    custom_components.secure4home: debug
```

### Häufige Probleme

**Problem**: Integration lädt nicht
- **Lösung**: Überprüfe die Logs unter Einstellungen → System → Protokolle

**Problem**: Keine PIN-Abfrage beim Ändern des Status
- **Lösung**: Stelle sicher, dass du die neueste Version verwendest (v1.0.0+)

**Problem**: Entities werden nicht erstellt
- **Lösung**:
  1. Überprüfe die API-Verbindung
  2. Verifiziere deine Zugangsdaten
  3. Schaue in die Logs für detaillierte Fehlermeldungen

## API Dokumentation

Die Integration nutzt die Secure4Home REST API v2:

### Endpoints

- `POST auth/login` - Authentifizierung
- `GET panel/mode` - Aktueller Alarm-Status (arm/disarm/home)
- `GET panel/status` - System Health (battery, tamper, AC power)
- `POST panel/mode` - Alarm-Modus ändern

### Response-Struktur

**Panel Mode Response:**
```json
{
  "result": true,
  "code": "000",
  "message": "OK!",
  "data": [
    {
      "area": "1",
      "mode": "disarm",
      "burglar": false,
      "area_name": ""
    }
  ]
}
```

## Development

### Voraussetzungen

- Python 3.11+
- HomeAssistant 2024.1.0+

### Testing

Ein Standalone-Test-Script ist verfügbar:

```bash
cd custom_components/secure4home
python3 test_api_standalone.py
```

### API Testen

```bash
# Login und alle Endpoints testen
python3 test_api_standalone.py

# Outputs werden in JSON-Dateien gespeichert:
# - api_response_panel_mode.json
# - api_response_panel_status.json
```

## Bekannte Einschränkungen

1. ❌ `POST user/info` Endpoint gibt 500 Fehler zurück (nicht kritisch)
2. ⚠️ Area Names sind manchmal leer - Integration verwendet Fallback "Secure4Home Area X"
3. ⚠️ WebSocket/Push-Benachrichtigungen noch nicht implementiert (Polling mit 30s Intervall)

## Changelog

### v1.0.0 (2026-01-01)
- Initial Release
- Alarm Control Panel Entity
- Binary Sensors für System Health
- Sensors für Signal Strength
- Multi-Area Support
- PIN Code Authentifizierung

## Support

Falls Probleme auftreten:

1. Aktiviere Debug-Logging (siehe oben)
2. Überprüfe die [Issues](https://github.com/Meyblaubaer/secure4home-homeassistant/issues)
3. Erstelle ein neues Issue mit:
   - Vollständige Logs (Passwörter entfernen!)
   - HomeAssistant Version
   - Beschreibung des Problems
   - Schritte zur Reproduktion

## License

MIT License - siehe [LICENSE](LICENSE) Datei

## Credits

Entwickelt durch Reverse Engineering der Secure4Home Android App.

API Endpoint: `https://eu.bphomeconnect.com/REST/v2/`

---

**Hinweis**: Diese Integration ist nicht offiziell von Blaupunkt oder Secure4Home endorsed.
