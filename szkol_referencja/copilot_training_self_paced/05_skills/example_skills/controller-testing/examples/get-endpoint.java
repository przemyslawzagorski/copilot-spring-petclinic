// Przykład testu GET endpoint z MockMvc
// Użyj jako wzorzec w SKILL controller-testing

@Test
void shouldShowOwnerDetails() throws Exception {
    Owner owner = new Owner();
    owner.setId(1);
    owner.setFirstName("Jan");
    owner.setLastName("Kowalski");

    when(ownerService.findById(1)).thenReturn(owner);

    mockMvc.perform(get("/owners/{ownerId}", 1))
        .andExpect(status().isOk())
        .andExpect(model().attribute("owner", hasProperty("firstName", is("Jan"))))
        .andExpect(view().name("owners/ownerDetails"));
}
