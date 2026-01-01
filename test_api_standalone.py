#!/usr/bin/env python3
"""
Standalone Test-Script für Secure4Home API
Benötigt KEINE HomeAssistant Installation!
"""

import asyncio
import json
import logging
from typing import Any

import aiohttp

# Setup Logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
_LOGGER = logging.getLogger(__name__)

# API Constants
API_BASE_URL = "https://eu.bphomeconnect.com/REST/v2/"


class Secure4HomeAPI:
    """Standalone API Client für Secure4Home."""

    def __init__(self, username: str, password: str) -> None:
        """Initialize the API client."""
        self.username = username
        self.password = password
        self.token: str | None = None
        self.session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session

    async def close(self) -> None:
        """Close the session."""
        if self.session:
            await self.session.close()
            self.session = None

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
        require_auth: bool = True,
    ) -> dict[str, Any]:
        """Make API request."""
        session = await self._get_session()
        url = f"{API_BASE_URL}{endpoint}"

        headers = {"Content-Type": "application/json"}
        if require_auth and self.token:
            headers["token"] = self.token

        _LOGGER.debug("API Request: %s %s", method, url)
        if data:
            _LOGGER.debug("Request Data: %s", json.dumps(data, indent=2))

        async with session.request(
            method, url, json=data, headers=headers
        ) as response:
            response.raise_for_status()
            result = await response.json()
            _LOGGER.debug("API Response: %s", json.dumps(result, indent=2))
            return result

    async def login(self) -> bool:
        """Login to Secure4Home API."""
        try:
            data = {"account": self.username, "password": self.password}
            response = await self._request(
                "POST", "auth/login", data=data, require_auth=False
            )

            # Extract token from response
            # API uses "token" not "sToken"
            if "token" in response:
                self.token = response["token"]
                _LOGGER.info("Successfully logged in to Secure4Home")
                return True
            else:
                _LOGGER.error("No token in login response: %s", response.keys())
                return False

        except Exception as err:
            _LOGGER.error("Login failed: %s", err)
            raise

    async def get_panel_area(self) -> dict[str, Any]:
        """Get panel area configuration."""
        return await self._request("GET", "panel/area")

    async def get_panel_status(self) -> dict[str, Any]:
        """Get panel status (system health - battery, tamper, etc)."""
        return await self._request("GET", "panel/status")

    async def get_panel_mode(self) -> dict[str, Any]:
        """Get panel mode (current arm/disarm state)."""
        return await self._request("GET", "panel/mode")

    async def set_panel_mode(
        self, area: str, mode: str, pincode: str
    ) -> dict[str, Any]:
        """Set panel mode (arm/disarm/home)."""
        data = {"area": area, "mode": mode, "pincode": pincode}
        return await self._request("POST", "panel/mode", data=data)

    async def get_user_info(self) -> dict[str, Any]:
        """Get user information."""
        return await self._request("POST", "user/info")

    async def extend_token(self) -> bool:
        """Extend authentication token."""
        try:
            await self._request("GET", "auth/extend")
            return True
        except Exception as err:
            _LOGGER.error("Token extend failed: %s", err)
            return False

    async def logout(self) -> bool:
        """Logout from Secure4Home API."""
        try:
            await self._request("POST", "auth/logout")
            self.token = None
            return True
        except Exception as err:
            _LOGGER.error("Logout failed: %s", err)
            return False


async def test_login(username: str, password: str):
    """Testet den Login."""
    print("\n" + "="*60)
    print("TEST 1: Login")
    print("="*60)

    api = Secure4HomeAPI(username, password)

    try:
        success = await api.login()
        if success:
            print("✅ Login erfolgreich!")
            print(f"Token: {api.token[:20]}..." if api.token else "Kein Token")
        else:
            print("❌ Login fehlgeschlagen!")
            return None
    except Exception as e:
        print(f"❌ Login Error: {e}")
        import traceback
        traceback.print_exc()
        return None

    return api


async def test_panel_status(api: Secure4HomeAPI):
    """Testet das Abrufen des Panel Status (arm/disarm)."""
    print("\n" + "="*60)
    print("TEST 2: Panel Status (Arm/Disarm State)")
    print("="*60)

    try:
        data = await api.get_panel_status()
        print("✅ Panel Status erfolgreich abgerufen!")
        print("\nResponse-Struktur:")
        print(json.dumps(data, indent=2, ensure_ascii=False))

        # Speichere Response in Datei
        with open("api_response_panel_status.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("\n💾 Response gespeichert in: api_response_panel_status.json")

        return data
    except Exception as e:
        print(f"❌ Panel Status Error: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_panel_mode(api: Secure4HomeAPI):
    """Testet das Abrufen des Panel Mode (WICHTIG - aktueller Alarm-Status!)."""
    print("\n" + "="*60)
    print("TEST 3: Panel Mode (Current Alarm State) ⭐ WICHTIG!")
    print("="*60)

    try:
        data = await api.get_panel_mode()
        print("✅ Panel Mode erfolgreich abgerufen!")
        print("\nResponse-Struktur:")
        print(json.dumps(data, indent=2, ensure_ascii=False))

        # Speichere Response in Datei
        with open("api_response_panel_mode.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("\n💾 Response gespeichert in: api_response_panel_mode.json")

        # Zeige aktuellen Modus prominent an
        if isinstance(data, dict) and "mode" in data:
            print(f"\n🎯 AKTUELLER MODUS: {data['mode'].upper()}")
            print(f"   Area: {data.get('area', 'N/A')}")
            print(f"   Area Name: {data.get('area_name', 'N/A')}")
            print(f"   Burglar: {data.get('burglar', 'N/A')}")

        return data
    except Exception as e:
        print(f"❌ Panel Mode Error: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_panel_area(api: Secure4HomeAPI):
    """Testet das Abrufen der Panel Area Konfiguration."""
    print("\n" + "="*60)
    print("TEST 4: Panel Area Configuration")
    print("="*60)

    try:
        data = await api.get_panel_area()
        print("✅ Panel Area erfolgreich abgerufen!")
        print("\nResponse-Struktur:")
        print(json.dumps(data, indent=2, ensure_ascii=False))

        # Speichere Response in Datei
        with open("api_response_panel_area.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("\n💾 Response gespeichert in: api_response_panel_area.json")

        return data
    except Exception as e:
        print(f"❌ Panel Area Error: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_user_info(api: Secure4HomeAPI):
    """Testet das Abrufen der User Info."""
    print("\n" + "="*60)
    print("TEST 5: User Info")
    print("="*60)

    try:
        data = await api.get_user_info()
        print("✅ User Info erfolgreich abgerufen!")
        print("\nResponse-Struktur:")
        print(json.dumps(data, indent=2, ensure_ascii=False))

        with open("api_response_user_info.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("\n💾 Response gespeichert in: api_response_user_info.json")

        return data
    except Exception as e:
        print(f"❌ User Info Error: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_set_mode(api: Secure4HomeAPI, area: str, mode: str, pincode: str):
    """Testet das Setzen eines Panel-Modus."""
    print("\n" + "="*60)
    print(f"TEST 6: Set Panel Mode (Area: {area}, Mode: {mode})")
    print("="*60)

    confirm = input(f"⚠️  Dies wird den Alarm auf '{mode}' setzen. Fortfahren? (y/n): ")
    if confirm.lower() != 'y':
        print("⏭️  Test übersprungen")
        return None

    try:
        data = await api.set_panel_mode(area, mode, pincode)
        print("✅ Modus erfolgreich geändert!")
        print("\nResponse:")
        print(json.dumps(data, indent=2, ensure_ascii=False))

        return data
    except Exception as e:
        print(f"❌ Set Mode Error: {e}")
        import traceback
        traceback.print_exc()
        return None


async def analyze_panel_data(data: dict):
    """Analysiert die Panel-Daten und gibt Hinweise zur Code-Anpassung."""
    print("\n" + "="*60)
    print("ANALYSE: Panel Area Response")
    print("="*60)

    if not data:
        print("❌ Keine Daten zum Analysieren")
        return

    print("\n📊 Gefundene Haupt-Keys:")
    for key in data.keys():
        value = data[key]
        value_type = type(value).__name__
        if isinstance(value, list):
            print(f"  - {key}: {value_type} (Länge: {len(value)})")
        else:
            print(f"  - {key}: {value_type}")

    # Suche nach Areas
    print("\n🔍 Suche nach Area-Informationen...")

    area_candidates = []
    for key, value in data.items():
        if isinstance(value, list) and value:
            print(f"\n  📋 Liste gefunden: '{key}' (Länge: {len(value)})")
            if isinstance(value[0], dict):
                print(f"     Erstes Element ist ein Dictionary mit Keys:")
                for k in value[0].keys():
                    print(f"       - {k}")
                area_candidates.append((key, value[0]))

    print("\n" + "="*60)
    print("💡 CODE-ANPASSUNGS-HINWEISE")
    print("="*60)

    if area_candidates:
        for candidate_key, sample in area_candidates:
            print(f"\n🎯 Falls '{candidate_key}' die Areas enthält:")
            print(f"\n1. In alarm_control_panel.py Zeile ~62 ändern zu:")
            print(f"   OLD: areas = coordinator.data.get(\"areas\", [])")
            print(f"   NEW: areas = coordinator.data.get(\"{candidate_key}\", [])")

            print(f"\n2. Mögliche Keys im Area-Objekt:")
            for k, v in sample.items():
                print(f"   - {k}: {v} (Type: {type(v).__name__})")

            # Versuche Mode/Status zu finden
            print(f"\n3. Suche nach Mode/Status-Key:")
            status_keys = [k for k in sample.keys() if 'mode' in k.lower() or 'status' in k.lower() or 'state' in k.lower()]
            if status_keys:
                print(f"   Gefundene Status-Keys: {status_keys}")
                for sk in status_keys:
                    print(f"   → {sk} = {sample[sk]}")
                    print(f"\n   In alarm_control_panel.py Zeile ~70 verwenden:")
                    print(f"   mode = area.get(\"{sk}\", \"\").lower()")
            else:
                print("   ⚠️ Kein offensichtlicher Status-Key gefunden")

            # Suche nach Area ID
            print(f"\n4. Suche nach Area-ID-Key:")
            id_keys = [k for k in sample.keys() if 'id' in k.lower() or 'num' in k.lower() or 'index' in k.lower()]
            if id_keys:
                print(f"   Gefundene ID-Keys: {id_keys}")
                for ik in id_keys:
                    print(f"   → {ik} = {sample[ik]}")
            else:
                print("   ℹ️ Verwende vermutlich nur Index in Liste")

    else:
        print("\n⚠️  Keine offensichtliche Area-Liste gefunden!")
        print("Die Response-Struktur ist anders als erwartet.")
        print("\nÜberprüfe die api_response_panel_area.json Datei manuell")

    print("\n" + "="*60)


async def main():
    """Haupt-Test-Funktion."""
    print("""
╔════════════════════════════════════════════════════════════╗
║       Secure4Home API Test Script (Standalone)             ║
║                                                            ║
║  Benötigt KEINE HomeAssistant Installation                ║
╚════════════════════════════════════════════════════════════╝
    """)

    # Hole Zugangsdaten
    print("Bitte gib deine Secure4Home Zugangsdaten ein:")
    username = input("Benutzername: ").strip()
    password = input("Passwort: ").strip()

    if not username or not password:
        print("❌ Benutzername und Passwort erforderlich!")
        return

    api = None

    try:
        # Test 1: Login
        api = await test_login(username, password)
        if not api:
            print("\n❌ Login fehlgeschlagen. Kann nicht fortfahren.")
            return

        # Test 2: Panel Status (System Health)
        panel_status = await test_panel_status(api)

        # Test 3: Panel Mode (⭐ CRITICAL - aktueller Alarm-Status!)
        panel_mode = await test_panel_mode(api)

        # Test 4: Panel Area (Konfiguration)
        panel_data = await test_panel_area(api)

        # Test 5: User Info
        await test_user_info(api)

        # Analyse
        if panel_data:
            await analyze_panel_data(panel_data)

        # Test 4: Optional - Modus ändern
        print("\n" + "="*60)
        print("OPTIONAL: Modus-Änderung testen")
        print("="*60)

        test_mode = input("\nMöchtest du das Ändern des Modus testen? (y/n): ")
        if test_mode.lower() == 'y':
            area = input("Area (z.B. '1'): ").strip() or "1"
            print("\nVerfügbare Modi:")
            print("  - disarm (Unscharf)")
            print("  - arm (Scharf/Away)")
            print("  - home (Scharf/Home)")
            mode = input("Mode (arm/disarm/home): ").strip() or "disarm"
            pincode = input("PIN-Code: ").strip()

            if pincode:
                await test_set_mode(api, area, mode, pincode)

                # Panel Mode erneut abrufen um Änderung zu sehen
                print("\n🔄 Warte 3 Sekunden und rufe Panel Mode erneut ab...")
                await asyncio.sleep(3)
                updated_mode = await test_panel_mode(api)

                if updated_mode and panel_mode:
                    print("\n📊 Vergleich Modus vorher/nachher:")
                    print(f"Vorher: {panel_mode.get('mode', 'N/A') if isinstance(panel_mode, dict) else panel_mode}")
                    print(f"Nachher: {updated_mode.get('mode', 'N/A') if isinstance(updated_mode, dict) else updated_mode}")

        # Zusammenfassung
        print("\n" + "="*60)
        print("✅ TESTS ABGESCHLOSSEN")
        print("="*60)
        print("\n📁 Erstellte Dateien:")
        import os
        if os.path.exists("api_response_panel_mode.json"):
            print("  ⭐ api_response_panel_mode.json (WICHTIG - enthält Alarm-Status!)")
        if os.path.exists("api_response_panel_status.json"):
            print("  ✅ api_response_panel_status.json (System Health)")
        if os.path.exists("api_response_panel_area.json"):
            print("  ✅ api_response_panel_area.json (Konfiguration)")
        if os.path.exists("api_response_user_info.json"):
            print("  ✅ api_response_user_info.json (User Info)")

        print("\n💡 Nächste Schritte:")
        print("  1. Überprüfe die JSON-Dateien")
        print("  2. ⭐ api_response_panel_mode.json enthält den aktuellen Alarm-Status!")
        print("  3. Passe custom_components/secure4home/api.py an (GET panel/mode)")
        print("  4. Installiere die Integration in Home Assistant")
        print("  5. Siehe TESTING.md für weitere Schritte")

    except KeyboardInterrupt:
        print("\n\n⚠️  Test abgebrochen durch Benutzer")
    except Exception as e:
        print(f"\n❌ Unerwarteter Fehler: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        if api:
            print("\n🧹 Schließe API-Verbindung...")
            await api.close()

    print("\n" + "="*60)
    print("Vielen Dank fürs Testen! 🚀")
    print("="*60 + "\n")


if __name__ == "__main__":
    # Check für aiohttp
    try:
        import aiohttp
    except ImportError:
        print("❌ FEHLER: aiohttp ist nicht installiert!")
        print("\nBitte installiere es mit:")
        print("  pip3 install aiohttp")
        print("\nDann führe dieses Script erneut aus.")
        exit(1)

    asyncio.run(main())
