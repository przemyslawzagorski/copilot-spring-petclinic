---
name: java-conventions
description: "Konwencje Java używane w tym projekcie: nazewnictwo, formatowanie, wzorce. Użyj gdy piszesz lub reviewujesz kod Java."
user-invocable: false
---

# Konwencje Java w PetClinic

- Pakiety: lowercase, bez underscore
- Klasy: PascalCase
- Metody/pola: camelCase
- Testy: `should_{co}_{kiedy}` (konwencja projektu) lub `{Klasa}Test`
- Spring: constructor injection (nie @Autowired na polach)
- Walidacja: @Valid na kontrolerze, nie w serwisie
- Records zamiast POJO tam gdzie brak mutacji
- Javadoc po polsku dla klas publicznych
