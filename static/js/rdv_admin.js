function handleDayClick(element, patients) {


     var patientNamesElement = document.getElementById('patientName');
     //var  temps document.getElementById('time').textContent ;
     patientNamesElement.innerHTML = '';
     if (patients.length > 0) {
        // Process the appointments data
        for (var i = 0; i < patients.length; i++) {
            var appointment = patients[i];
            var patientName = appointment.patient_name;
            var time = appointment.temps;
            // Do something with the appointment data
            console.log("Patient Name: " + patientName);
            console.log("Time: " + time);
            var patientName = patients[i].patient_name;
          // Create a new <p> element for each patient name and append it to the parent <p> tag
             var pElement = document.createElement('p');
             var tElement =document.createElement('p');
              pElement.textContent = patientName;
              tElement.textContent = time;
              patientNamesElement.appendChild(pElement);
              patientNamesElement.appendChild(tElement);
        }
    }


  // Get the day value from the clicked element
  var day = element.textContent;


  // Check if the clicked day has a rendez-vous
  var hasRendezvous = element.dataset.hasRendezvous;

  if (hasRendezvous === 'true') {
    // Retrieve the rendez-vous details using AJAX or other means
    // In this example, we assume the rendez-vous details are stored in a JavaScript object

  }



    $('#rendezvousModal').show();
    // Show the modal
    $('.close').on('click', function() {

    $('#rendezvousModal').hide();
        });
}

