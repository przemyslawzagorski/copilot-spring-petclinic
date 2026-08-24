"""Serwer MCP "PublicAPIs" — demonstracja pełnego protokołu MCP.

Trzy rodzaje zdolności, które serwer może udostępnić klientowi:

  * TOOLS     — czynność do wykonania. Model wywołuje ją sam, gdy uzna za potrzebną.
                Może kosztować czas/pieniądze i zmieniać stan świata.
  * RESOURCES — kontekst do przeczytania, adresowany przez URI. Użytkownik wciąga go
                jawnie (w Claude Code: `@nbp://rates/table-a`). Tylko odczyt.
  * PROMPTS   — gotowy przepływ pracy, uruchamiany przez użytkownika jako slash-komenda
                (w Claude Code: `/mcp__publiczne-api__analiza_kursu`).

Uwaga na transport stdio: stdout należy do protokołu JSON-RPC. Żadnych `print()` —
diagnostykę wypisuj na stderr (patrz `log` poniżej).
"""

import logging
import sys

import httpx
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
log = logging.getLogger("publiczne-api")

# Inicjalizacja serwera pod nazwą "PublicAPIs"
mcp = FastMCP("PublicAPIs")


# ==========================================================================
# TOOLS — czynności wywoływane przez model
# ==========================================================================

@mcp.tool()
def get_exchange_rate(currency_code: str) -> str:
    """Pobiera aktualny średni kurs podanej waluty (np. USD, EUR, CHF) w PLN z NBP."""
    url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency_code.upper()}/?format=json"
    try:
        response = httpx.get(url)
        response.raise_for_status()
        data = response.json()
        rate = data['rates'][0]['mid']
        date = data['rates'][0]['effectiveDate']
        return f"Kurs {currency_code.upper()} z dnia {date} wynosi: {rate} PLN"
    except Exception as e:
        return f"Błąd podczas pobierania kursu dla {currency_code}: {str(e)}"

@mcp.tool()
def get_pokemon_stats(pokemon_name: str) -> str:
    """Pobiera szczegółowe statystyki (wzrost, waga, typy) dla danego Pokemona (np. pikachu)."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    try:
        response = httpx.get(url)
        response.raise_for_status()
        data = response.json()
        weight = data['weight'] / 10  # waga w kg
        height = data['height'] / 10  # wzrost w metrach
        types = [t['type']['name'] for t in data['types']]
        return f"Pokemon {pokemon_name.capitalize()}: Wzrost {height}m, Waga {weight}kg, Typy: {', '.join(types)}"
    except Exception as e:
        return f"Nie znaleziono pokemona o nazwie {pokemon_name} lub wystąpił błąd: {str(e)}"

@mcp.tool()
def get_random_joke() -> str:
    """Pobiera losowy żart w języku angielskim."""
    url = "https://official-joke-api.appspot.com/random_joke"
    try:
        response = httpx.get(url)
        response.raise_for_status()
        data = response.json()
        return f"{data['setup']} ... {data['punchline']}"
    except Exception as e:
        return f"Błąd podczas pobierania żartu: {str(e)}"


@mcp.tool()
def get_rate_history(currency_code: str, days: int = 30) -> dict:
    """Pobiera historię kursu waluty z ostatnich N dni (max 255) wraz z min/max/średnią.

    Args:
        currency_code: Kod waluty, np. "USD", "EUR", "CHF".
        days: Liczba dni wstecz (1-255, domyślnie 30).

    Returns:
        dict: waluta, zakres dat, statystyki (min, max, średnia, zmiana %) i notowania.
    """
    days = max(1, min(days, 255))
    code = currency_code.upper()
    url = f"https://api.nbp.pl/api/exchangerates/rates/a/{code}/last/{days}/?format=json"
    try:
        response = httpx.get(url, timeout=20)
        response.raise_for_status()
        rates = response.json()["rates"]
    except Exception as e:
        return {"error": f"Nie udało się pobrać historii dla {code}: {e}"}

    values = [r["mid"] for r in rates]
    first, last = values[0], values[-1]
    return {
        "waluta": code,
        "od": rates[0]["effectiveDate"],
        "do": rates[-1]["effectiveDate"],
        "notowan": len(values),
        "min": min(values),
        "max": max(values),
        "srednia": round(sum(values) / len(values), 4),
        "zmiana_proc": round((last - first) / first * 100, 2),
        "notowania": [{"data": r["effectiveDate"], "kurs": r["mid"]} for r in rates],
    }


# ==========================================================================
# RESOURCES — kontekst adresowany przez URI (tylko odczyt)
# ==========================================================================

@mcp.resource("nbp://rates/table-a", title="Tabela A NBP", mime_type="application/json")
def resource_table_a() -> dict:
    """Pełna tabela A kursów średnich NBP — wszystkie waluty w jednym odczycie.

    To jest zasób, a nie narzędzie: nie ma efektów ubocznych, a użytkownik decyduje,
    czy wciągnąć te dane do kontekstu.
    """
    try:
        response = httpx.get("https://api.nbp.pl/api/exchangerates/tables/a/?format=json", timeout=20)
        response.raise_for_status()
        table = response.json()[0]
        return {
            "tabela": table["no"],
            "data": table["effectiveDate"],
            "kursy": {r["code"]: r["mid"] for r in table["rates"]},
        }
    except Exception as e:
        return {"error": f"Nie udało się pobrać tabeli A: {e}"}


@mcp.resource("nbp://rates/{currency_code}", title="Kurs waluty", mime_type="application/json")
def resource_rate(currency_code: str) -> dict:
    """Kurs pojedynczej waluty (resource template — parametr w URI, np. `nbp://rates/EUR`)."""
    code = currency_code.upper()
    try:
        response = httpx.get(
            f"https://api.nbp.pl/api/exchangerates/rates/a/{code}/?format=json", timeout=20
        )
        response.raise_for_status()
        rate = response.json()["rates"][0]
        return {"waluta": code, "data": rate["effectiveDate"], "kurs_pln": rate["mid"]}
    except Exception as e:
        return {"error": f"Nie udało się pobrać kursu {code}: {e}"}


@mcp.resource("api://catalog", title="Katalog API", mime_type="text/markdown")
def resource_catalog() -> str:
    """Ściąga: z jakich publicznych API korzysta ten serwer i gdzie są ich limity."""
    return """\
# Katalog publicznych API użytych w tym serwerze

| API | Endpoint | Klucz | Limity |
|---|---|---|---|
| NBP (kursy walut) | `https://api.nbp.pl/api/exchangerates/` | nie | tabela A publikowana w dni robocze ok. 12:00 |
| PokeAPI | `https://pokeapi.co/api/v2/` | nie | fair use, bez twardego limitu |
| Official Joke API | `https://official-joke-api.appspot.com/` | nie | bez gwarancji SLA |

## Pułapki

- NBP nie ma notowań w weekendy i święta — `last/N` zwraca N ostatnich **notowań**, nie dni.
- Kody walut są wielkimi literami (`usd` → 404).
- PokeAPI wymaga nazw małymi literami (`Pikachu` → 404).
"""


# ==========================================================================
# PROMPTS — gotowe przepływy uruchamiane przez użytkownika
# ==========================================================================

@mcp.prompt(title="Analiza kursu waluty")
def analiza_kursu(waluta: str, dni: str = "30") -> str:
    """Przepływ: pobierz historię kursu, policz trend i wyciągnij wniosek biznesowy."""
    return f"""\
Przeanalizuj kurs waluty **{waluta}** z ostatnich {dni} notowań.

1. Wywołaj `get_rate_history(currency_code="{waluta}", days={dni})`.
2. Porównaj z aktualnym kursem z zasobu `nbp://rates/{waluta.upper()}`.
3. Przedstaw:
   - **Trend** (wzrost/spadek/stabilny) wraz ze zmianą procentową,
   - **Zmienność** (rozstęp min-max względem średniej),
   - **Wniosek praktyczny** w dwóch zdaniach — dla kogoś, kto rozlicza fakturę w tej walucie.
4. Nie wypisuj wszystkich notowań — podaj tylko statystyki i 3 skrajne punkty.
"""


@mcp.prompt(title="Porównanie Pokemonów")
def porownaj_pokemony(pierwszy: str, drugi: str) -> str:
    """Przepływ pokazujący łączenie kilku wywołań narzędzia w jednej odpowiedzi."""
    return f"""\
Porównaj dwa Pokemony: **{pierwszy}** i **{drugi}**.

1. Wywołaj `get_pokemon_stats` osobno dla każdego z nich.
2. Zestaw wyniki w tabeli Markdown (wzrost, waga, typy).
3. Wskaż, który z nich ma przewagę w starciu i dlaczego — na podstawie typów.
4. Jeśli któregoś nie znaleziono, powiedz to wprost i zaproponuj poprawną nazwę.
"""


if __name__ == "__main__":
    # Uruchomienie serwera w trybie STDIO (wymagane przez klienty MCP)
    log.info("PublicAPIs MCP startuje (stdio)")
    mcp.run(transport='stdio')
