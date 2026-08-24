package org.springframework.samples.petclinic.owner;

import java.util.Map;
import java.util.Optional;

import org.springframework.stereotype.Controller;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.WebDataBinder;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.InitBinder;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import jakarta.validation.Valid;

/**
 * Obsluguje formularze rezerwacji hotelu dla zwierzat.
 */
@Controller
class HotelBookingController {

	private final OwnerRepository owners;

	HotelBookingController(OwnerRepository owners) {
		this.owners = owners;
	}

	@InitBinder("hotelBooking")
	public void initHotelBookingBinder(WebDataBinder dataBinder) {
		dataBinder.setDisallowedFields("id", "pet");
		dataBinder.addValidators(new HotelBookingValidator());
	}

	@ModelAttribute("hotelBooking")
	public HotelBooking loadPetWithHotelBooking(@PathVariable("ownerId") int ownerId, @PathVariable("petId") int petId,
			Map<String, Object> model) {
		Optional<Owner> optionalOwner = this.owners.findById(ownerId);
		Owner owner = optionalOwner.orElseThrow(() -> new IllegalArgumentException(
				"Owner not found with id: " + ownerId + ". Please ensure the ID is correct "));

		Pet pet = owner.getPet(petId);
		if (pet == null) {
			throw new IllegalArgumentException(
					"Pet with id " + petId + " not found for owner with id " + ownerId + ".");
		}

		model.put("pet", pet);
		model.put("owner", owner);

		HotelBooking hotelBooking = new HotelBooking();
		pet.addHotelBooking(hotelBooking);
		return hotelBooking;
	}

	@GetMapping("/owners/{ownerId}/pets/{petId}/hotel-bookings/new")
	public String initNewHotelBookingForm() {
		return "pets/createOrUpdateHotelBookingForm";
	}

	int getHotelBookingCountForPet(Pet pet) {
		return pet.getHotelBookings().size();
	}

	int getHotelBookingCountForOwner(Owner owner) {
		return owner.getPets().stream().mapToInt(this::getHotelBookingCountForPet).sum();
	}

	@PostMapping("/owners/{ownerId}/pets/{petId}/hotel-bookings/new")
	public String processNewHotelBookingForm(@ModelAttribute Owner owner, @PathVariable int petId,
			@Valid HotelBooking hotelBooking, BindingResult result, RedirectAttributes redirectAttributes) {
		if (result.hasErrors()) {
			return "pets/createOrUpdateHotelBookingForm";
		}

		owner.addHotelBooking(petId, hotelBooking);
		this.owners.save(owner);
		redirectAttributes.addFlashAttribute("message", "Your hotel booking has been created");
		return "redirect:/owners/{ownerId}";
	}

}