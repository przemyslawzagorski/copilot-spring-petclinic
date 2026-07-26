package org.springframework.samples.petclinic.owner;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;
import org.springframework.test.context.aot.DisabledInAotMode;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.hamcrest.Matchers.empty;
import static org.hamcrest.Matchers.greaterThan;
import static org.hamcrest.Matchers.hasItem;
import static org.hamcrest.Matchers.hasProperty;
import static org.hamcrest.Matchers.hasSize;
import static org.hamcrest.Matchers.is;
import static org.hamcrest.Matchers.not;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.flash;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.model;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.redirectedUrl;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.view;

/**
 * Testy integracyjne dla {@link OwnerController} z użyciem MockMvc i @WebMvcTest.
 * Weryfikują wszystkie endpointy kontrolera: tworzenie, wyszukiwanie, edycję i
 * wyświetlanie właścicieli.
 */
@WebMvcTest(OwnerController.class)
@DisabledInAotMode
class OwnerControllerMockMvcTest {

	private static final int TEST_OWNER_ID = 1;

	@Autowired
	private MockMvc mockMvc;

	@MockitoBean
	private OwnerRepository owners;

	private Owner georgeOwner() {
		Owner george = new Owner();
		george.setId(TEST_OWNER_ID);
		george.setFirstName("George");
		george.setLastName("Franklin");
		george.setAddress("110 W. Liberty St.");
		george.setCity("Madison");
		george.setTelephone("6085551023");

		Pet max = new Pet();
		PetType dog = new PetType();
		dog.setName("dog");
		max.setType(dog);
		max.setName("Max");
		max.setBirthDate(LocalDate.now());
		george.addPet(max);
		max.setId(1);

		Visit visit = new Visit();
		visit.setDate(LocalDate.now());
		max.getVisits().add(visit);

		return george;
	}

	@BeforeEach
	void setup() {
		Owner george = georgeOwner();
		given(this.owners.findById(TEST_OWNER_ID)).willReturn(Optional.of(george));
		given(this.owners.findByLastNameStartingWith(eq("Franklin"), any(Pageable.class)))
			.willReturn(new PageImpl<>(List.of(george)));
	}

	// --- GET /owners/new ---

	@Test
	void should_showCreationForm_when_getOwnersNew() throws Exception {
		mockMvc.perform(get("/owners/new"))
			.andExpect(status().isOk())
			.andExpect(model().attributeExists("owner"))
			.andExpect(view().name("owners/createOrUpdateOwnerForm"));
	}

	// --- POST /owners/new ---

	@Test
	void should_redirectAfterSave_when_postOwnerWithValidData() throws Exception {
		mockMvc
			.perform(post("/owners/new").param("firstName", "Anna")
				.param("lastName", "Kowalska")
				.param("address", "ul. Kwiatowa 5")
				.param("city", "Warszawa")
				.param("telephone", "1234567890"))
			.andExpect(status().is3xxRedirection());
	}

	@Test
	void should_returnFormWithErrors_when_postOwnerWithMissingAddress() throws Exception {
		mockMvc.perform(
				post("/owners/new").param("firstName", "Anna").param("lastName", "Kowalska").param("city", "Warszawa"))
			.andExpect(status().isOk())
			.andExpect(model().attributeHasErrors("owner"))
			.andExpect(model().attributeHasFieldErrors("owner", "address"))
			.andExpect(model().attributeHasFieldErrors("owner", "telephone"))
			.andExpect(view().name("owners/createOrUpdateOwnerForm"));
	}

	// --- GET /owners/find ---

	@Test
	void should_showFindForm_when_getOwnersFindPage() throws Exception {
		mockMvc.perform(get("/owners/find"))
			.andExpect(status().isOk())
			.andExpect(model().attributeExists("owner"))
			.andExpect(view().name("owners/findOwners"));
	}

	// --- GET /owners ---

	@Test
	void should_showOwnersList_when_multipleOwnersFound() throws Exception {
		Owner second = new Owner();
		second.setId(2);
		Page<Owner> page = new PageImpl<>(List.of(georgeOwner(), second));
		given(this.owners.findByLastNameStartingWith(anyString(), any(Pageable.class))).willReturn(page);

		mockMvc.perform(get("/owners").param("page", "1"))
			.andExpect(status().isOk())
			.andExpect(view().name("owners/ownersList"))
			.andExpect(model().attributeExists("listOwners"));
	}

	@Test
	void should_redirectToOwner_when_singleOwnerFoundByLastName() throws Exception {
		given(this.owners.findByLastNameStartingWith(eq("Franklin"), any(Pageable.class)))
			.willReturn(new PageImpl<>(List.of(georgeOwner())));

		mockMvc.perform(get("/owners").param("page", "1").param("lastName", "Franklin"))
			.andExpect(status().is3xxRedirection())
			.andExpect(view().name("redirect:/owners/" + TEST_OWNER_ID));
	}

	@Test
	void should_returnFindFormWithError_when_noOwnersFoundByLastName() throws Exception {
		given(this.owners.findByLastNameStartingWith(eq("Nieznajomy"), any(Pageable.class)))
			.willReturn(new PageImpl<>(List.of()));

		mockMvc.perform(get("/owners").param("page", "1").param("lastName", "Nieznajomy"))
			.andExpect(status().isOk())
			.andExpect(model().attributeHasFieldErrors("owner", "lastName"))
			.andExpect(model().attributeHasFieldErrorCode("owner", "lastName", "notFound"))
			.andExpect(view().name("owners/findOwners"));
	}

	@Test
	void should_returnOwnerSummary_when_aiSearchesByLastName() throws Exception {
		mockMvc.perform(get("/api/owners").param("lastName", "Franklin"))
			.andExpect(status().isOk())
			.andExpect(jsonPath("$[0].id").value(TEST_OWNER_ID))
			.andExpect(jsonPath("$[0].firstName").value("George"))
			.andExpect(jsonPath("$[0].lastName").value("Franklin"))
			.andExpect(jsonPath("$[0].pets[0].name").value("Max"))
			.andExpect(jsonPath("$[0].pets[0].visits[0].date").exists());
	}

	// --- GET /owners/{ownerId}/edit ---

	@Test
	void should_showEditForm_when_getOwnerEditPage() throws Exception {
		mockMvc.perform(get("/owners/{ownerId}/edit", TEST_OWNER_ID))
			.andExpect(status().isOk())
			.andExpect(model().attributeExists("owner"))
			.andExpect(model().attribute("owner", hasProperty("lastName", is("Franklin"))))
			.andExpect(model().attribute("owner", hasProperty("firstName", is("George"))))
			.andExpect(model().attribute("owner", hasProperty("address", is("110 W. Liberty St."))))
			.andExpect(model().attribute("owner", hasProperty("city", is("Madison"))))
			.andExpect(model().attribute("owner", hasProperty("telephone", is("6085551023"))))
			.andExpect(view().name("owners/createOrUpdateOwnerForm"));
	}

	// --- POST /owners/{ownerId}/edit ---

	@Test
	void should_redirectAfterUpdate_when_postOwnerEditWithValidData() throws Exception {
		mockMvc
			.perform(post("/owners/{ownerId}/edit", TEST_OWNER_ID).param("firstName", "George")
				.param("lastName", "Franklin")
				.param("address", "110 W. Liberty St.")
				.param("city", "Madison")
				.param("telephone", "6085551023"))
			.andExpect(status().is3xxRedirection())
			.andExpect(view().name("redirect:/owners/{ownerId}"));
	}

	@Test
	void should_returnFormWithErrors_when_postOwnerEditWithEmptyFields() throws Exception {
		mockMvc
			.perform(post("/owners/{ownerId}/edit", TEST_OWNER_ID).param("firstName", "George")
				.param("lastName", "Franklin")
				.param("address", "")
				.param("telephone", ""))
			.andExpect(status().isOk())
			.andExpect(model().attributeHasErrors("owner"))
			.andExpect(model().attributeHasFieldErrors("owner", "address"))
			.andExpect(model().attributeHasFieldErrors("owner", "telephone"))
			.andExpect(view().name("owners/createOrUpdateOwnerForm"));
	}

	@Test
	void should_redirectWithError_when_postOwnerEditWithIdMismatch() throws Exception {
		Owner ownerWithDifferentId = new Owner();
		ownerWithDifferentId.setId(99);
		ownerWithDifferentId.setFirstName("Jan");
		ownerWithDifferentId.setLastName("Nowak");
		ownerWithDifferentId.setAddress("ul. Polna 1");
		ownerWithDifferentId.setCity("Kraków");
		ownerWithDifferentId.setTelephone("9876543210");

		given(this.owners.findById(TEST_OWNER_ID)).willReturn(Optional.of(ownerWithDifferentId));

		mockMvc.perform(post("/owners/{ownerId}/edit", TEST_OWNER_ID).flashAttr("owner", ownerWithDifferentId))
			.andExpect(status().is3xxRedirection())
			.andExpect(redirectedUrl("/owners/" + TEST_OWNER_ID + "/edit"))
			.andExpect(flash().attributeExists("error"));
	}

	// --- GET /owners/{ownerId} ---

	@Test
	void should_showOwnerDetails_when_getOwnerById() throws Exception {
		mockMvc.perform(get("/owners/{ownerId}", TEST_OWNER_ID))
			.andExpect(status().isOk())
			.andExpect(model().attribute("owner", hasProperty("lastName", is("Franklin"))))
			.andExpect(model().attribute("owner", hasProperty("firstName", is("George"))))
			.andExpect(model().attribute("owner", hasProperty("address", is("110 W. Liberty St."))))
			.andExpect(model().attribute("owner", hasProperty("city", is("Madison"))))
			.andExpect(model().attribute("owner", hasProperty("telephone", is("6085551023"))))
			.andExpect(model().attribute("owner", hasProperty("pets", not(empty()))))
			.andExpect(model().attribute("owner",
					hasProperty("pets", hasItem(hasProperty("visits", hasSize(greaterThan(0)))))))
			.andExpect(view().name("owners/ownerDetails"));
	}

}
