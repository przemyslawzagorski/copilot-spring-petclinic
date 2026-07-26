package org.springframework.samples.petclinic.owner;

import java.time.LocalDate;

import org.junit.jupiter.api.Test;
import org.springframework.validation.BeanPropertyBindingResult;
import org.springframework.validation.Errors;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Testy walidatora rezerwacji hotelu dla zwierzat.
 */
class HotelBookingValidatorTests {

	private final HotelBookingValidator validator = new HotelBookingValidator();

	@Test
	void should_acceptHotelBooking_whenDatesAreValid() {
		HotelBooking hotelBooking = new HotelBooking();
		hotelBooking.setCheckInDate(LocalDate.of(2026, 7, 10));
		hotelBooking.setCheckOutDate(LocalDate.of(2026, 7, 14));
		Errors errors = new BeanPropertyBindingResult(hotelBooking, "hotelBooking");

		this.validator.validate(hotelBooking, errors);

		assertThat(errors.hasErrors()).isFalse();
	}

	@Test
	void should_rejectHotelBooking_whenDatesAreMissing() {
		HotelBooking hotelBooking = new HotelBooking();
		Errors errors = new BeanPropertyBindingResult(hotelBooking, "hotelBooking");

		this.validator.validate(hotelBooking, errors);

		assertThat(errors.getFieldError("checkInDate").getCode()).isEqualTo("required");
		assertThat(errors.getFieldError("checkOutDate").getCode()).isEqualTo("required");
	}

	@Test
	void should_rejectHotelBooking_whenCheckOutDateIsNotAfterCheckInDate() {
		HotelBooking hotelBooking = new HotelBooking();
		hotelBooking.setCheckInDate(LocalDate.of(2026, 7, 10));
		hotelBooking.setCheckOutDate(LocalDate.of(2026, 7, 10));
		Errors errors = new BeanPropertyBindingResult(hotelBooking, "hotelBooking");

		this.validator.validate(hotelBooking, errors);

		assertThat(errors.getFieldError("checkOutDate").getCode()).isEqualTo("hotelBooking.dateRange.invalid");
	}

}