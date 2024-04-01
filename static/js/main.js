/**
* Template Name: Siimple
* Updated: Mar 10 2024 with Bootstrap v5.3.3
* Template URL: https://bootstrapmade.com/free-bootstrap-landing-page/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/
(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    let selectEl = select(el, all)
    if (selectEl) {
      if (all) {
        selectEl.forEach(e => e.addEventListener(type, listener))
      } else {
        selectEl.addEventListener(type, listener)
      }
    }
  }

  /**
   * Mobile nav toggle
   */
  const toogleNav = function() {
    let navButton = select('.nav-toggle')
    navButton.classList.toggle('nav-toggle-active')
    navButton.querySelector('i').classList.toggle('bx-x')
    navButton.querySelector('i').classList.toggle('bx-menu')

    select('.nav-menu').classList.toggle('nav-menu-active')
  }
  on('click', '.nav-toggle', function(e) {
    toogleNav();
  })

  /**
   * Mobile nav dropdowns activate
   */
  on('click', '.nav-menu .drop-down > a', function(e) {
    e.preventDefault()
    this.nextElementSibling.classList.toggle('drop-down-active')
    this.parentElement.classList.toggle('active')
  }, true)

  /**
   * Scrool links with a class name .scrollto
   */
  on('click', '.scrollto', function(e) {
    if (select(this.hash)) {
      select('.nav-menu .active').classList.remove('active')
      this.parentElement.classList.toggle('active')
      toogleNav();
    }
  }, true)

})()

/* Updated! */
// Display driving time only when car is selected
document.addEventListener('DOMContentLoaded', function() {
  var travelMethodSelect = document.getElementById('travel_method');
  var drivingTimeField = document.querySelector('.form-driving');

  // Check the initial value of the travel method select element
  if (travelMethodSelect.value === 'Car') {
    drivingTimeField.style.display = 'block';
  }

  // Add event listener to listen for changes in travel method
  travelMethodSelect.addEventListener('change', function() {
    if (this.value === 'Car') {
      drivingTimeField.style.display = 'block';
    } else {
      drivingTimeField.style.display = 'none';
    }
  });
});

// Add and remove departure cities, Error in autocomplete!
document.addEventListener('DOMContentLoaded', function() {
  var departureCityCount = 1;
  var maxDepartureCities = 4; // Maximum number of departure cities allowed

  function createDepartureCity() {
      departureCityCount++;
      var newDepartureCity = document.createElement('div');
      newDepartureCity.classList.add('form-group');
      newDepartureCity.classList.add('form-departure' + departureCityCount);
      newDepartureCity.innerHTML = `
          <div class="departure-city-field">
              <input type="text" name="departure${departureCityCount}" class="form-control" id="autocompleteDatalist${departureCityCount}" data-datalist="departure-city" placeholder="Departure City ${departureCityCount}" />
              <datalist id="departure-city${departureCityCount}">
                  {% for city in departure_list %}
                  <option>{{city}}</option>
                  {% endfor %}
              </datalist>
          </div>
      `;
      document.getElementById('additional-departure-cities').appendChild(newDepartureCity);
  }

  document.getElementById('add-departure-city').addEventListener('click', function() {
      if (departureCityCount < maxDepartureCities) {
          createDepartureCity();
      } else {
          alert('You can only add up to ' + maxDepartureCities + ' departure cities.');
      }
  });

  document.getElementById('remove-departure-city').addEventListener('click', function() {
      var additionalDepartureCities = document.getElementById('additional-departure-cities');
      if (departureCityCount > 1) {
          departureCityCount--;
          additionalDepartureCities.removeChild(additionalDepartureCities.lastChild);
      }
  });
});
