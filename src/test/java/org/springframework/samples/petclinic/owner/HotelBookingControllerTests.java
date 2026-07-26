package org.springframework.samples.petclinic.owner;

import java.util.Optional;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.condition.DisabledInNativeImage;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.test.context.aot.DisabledInAotMode;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.verify;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.model;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.view;

/**
 * Testy kontrolera rezerwacji hotelu dla zwierzat.
 */
@WebMvcTest(HotelBookingController.class)
@DisabledInNativeImage
@DisabledInAotMode
class HotelBookingControllerTests {

	private static final int TEST_OWNER_ID = 1;

	private static final int TEST_PET_ID = 1;

	@Autowired
	private MockMvc mockMvc;

	@MockitoBean
	private OwnerRepository owners;

	@BeforeEach
	void setup() {
		Owner owner = new Owner();
		Pet pet = new Pet();
		owner.addPet(pet);
		pet.setId(TEST_PET_ID);
		given(this.owners.findById(TEST_OWNER_ID)).willReturn(Optional.of(owner));
	}

	@Test
	void should_showHotelBookingForm_whenCreatingNewBooking() throws Exception {
		this.mockMvc.perform(get("/owners/{ownerId}/pets/{petId}/hotel-bookings/new", TEST_OWNER_ID, TEST_PET_ID))
			.andExpect(status().isOk())
			.andExpect(model().attributeExists("hotelBooking"))
			.andExpect(view().name("pets/createOrUpdateHotelBookingForm"));
	}

	@Test
	void should_redirectToOwnerDetails_whenHotelBookingIsValid() throws Exception {
		this.mockMvc
			.perform(post("/owners/{ownerId}/pets/{petId}/hotel-bookings/new", TEST_OWNER_ID, TEST_PET_ID)
				.param("checkInDate", "2026-07-10")
				.param("checkOutDate", "2026-07-14")
				.param("notes", "Needs morning medication"))
			.andExpect(status().is3xxRedirection())
			.andExpect(view().name("redirect:/owners/{ownerId}"));

		verify(this.owners).save(any(Owner.class));
	}

	@Test
	void should_returnFormWithErrors_whenRequiredDatesAreMissing() throws Exception {
		this.mockMvc
			.perform(post("/owners/{ownerId}/pets/{petId}/hotel-bookings/new", TEST_OWNER_ID, TEST_PET_ID)
				.param("notes", "Needs morning medication"))
			.andExpect(model().attributeHasErrors("hotelBooking"))
			.andExpect(model().attributeHasFieldErrors("hotelBooking", "checkInDate", "checkOutDate"))
			.andExpect(status().isOk())
			.andExpect(view().name("pets/createOrUpdateHotelBookingForm"));
	}

	@Test
	void should_returnFormWithErrors_whenCheckOutDateIsNotAfterCheckInDate() throws Exception {
		this.mockMvc
			.perform(post("/owners/{ownerId}/pets/{petId}/hotel-bookings/new", TEST_OWNER_ID, TEST_PET_ID)
				.param("checkInDate", "2026-07-10")
				.param("checkOutDate", "2026-07-10"))
			.andExpect(model().attributeHasErrors("hotelBooking"))
			.andExpect(model().attributeHasFieldErrorCode("hotelBooking", "checkOutDate",
					"hotelBooking.dateRange.invalid"))
			.andExpect(status().isOk())
			.andExpect(view().name("pets/createOrUpdateHotelBookingForm"));
	}

}