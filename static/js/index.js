

        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
            } else {
                console.log("Geolocation is not supported by this browser.");
            }
        }


             function successCallback(position) {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;

                console.log("Latitude: " + latitude);
                console.log("Longitude: " + longitude);
                var inputLat = document.getElementById('lat');
                var inputLong = document.getElementById('long');
                inputLat.value = latitude;
                inputLong.value = longitude;

                 // Create a map with the location marker
                /*var user_location = 'toi';
                var map = L.map('map', {
                  dragging: true // Enable dragging
                }).setView([latitude, longitude], 13);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                  attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors',
                  maxZoom: 18,
                }).addTo(map);
                map.dragging.enable();
                L.marker([latitude, longitude]).addTo(map).bindPopup(user_location).openPopup();*/
                var inputElement = document.getElementById('localisation');

                  // Update the placeholder attribute
                  inputElement.textContent = "Votre cordonné sont : "+latitude+" , "+ longitude;



        }

        function errorCallback(error) {
            alert('there is an error');
            console.log("Error occurred while getting the location: " + error.message);
        }

        var previousSelected = null;
        function handleDayClick(button) {
             if (previousSelected) {
                    previousSelected.classList.remove("selected");
                }

            button.classList.add("selected");
            previousSelected = button;
            var selectedDay = button.textContent;
            console.log("Selected day: " + selectedDay);
            // Do something with the selected day value
            var year_month= document.getElementById('year_month');



            var date_complet=selectedDay+"-"+year_month.getAttribute('date');

            var input_date = document.getElementById('date');
            var ville_input = document.getElementById('ville');
            var selected_ville= document.getElementById('search_city_id').value;

            input_date.value = date_complet;
            var button_heure = document.getElementById('select_time').value;


            ville_input.value=selected_ville;


        }

