# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Geplante Features
- WebSocket Support für Echtzeit-Updates
- Zone/Device Sensoren
- Event History Integration
- Kamera-Integration (falls API unterstützt)

## [1.0.0] - 2026-01-01

### Added
- Initial Release der Integration
- **Alarm Control Panel Entity**
  - ARM_AWAY Modus
  - ARM_HOME Modus
  - DISARM Modus
  - PIN Code Authentifizierung
  - Multi-Area Support
- **Binary Sensors**
  - Tamper Sensor (Sabotage-Alarm)
  - AC Power Sensor (Stromversorgung)
  - Battery Sensor (Batteriestatus)
- **Sensors**
  - Signal Strength (RSSI)
  - GSM Signal Strength
- **API Client**
  - JWT Token Authentifizierung
  - GET panel/mode Endpoint
  - GET panel/status Endpoint
  - POST panel/mode Endpoint
- **DataUpdateCoordinator**
  - Automatisches Polling alle 30 Sekunden
  - Fehlerbehandlung mit UpdateFailed
- **Config Flow**
  - Benutzerfreundliche Einrichtung via UI
  - Credential Validation
- **Dokumentation**
  - README.md mit ausführlicher Anleitung
  - CONTRIBUTING.md für Entwickler
  - API Dokumentation
- **Testing**
  - Standalone API Test Script
  - HACS Validation Workflow
  - Hassfest Validation Workflow

### Fixed
- Token-Feld korrigiert von `sToken` zu `token`
- State Enum Migration von `STATE_ALARM_*` zu `AlarmControlPanelState`
- CodeFormat.NUMBER für PIN Code Eingabe
- TRIGGER_DISARM Feature Flag für Disarm-Operationen

### Technical Details
- Python 3.11+ Kompatibilität
- HomeAssistant 2024.1.0+ Kompatibilität
- API Base URL: `https://eu.bphomeconnect.com/REST/v2/`
- Async/Await Implementation mit aiohttp
- Type Hints für alle Funktionen

### Known Limitations
- `POST user/info` Endpoint gibt 500 Fehler zurück (nicht kritisch)
- Area Names können leer sein - Fallback zu "Secure4Home Area X"
- Kein WebSocket Support - nur Polling (30s Intervall)

[Unreleased]: https://github.com/Meyblaubaer/secure4home-homeassistant/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Meyblaubaer/secure4home-homeassistant/releases/tag/v1.0.0
