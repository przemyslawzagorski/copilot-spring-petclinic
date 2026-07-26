/*
 * Copyright 2012-2025 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.springframework.samples.petclinic.model;

import java.io.Serializable;

import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.MappedSuperclass;

/**
 * Bazowa klasa domenowa stanowiąca fundament dla wszystkich encji persystentnych. Zawiera
 * pole identyfikatora (id) z automatycznym generowaniem wartości przez bazę danych. Klasa
 * ta powinna być dziedziczona przez wszystkie encje wymagające unikatowego klucza
 * głównego.
 *
 * @author Ken Krebs
 * @author Juergen Hoeller
 */
@MappedSuperclass
public class BaseEntity implements Serializable {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Integer id;

	/**
	 * Zwraca identyfikator encji.
	 * @return identyfikator lub {@code null}, jeśli encja nie została jeszcze zapisana
	 */
	public Integer getId() {
		return id;
	}

	/**
	 * Ustawia identyfikator encji.
	 * @param id identyfikator do ustawienia
	 */
	public void setId(Integer id) {
		this.id = id;
	}

	/**
	 * Sprawdza, czy encja jest nowa (nie ma jeszcze przypisanego identyfikatora).
	 * @return {@code true} jeśli identyfikator jest {@code null}, {@code false} w
	 * przeciwnym razie
	 */
	public boolean isNew() {
		return this.id == null;
	}

}
