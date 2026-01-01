# Installation Guide

Diese Anleitung erklärt Schritt für Schritt, wie du die Secure4Home Integration in HomeAssistant installierst.

## Voraussetzungen

- HomeAssistant 2024.1.0 oder höher
- Zugang zu deinem HomeAssistant Filesystem (via SSH, Samba, oder File Editor Add-on)
- Secure4Home / Blaupunkt Alarmanlage mit aktiven Zugangsdaten

## Installations-Methoden

### Methode 1: HACS Installation (empfohlen)

HACS (Home Assistant Community Store) ist der einfachste Weg, Custom Integrations zu installieren.

#### 1. HACS installieren

Falls noch nicht installiert, folge der [HACS Installation Guide](https://hacs.xyz/docs/setup/download).

#### 2. Custom Repository hinzufügen

1. Öffne **HACS** in HomeAssistant
2. Klicke auf **Integrations**
3. Klicke auf das **Menü (⋮)** oben rechts
4. Wähle **Custom repositories**
5. Füge hinzu:
   - **Repository**: `https://github.com/Meyblaubaer/secure4home-homeassistant`
   - **Kategorie**: `Integration`
6. Klicke **Add**

#### 3. Integration installieren

1. Suche in HACS nach **"Secure4Home"**
2. Klicke auf die Integration
3. Klicke **Download**
4. Wähle die neueste Version
5. Bestätige den Download

#### 4. HomeAssistant neu starten

Gehe zu:
**Einstellungen** → **System** → **Neu starten**

---

### Methode 2: Manuelle Installation via SSH

Diese Methode ist ideal, wenn du direkten SSH-Zugang zu deinem HomeAssistant hast.

#### 1. Mit HomeAssistant verbinden

```bash
ssh root@DEINE-HOMEASSISTANT-IP
```

#### 2. Integration kopieren

```bash
# Erstelle custom_components Ordner falls nicht vorhanden
mkdir -p /config/custom_components

# Lade die Integration herunter
cd /tmp
wget https://github.com/Meyblaubaer/secure4home-homeassistant/archive/main.zip
unzip main.zip

# Kopiere die Integration
cp -r secure4home-homeassistant-main/custom_components/secure4home /config/custom_components/

# Aufräumen
rm -rf /tmp/secure4home-homeassistant-main main.zip
```

#### 3. Berechtigungen setzen

```bash
chown -R homeassistant:homeassistant /config/custom_components/secure4home
```

#### 4. HomeAssistant neu starten

```bash
# Via CLI
ha core restart

# Oder via UI:
# Einstellungen → System → Neu starten
```

---

### Methode 3: Manuelle Installation via Samba/File Share

Diese Methode ist ideal, wenn du über das Netzwerk auf deine HomeAssistant-Dateien zugreifst.

#### 1. Samba Share öffnen

**Windows:**
```
\\HOMEASSISTANT-IP\config
```

**Mac:**
```
smb://HOMEASSISTANT-IP/config
```

**Linux:**
```
smb://HOMEASSISTANT-IP/config
```

#### 2. Integration kopieren

1. Öffne den `config` Ordner
2. Erstelle einen Ordner `custom_components` (falls nicht vorhanden)
3. Lade die Integration von GitHub herunter:
   - Gehe zu https://github.com/Meyblaubaer/secure4home-homeassistant
   - Klicke **Code** → **Download ZIP**
4. Entpacke die ZIP-Datei
5. Kopiere den Ordner `custom_components/secure4home` in deinen `config/custom_components/` Ordner

#### 3. HomeAssistant neu starten

Gehe zu:
**Einstellungen** → **System** → **Neu starten**

---

### Methode 4: File Editor Add-on (für Fortgeschrittene)

Falls du das "File Editor" oder "Studio Code Server" Add-on verwendest:

#### 1. File Editor öffnen

Gehe zu **Add-ons** → **File Editor**

#### 2. Ordnerstruktur erstellen

Erstelle folgende Struktur:
```
/config/custom_components/secure4home/
```

#### 3. Dateien manuell erstellen

Kopiere den Inhalt jeder Datei aus dem GitHub Repository:

- `__init__.py`
- `manifest.json`
- `config_flow.py`
- `const.py`
- `api.py`
- `alarm_control_panel.py`
- `binary_sensor.py`
- `sensor.py`
- `strings.json`
- `translations/de.json` (optional)

#### 4. HomeAssistant neu starten

Gehe zu:
**Einstellungen** → **System** → **Neu starten**

---

## Integration einrichten

Nach dem Neustart:

### 1. Integration hinzufügen

1. Gehe zu **Einstellungen** → **Geräte & Dienste**
2. Klicke **+ INTEGRATION HINZUFÜGEN**
3. Suche nach **"Secure4Home"**
4. Klicke auf das Ergebnis

### 2. Zugangsdaten eingeben

Gib deine Secure4Home Zugangsdaten ein:
- **Benutzername**: Dein Secure4Home Benutzername
- **Passwort**: Dein Secure4Home Passwort

### 3. Verbindung wird getestet

Die Integration testet die Verbindung zur API. Bei Erfolg siehst du:
- ✅ "Erfolgreich eingerichtet"

### 4. Entities überprüfen

Nach der Einrichtung werden automatisch folgende Entities erstellt:

**Alarm Control Panel:**
- `alarm_control_panel.secure4home_area_1`

**Binary Sensors:**
- `binary_sensor.secure4home_tamper`
- `binary_sensor.secure4home_ac_power`
- `binary_sensor.secure4home_battery`

**Sensors:**
- `sensor.secure4home_signal_strength`
- `sensor.secure4home_gsm_signal`

---

## Debug-Logging aktivieren (optional)

Für Troubleshooting kannst du Debug-Logging aktivieren:

### 1. configuration.yaml bearbeiten

Füge hinzu:

```yaml
logger:
  default: warning
  logs:
    custom_components.secure4home: debug
```

### 2. HomeAssistant neu starten

### 3. Logs anzeigen

**Via UI:**
Gehe zu **Einstellungen** → **System** → **Protokolle**

**Via SSH:**
```bash
docker logs -f homeassistant | grep secure4home
```

---

## Verifizierung

### Test 1: Alarm Control Panel Karte

Erstelle eine Test-Karte in deiner Übersicht:

```yaml
type: alarm-panel
entity: alarm_control_panel.secure4home_area_1
states:
  - arm_away
  - arm_home
```

### Test 2: Status ändern

1. Klicke auf **"DISARM"** oder **"ARM AWAY"**
2. Gib deinen PIN-Code ein
3. Bestätige
4. Überprüfe, ob sich der Status ändert
5. Überprüfe in der Secure4Home App, ob der Status übereinstimmt

### Test 3: Sensoren überprüfen

Gehe zu **Entwicklerwerkzeuge** → **Zustände** und suche nach:
- `binary_sensor.secure4home_tamper`
- `sensor.secure4home_signal_strength`

---

## Problembehebung

### Integration wird nicht gefunden

**Problem**: "Secure4Home" erscheint nicht in der Integrationsliste

**Lösung**:
1. Überprüfe, ob der Ordner `/config/custom_components/secure4home/` existiert
2. Überprüfe, ob alle Dateien vorhanden sind (besonders `manifest.json`)
3. Starte HomeAssistant neu
4. Leere Browser-Cache (Strg+Shift+R)

### Login schlägt fehl

**Problem**: "Verbindung zur API fehlgeschlagen"

**Lösung**:
1. Überprüfe deine Zugangsdaten
2. Teste ob du dich in der Secure4Home App einloggen kannst
3. Überprüfe die Logs: **Einstellungen** → **System** → **Protokolle**
4. Teste die API mit dem Test-Script:
   ```bash
   python3 test_api_standalone.py
   ```

### Entities werden nicht erstellt

**Problem**: Keine Entities nach der Einrichtung

**Lösung**:
1. Aktiviere Debug-Logging (siehe oben)
2. Gehe zu **Einstellungen** → **System** → **Protokolle**
3. Suche nach Fehlern mit "secure4home"
4. Überprüfe die API-Responses mit dem Test-Script

### PIN-Code Abfrage erscheint nicht

**Problem**: Keine PIN-Eingabe beim Statuswechsel

**Lösung**:
1. Stelle sicher, dass du Version 1.0.0+ verwendest
2. Überprüfe die `alarm_control_panel.py` auf folgende Zeilen:
   ```python
   self._attr_code_format = CodeFormat.NUMBER
   self._attr_code_arm_required = True
   ```
3. Starte HomeAssistant neu

---

## Deinstallation

Falls du die Integration entfernen möchtest:

### 1. Integration entfernen

1. Gehe zu **Einstellungen** → **Geräte & Dienste**
2. Finde **Secure4Home**
3. Klicke auf **Optionen (⋮)**
4. Wähle **Löschen**

### 2. Dateien löschen

**Via SSH:**
```bash
rm -rf /config/custom_components/secure4home
```

**Via Samba:**
Lösche den Ordner `config/custom_components/secure4home`

### 3. HomeAssistant neu starten

---

## Nächste Schritte

Nach erfolgreicher Installation:

1. ✅ Erstelle Automationen (siehe [README.md](README.md))
2. ✅ Konfiguriere Benachrichtigungen
3. ✅ Teste alle Funktionen für 24 Stunden
4. ✅ Berichte Feedback oder Probleme auf [GitHub Issues](https://github.com/Meyblaubaer/secure4home-homeassistant/issues)

---

**Viel Erfolg mit deiner Installation!** 🚀
