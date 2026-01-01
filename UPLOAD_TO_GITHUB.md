# GitHub Upload Anleitung

Diese Anleitung zeigt dir, wie du die Integration zu GitHub hochlädst.

## Schritt 1: GitHub Repository erstellen

1. Gehe zu [GitHub](https://github.com)
2. Klicke auf **New repository** (grüner Button oben rechts)
3. Fülle die Felder aus:
   - **Repository name**: `secure4home-homeassistant`
   - **Description**: `HomeAssistant Custom Integration für Secure4Home / Blaupunkt Alarmanlagen`
   - **Public** oder **Private**: Wähle "Public" wenn du es teilen möchtest
   - ❌ **NICHT** "Initialize with README" auswählen (wir haben schon einen README)
4. Klicke **Create repository**

## Schritt 2: Git initialisieren (lokal)

Öffne ein Terminal und navigiere zum Repository-Ordner:

```bash
cd /Users/sven-christianmeyhoefer/Downloads/secure4home-homeassistant-repo
```

### Git initialisieren

```bash
# Git Repository initialisieren
git init

# Alle Dateien zum Staging hinzufügen
git add .

# Ersten Commit erstellen
git commit -m "Initial commit - Secure4Home HomeAssistant Integration v1.0.0"
```

## Schritt 3: Mit GitHub verbinden

Ersetze `Meyblaubaer` mit deinem GitHub-Benutzernamen:

```bash
# Remote Repository hinzufügen
git remote add origin https://github.com/Meyblaubaer/secure4home-homeassistant.git

# Branch auf 'main' umbenennen (falls nötig)
git branch -M main

# Hochladen zu GitHub
git push -u origin main
```

### Authentifizierung

Wenn du nach Zugangsdaten gefragt wirst:

**Option 1: Personal Access Token (empfohlen)**
1. Gehe zu GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Wähle Scopes: `repo` (voller Zugriff)
4. Kopiere den Token
5. Verwende den Token als Passwort beim `git push`

**Option 2: SSH Key**
```bash
# SSH Key generieren (falls noch nicht vorhanden)
ssh-keygen -t ed25519 -C "deine-email@example.com"

# Public Key anzeigen
cat ~/.ssh/id_ed25519.pub

# Kopiere den Output und füge ihn auf GitHub hinzu:
# GitHub → Settings → SSH and GPG keys → New SSH key

# Remote auf SSH ändern
git remote set-url origin git@github.com:Meyblaubaer/secure4home-homeassistant.git
```

## Schritt 4: Verifizierung

Gehe zu deinem Repository auf GitHub:
```
https://github.com/Meyblaubaer/secure4home-homeassistant
```

Du solltest alle Dateien sehen:
- ✅ README.md
- ✅ custom_components/secure4home/
- ✅ LICENSE
- ✅ CHANGELOG.md
- ✅ etc.

## Schritt 5: GitHub Actions aktivieren (optional)

GitHub Actions sollten automatisch aktiviert werden. Überprüfe:

1. Gehe zu **Actions** Tab in deinem Repository
2. Aktiviere Workflows falls nötig
3. Die HACS und Hassfest Validations sollten automatisch laufen

## Schritt 6: Release erstellen (optional)

Um ein offizielles v1.0.0 Release zu erstellen:

1. Gehe zu deinem Repository auf GitHub
2. Klicke **Releases** → **Create a new release**
3. Fülle aus:
   - **Tag version**: `v1.0.0`
   - **Release title**: `v1.0.0 - Initial Release`
   - **Description**: Kopiere den Inhalt aus CHANGELOG.md
4. Klicke **Publish release**

## Schritt 7: README.md URLs aktualisieren

Nachdem das Repository erstellt ist, aktualisiere alle `Meyblaubaer` Platzhalter:

```bash
# In README.md
sed -i '' 's/Meyblaubaer/dein-echter-username/g' README.md

# In INSTALLATION.md
sed -i '' 's/Meyblaubaer/dein-echter-username/g' INSTALLATION.md

# In CONTRIBUTING.md
sed -i '' 's/Meyblaubaer/dein-echter-username/g' CONTRIBUTING.md

# In CHANGELOG.md
sed -i '' 's/Meyblaubaer/dein-echter-username/g' CHANGELOG.md

# Änderungen committen
git add .
git commit -m "Update repository URLs"
git push
```

## Schritt 8: HACS Kompatibilität (optional)

Falls du möchtest, dass andere deine Integration via HACS installieren können:

### Option A: HACS Default Repository (erfordert Genehmigung)

1. Gehe zu [HACS Integration Request](https://github.com/hacs/default/issues/new?template=integration.yml)
2. Fülle das Formular aus
3. Warte auf Genehmigung (kann einige Tage dauern)

### Option B: HACS Custom Repository (sofort verfügbar)

Benutzer können dein Repository manuell als Custom Repository hinzufügen:

1. HACS öffnen
2. Integrations
3. Menü (⋮) → Custom repositories
4. URL eingeben: `https://github.com/Meyblaubaer/secure4home-homeassistant`
5. Kategorie: Integration
6. Hinzufügen

## Zusätzliche Tipps

### .gitignore überprüfen

Stelle sicher, dass keine sensiblen Daten hochgeladen werden:

```bash
# Überprüfe was committed wird
git status

# Falls sensible Dateien aufgelistet sind, füge sie zur .gitignore hinzu
echo "geheime-datei.txt" >> .gitignore
git add .gitignore
git commit -m "Update .gitignore"
```

### GitHub Repository Settings

Empfohlene Settings für dein Repository:

1. **Settings** → **General**
   - ✅ Issues aktivieren
   - ✅ Discussions aktivieren (optional)

2. **Settings** → **Actions** → **General**
   - ✅ Allow all actions and reusable workflows

3. **Settings** → **Code and automation** → **Pages** (optional)
   - Falls du GitHub Pages für Dokumentation nutzen möchtest

### Repository Topics hinzufügen

Füge Topics hinzu für bessere Auffindbarkeit:

1. Klicke auf das **Zahnrad** neben "About"
2. Füge Topics hinzu:
   - `homeassistant`
   - `home-automation`
   - `secure4home`
   - `blaupunkt`
   - `alarm-system`
   - `hacs`
   - `custom-integration`

## Zukünftige Updates hochladen

Wenn du Änderungen machst:

```bash
# Status anzeigen
git status

# Geänderte Dateien hinzufügen
git add .

# Commit erstellen
git commit -m "Beschreibung der Änderungen"

# Zu GitHub hochladen
git push
```

## Troubleshooting

### Problem: "Permission denied"

**Lösung**: Überprüfe deine GitHub Zugangsdaten oder SSH Key

### Problem: "Repository not found"

**Lösung**: Überprüfe die Repository URL:
```bash
git remote -v
```

Falls falsch, korrigiere:
```bash
git remote set-url origin https://github.com/RICHTIGER-USERNAME/secure4home-homeassistant.git
```

### Problem: "Large files"

**Lösung**: Entferne große Dateien und füge sie zur .gitignore hinzu

---

**Viel Erfolg beim Upload zu GitHub!** 🚀

Nach dem Upload kannst du die URL zu deinem Repository teilen:
```
https://github.com/Meyblaubaer/secure4home-homeassistant
```
