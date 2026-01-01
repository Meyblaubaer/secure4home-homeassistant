# 🚀 Quick Start - GitHub Upload

## Voraussetzungen

- GitHub Account: https://github.com/Meyblaubaer
- Git installiert auf deinem Mac

## Schritt 1: GitHub Repository erstellen

1. Gehe zu https://github.com/new
2. **Repository name**: `secure4home-homeassistant`
3. **Description**: `HomeAssistant Custom Integration für Secure4Home / Blaupunkt Alarmanlagen`
4. **Public** (damit andere es nutzen können)
5. ❌ **NICHT** "Initialize with README" aktivieren
6. Klicke **Create repository**

## Schritt 2: Upload durchführen

Öffne Terminal und führe aus:

```bash
# Navigiere zum Repository
cd /Users/sven-christianmeyhoefer/Downloads/secure4home-homeassistant-repo

# Git initialisieren
git init

# Alle Dateien hinzufügen
git add .

# Ersten Commit erstellen
git commit -m "Initial commit - Secure4Home HomeAssistant Integration v1.0.0"

# Branch auf main setzen
git branch -M main

# Mit GitHub verbinden
git remote add origin https://github.com/Meyblaubaer/secure4home-homeassistant.git

# Hochladen
git push -u origin main
```

## Schritt 3: GitHub Personal Access Token (falls nötig)

Falls beim `git push` nach einem Passwort gefragt wird:

1. Gehe zu https://github.com/settings/tokens
2. **Generate new token** → **Generate new token (classic)**
3. **Note**: `HomeAssistant Secure4Home`
4. **Expiration**: `90 days` (oder länger)
5. **Scopes**: Aktiviere `repo` (voller Zugriff)
6. Klicke **Generate token**
7. **KOPIERE DEN TOKEN SOFORT** (wird nur einmal angezeigt!)
8. Verwende den Token als Passwort beim `git push`

## Schritt 4: Release erstellen (optional)

1. Gehe zu https://github.com/Meyblaubaer/secure4home-homeassistant/releases
2. Klicke **Create a new release**
3. **Tag version**: `v1.0.0`
4. **Release title**: `v1.0.0 - Initial Release`
5. **Description**:

```markdown
# Secure4Home HomeAssistant Integration v1.0.0

Erste offizielle Version der Secure4Home / Blaupunkt Alarmanlage Integration für HomeAssistant.

## Features

- ✅ Alarm Control Panel (ARM_AWAY, ARM_HOME, DISARM)
- ✅ PIN Code Authentifizierung
- ✅ Binary Sensors (Tamper, AC Power, Battery)
- ✅ Signal Sensors (RSSI, GSM)
- ✅ Multi-Area Support
- ✅ Automatisches Polling (30s)

## Installation

Siehe [INSTALLATION.md](https://github.com/Meyblaubaer/secure4home-homeassistant/blob/main/INSTALLATION.md)

## Getestet mit

- HomeAssistant 2024.1.0+
- Blaupunkt Q-Series Alarmanlagen
- API: https://eu.bphomeconnect.com/REST/v2/
```

6. Klicke **Publish release**

## Schritt 5: Repository-Settings

### Topics hinzufügen (für bessere Auffindbarkeit)

1. Gehe zu https://github.com/Meyblaubaer/secure4home-homeassistant
2. Klicke auf ⚙️ **Zahnrad** neben "About"
3. Füge Topics hinzu:
   - `homeassistant`
   - `home-automation`
   - `secure4home`
   - `blaupunkt`
   - `alarm-system`
   - `hacs`
   - `custom-integration`
   - `smart-home`
   - `home-assistant-component`

### GitHub Actions aktivieren

1. Gehe zu **Actions** Tab
2. Falls gefragt: **I understand my workflows, go ahead and enable them**

## Schritt 6: HACS Installation testen

Andere Benutzer können deine Integration jetzt via HACS installieren:

1. HACS öffnen in HomeAssistant
2. **Integrations**
3. **Menü (⋮)** → **Custom repositories**
4. URL eingeben: `https://github.com/Meyblaubaer/secure4home-homeassistant`
5. Kategorie: **Integration**
6. **Add**
7. Suche nach "Secure4Home"
8. **Download**

## Zukünftige Updates

Wenn du Änderungen machst:

```bash
cd /Users/sven-christianmeyhoefer/Downloads/secure4home-homeassistant-repo

# Änderungen anzeigen
git status

# Alle Änderungen hinzufügen
git add .

# Commit mit Beschreibung
git commit -m "Beschreibung der Änderung"

# Hochladen
git push
```

## Fertig! 🎉

Dein Repository ist jetzt öffentlich verfügbar unter:
**https://github.com/Meyblaubaer/secure4home-homeassistant**

Teile den Link mit anderen Blaupunkt/Secure4Home Benutzern!

---

## Troubleshooting

### Problem: "Permission denied (publickey)"

**Lösung**: Verwende Personal Access Token statt Passwort

### Problem: "Repository not found"

**Lösung**: Überprüfe ob das Repository existiert:
```bash
git remote -v
```

Falls falsch:
```bash
git remote set-url origin https://github.com/Meyblaubaer/secure4home-homeassistant.git
```

### Problem: "failed to push some refs"

**Lösung**: Pull zuerst, dann push:
```bash
git pull origin main --rebase
git push
```

---

**Bei Fragen**: Siehe [UPLOAD_TO_GITHUB.md](UPLOAD_TO_GITHUB.md) für ausführliche Anleitung
