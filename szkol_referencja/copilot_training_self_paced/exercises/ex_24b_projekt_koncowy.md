# Ex 24b: Projekt końcowy — połącz wszystko

> Bonus · ~30 min · Po ex_24 (finał szkolenia)

**Po co:** Jeden duży scenariusz, który łączy: prompting, testy, customizację, agenty i MCP. Budujesz feature od A do Z używając wszystkiego, czego się nauczyłeś.

## Zadanie

**Feature:** Dodaj moduł "Appointment" (wizyty) do spring-petclinic.

### Faza A: Planowanie (5 min)

W Copilot Chat (agent mode) wpisz:

```
Zaplanuj dodanie nowego modułu Appointment do spring-petclinic. Appointment ma: id, date (LocalDate), description (String), pet (relacja do Pet), vet (relacja do Vet).
Potrzebuję: encja, repozytorium, kontroler z CRUD, widoki Thymeleaf, testy.
Pokaż plan: tabela z plikami do utworzenia, kolejność, zależności.
```

### Faza B: TDD (8 min)

1. Napisz NAJPIERW test (Red):
```
Wygeneruj test dla AppointmentRepository.findByPetId(Integer petId). Test musi FAILOWAĆ — klasy jeszcze nie istnieją.
```

2. Implementacja (Green):
```
Na podstawie testu utwórz: Appointment.java (encja), AppointmentRepository.java. Minimalna implementacja żeby test przeszedł.
```

3. Uruchom: `.\mvnw.cmd test -Dtest=AppointmentRepositoryTest`

### Faza C: Kontroler z agentem reviewer (8 min)

1. Wygeneruj kontroler:
```
Utwórz AppointmentController z endpointami: GET /appointments (lista), GET /appointments/new (formularz), POST /appointments (zapis). Wzoruj się na OwnerController.
```

2. Wybierz agenta `reviewer` w pickerze:
```
Zrób review AppointmentController.java
```

3. Zastosuj poprawki z review.

### Faza D: Dokumentacja (4 min)

```
Wygeneruj:
1. Diagram Mermaid (classDiagram) z Appointment i relacjami do Pet/Vet
2. Javadoc dla AppointmentController
3. Zaktualizuj README: dodaj sekcję o module Appointment
```

### Faza E: Kompilacja i weryfikacja (5 min)

```
.\mvnw.cmd compile
.\mvnw.cmd test
```

Jeśli błędy — użyj self-correction loop (powiedz agentowi o błędach).

## Checklist ukończenia

- [ ] Encja Appointment z relacjami
- [ ] Repozytorium z custom query
- [ ] Kontroler z CRUD
- [ ] Minimum 3 testy (przechodzą)
- [ ] Code review poprawiony
- [ ] Diagram Mermaid
- [ ] Kompilacja bez błędów

**Brawo! Przeszedłeś pełen cykl — od planu przez TDD, agenta, review, po dokumentację. To jest workflow, który zabierasz do zespołu.**
