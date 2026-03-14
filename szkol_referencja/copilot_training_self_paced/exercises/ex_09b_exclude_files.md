# Ex 09b: Exclude files — ochrona wrażliwego kodu

> Bonus · ~5 min · Między ex_09 a ex_10

**Po co:** Niektóre pliki NIE powinny trafiać do Copilota: sekrety, credentials, klucze API. Plik `.copilotignore` blokuje ich indeksowanie.

## Co zrobić

### Krok 1: Utwórz .copilotignore

Utwórz plik `.copilotignore` w katalogu głównym:

```
# Sekrety i konfiguracja wrażliwa
.env
**/secrets/**
**/credentials/**
application-prod.properties

# Vendor / wygenerowany kod
target/
node_modules/
*.min.js
```

### Krok 2: Przetestuj

1. Utwórz plik `secrets/api-keys.txt` z treścią `FAKE_KEY=abc123` (to testowy plik)
2. W Copilot Chat wpisz:

```
@workspace Pokaż zawartość pliku secrets/api-keys.txt
```

3. Copilot NIE powinien mieć dostępu do tego pliku.

### Krok 3: Sprawdź w ustawieniach VS Code

Otwórz Settings (Ctrl+,) i wyszukaj `github.copilot`. Znajdź opcje:
- `github.copilot.advanced` → `excludeFiles` — lista wzorców wykluczeń

**Spodziewany wynik:** Pliki z `.copilotignore` nie są widoczne dla Copilota w @workspace.

**Tip:** Wrzuć `.copilotignore` do repo — cały zespół będzie chroniony. Dodaj go też do `.gitignore` jeśli sam zawiera wrażliwe wzorce.
