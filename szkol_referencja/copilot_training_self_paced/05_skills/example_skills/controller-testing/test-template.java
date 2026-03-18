package com.example;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

// TODO: Zmień na właściwy kontroler i serwis
@WebMvcTest(/* TODO: NazwaController.class */)
class NazwaControllerTest {

	@Autowired
	private MockMvc mockMvc;

	// TODO: Dodaj @MockBean dla każdej zależności kontrolera
	// @MockBean
	// private NazwaService nazwaService;

	@BeforeEach
	void setup() {
		// TODO: Skonfiguruj mocki (when...thenReturn)
	}

	@Test
	void shouldReturnOkForGetEndpoint() throws Exception {
		// TODO: mockMvc.perform(get("/sciezka"))
		//   .andExpect(status().isOk())
		//   .andExpect(model().attributeExists("atrybut"))
		//   .andExpect(view().name("nazwaWidoku"));
	}

	@Test
	void shouldValidatePostData() throws Exception {
		// TODO: mockMvc.perform(post("/sciezka")
		//   .param("pole", ""))
		//   .andExpect(model().hasErrors());
	}

}
