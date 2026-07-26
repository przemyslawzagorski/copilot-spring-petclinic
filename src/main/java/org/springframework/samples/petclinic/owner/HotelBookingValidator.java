package org.springframework.samples.petclinic.owner;

import org.springframework.validation.Errors;
import org.springframework.validation.Validator;

/**
 * Waliduje formularz rezerwacji hotelu dla zwierzat.
 */
public class HotelBookingValidator implements Validator {

	private static final String REQUIRED = "required";

	private static final String INVALID_DATE_RANGE = "hotelBooking.dateRange.invalid";

	@Override
	public void validate(Object target, Errors errors) {
		HotelBooking hotelBooking = (HotelBooking) target;

		if (hotelBooking.getCheckInDate() == null) {
			errors.rejectValue("checkInDate", REQUIRED, REQUIRED);
		}

		if (hotelBooking.getCheckOutDate() == null) {
			errors.rejectValue("checkOutDate", REQUIRED, REQUIRED);
		}

		if (hotelBooking.getCheckInDate() != null && hotelBooking.getCheckOutDate() != null
				&& !hotelBooking.getCheckOutDate().isAfter(hotelBooking.getCheckInDate())) {
			errors.rejectValue("checkOutDate", INVALID_DATE_RANGE, INVALID_DATE_RANGE);
		}
	}

	@Override
	public boolean supports(Class<?> clazz) {
		return HotelBooking.class.isAssignableFrom(clazz);
	}

}