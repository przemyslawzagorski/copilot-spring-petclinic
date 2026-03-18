// Przykład testu POST z walidacją
// Użyj jako wzorzec w SKILL controller-testing

@Test
void shouldRejectEmptyOwnerName() throws Exception {
    mockMvc.perform(post("/owners/new")
            .param("firstName", "")
            .param("lastName", "")
            .param("address", "")
            .param("city", "")
            .param("telephone", ""))
        .andExpect(status().isOk())
        .andExpect(model().hasErrors())
        .andExpect(view().name("owners/createOrUpdateOwnerForm"));
}

@Test
void shouldCreateOwnerSuccessfully() throws Exception {
    mockMvc.perform(post("/owners/new")
            .param("firstName", "Anna")
            .param("lastName", "Nowak")
            .param("address", "ul. Testowa 1")
            .param("city", "Warszawa")
            .param("telephone", "123456789"))
        .andExpect(status().is3xxRedirection());
}
