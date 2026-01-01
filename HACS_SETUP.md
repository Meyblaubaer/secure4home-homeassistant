# HACS Setup Guide

Diese Anleitung zeigt, wie du die Integration HACS-kompatibel machst.

## ✅ Bereits erledigt

Die folgenden HACS-Anforderungen sind bereits erfüllt:

### 1. hacs.json korrigiert
- ❌ Entfernt: `domains` (nicht erlaubt in hacs.json)
- ❌ Entfernt: `iot_class` (nicht erlaubt in hacs.json)
- ✅ Behalten: `name`, `render_readme`, `homeassistant`

### 2. GitHub Issue Templates
- ✅ `.github/ISSUE_TEMPLATE/bug_report.yml`
- ✅ `.github/ISSUE_TEMPLATE/feature_request.yml`

### 3. GitHub Actions
- ✅ `.github/workflows/validate.yml` (HACS + Hassfest Validation)
- ✅ `.github/dependabot.yml` (automatische Updates)

### 4. README Badges
- ✅ HACS Badge
- ✅ Release Badge
- ✅ License Badge

## ⚠️ Noch zu erledigen nach GitHub Upload

### 1. Repository Topics hinzufügen

**Wichtig**: HACS erfordert Topics! Nach dem Upload:

1. Gehe zu https://github.com/Meyblaubaer/secure4home-homeassistant
2. Klicke auf ⚙️ **Zahnrad** neben "About"
3. Füge diese Topics hinzu:

```
homeassistant
home-automation
secure4home
blaupunkt
alarm-system
hacs
custom-integration
smart-home
home-assistant-component
```

4. Klicke **Save changes**

**Ohne Topics wird HACS-Validation fehlschlagen!**

### 2. Brands (Optional - nur für HACS Default Repository)

Die Brands-Warnung kannst du ignorieren, wenn du die Integration als **HACS Custom Repository** bereitstellst.

Falls du später zu **HACS Default** möchtest:
1. Erstelle PR zu https://github.com/home-assistant/brands
2. Füge Logo und Metadata hinzu
3. Warte auf Genehmigung

## Installation als HACS Custom Repository

Da die Integration als **Custom Repository** läuft, können Benutzer sie so installieren:

### Für Benutzer:

1. Öffne **HACS** in HomeAssistant
2. Klicke **Integrations**
3. Klicke **⋮ Menü** oben rechts
4. Wähle **Custom repositories**
5. Füge hinzu:
   - **Repository**: `https://github.com/Meyblaubaer/secure4home-homeassistant`
   - **Kategorie**: `Integration`
6. Klicke **Add**
7. Suche nach "Secure4Home"
8. Klicke **Download**

## HACS Validation Checks

Nach dem Upload werden diese Checks laufen:

### ✅ Sollte bestehen:
- Repository structure
- manifest.json
- README.md exists
- hacs.json format

### ⚠️ Warnings (können ignoriert werden):
- Brands (nur für Default Repository nötig)

### ❌ Muss behoben werden:
- **Topics**: Füge Topics manuell auf GitHub hinzu (siehe oben)

## Validation testen

Nach dem Upload kannst du die HACS Validation manuell testen:

1. Gehe zu **Actions** Tab
2. Wähle **Validate** Workflow
3. Klicke **Run workflow**
4. Überprüfe die Ergebnisse

## Troubleshooting

### Problem: "Repository has no valid topics"

**Lösung**: Topics manuell auf GitHub hinzufügen (siehe Schritt 1 oben)

### Problem: "Brands check failed"

**Lösung**: Ignorieren - nur für HACS Default Repository nötig

### Problem: "HACS JSON validation failed"

**Lösung**: Sollte mit der korrigierten hacs.json behoben sein

## Support

Falls HACS-Probleme auftreten:

1. Überprüfe https://hacs.xyz/docs/publish/include
2. Teste mit HACS Validation Action
3. Öffne Issue auf https://github.com/hacs/integration

---

**Nach erfolgreicher HACS-Setup können Benutzer die Integration einfach über HACS installieren!** 🚀
