# Diagram zależności warunków i parametrów

```mermaid
flowchart LR
    subgraph INPUT["Parametry wejściowe"]
      P1["owner.lastName"]
      P2["page"]
      P3["owner.id"]
      P4["ownerId (z URL)"]
      P5["pet.name"]
      P6["pet.id"]
      P7["pet.isNew"]
      P8["pet.birthDate"]
      P9["result.hasErrors()"]
    end

    subgraph CONDITIONS["Warunki / bramki"]
      C1["total == 0"]
      C2["total == 1"]
      C3["owner.id != ownerId"]
      C4["duplikat nazwy:
name && isNew && owner.getPet(name,true)!=null"]
      C5["duplikat przy edycji:
existingPet!=null && existingPet.id != pet.id"]
      C6["birthDate > today"]
      C7["result.hasErrors()"]
    end

    subgraph OUTCOMES["Efekty"]
      O1["rejectValue(lastName, notFound)"]
      O2["redirect /owners/{id}"]
      O3["lista z paginacją"]
      O4["rejectValue(id, mismatch) + redirect edit"]
      O5["rejectValue(name, duplicate)"]
      O6["rejectValue(birthDate, typeMismatch.birthDate)"]
      O7["powrót do formularza"]
      O8["save(...) + flash success + redirect details"]
    end

    %% Find owners
    P1 --> C1
    P2 --> C1
    P1 --> C2
    P2 --> C2
    C1 --> O1
    C2 --> O2
    C1 -. "nie" .-> C2
    C2 -. "nie" .-> O3

    %% Owner update
    P3 --> C3
    P4 --> C3
    C3 --> O4
    C3 -. "nie" .-> O8

    %% Pet create/update
    P5 --> C4
    P7 --> C4
    C4 --> O5

    P5 --> C5
    P6 --> C5
    C5 --> O5

    P8 --> C6
    C6 --> O6

    P9 --> C7
    O5 --> C7
    O6 --> C7

    C7 --> O7
    C7 -. "nie" .-> O8
  ```