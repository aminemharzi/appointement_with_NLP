var searchInput = document.getElementById('searchInput');
var list = document.getElementById('myList').getElementsByTagName('li');
var selectedItem = document.getElementById('selectedItem');

const currentDate = new Date();
const year = currentDate.getFullYear();
searchInput.addEventListener('input', function() {
  var searchValue = searchInput.value.toLowerCase();

  for (var i = 0; i < list.length; i++) {
    var text = list[i].textContent.toLowerCase();

    if (text.includes(searchValue)) {
      list[i].style.display = 'block';
    } else {
      list[i].style.display = 'none';
    }
  }
});

for (var i = 0; i < list.length; i++) {
  list[i].addEventListener('click', function() {
    var selectedText = this.textContent;


    // Remove 'selected' class from previously selected item
    var prevSelected = document.querySelector('.selected');
    if (prevSelected) {
      prevSelected.classList.remove('selected');
    }

    // Add 'selected' class to the clicked item
    this.classList.add('selected');
  });
}

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

// Function to create the bar graph
/*function createBarGraph(data) {
        var ctx = document.getElementById('appointmentChart').getContext('2d');
        var labels = data.map(function(item) {

            return item[0]['day'];
        });
        var values = data.map(function(item) {
            console.log(item[0])
            return item[0]['appointments'];
        });

        var chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Appointments per Month',
                    data: values,
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        precision: 0
                    }
                }
            }
        });
    }

    // Retrieve the appointment data and create the bar graph
  $.ajax({
        url: '/appointments_data',
        type: 'GET',
        success: function(data) {
            createBarGraph(data);
        }
  });*/

    // Retrieve the appointment data and create the bar graph


/*
function createBarGraph(weekData, month, year) {
  var ctx = document.getElementById('appointmentChart').getContext('2d');

  var labels = weekData.map(function (item) {
   return item[0];
  });
  var values = weekData.map(function (item) {
    console.log(item['appointments'])
    return item[1];
  });
  var nextButton= document.getElementById('nextButton');
  var previousButton= document.getElementById('previousButton');
   const currentDate = new Date();

    // Get the next month
    const nextMonth = new Date(currentDate.getFullYear(), month + 1);
    const nextMonthNumber = nextMonth.getMonth() +1; // Months are zero-based, so we add 1

    // Get the previous month
    console.log(month);
    alert(month);
    const previousMonth = new Date(currentDate.getFullYear(), month - 1);
    const previousMonthNumber = previousMonth.getMonth() ; // Months are zero-based, so we add 1

 // Output: Next month number (e.g., 6 for June)
    nextButton.textContent=nextMonthNumber;

    previousButton.textContent=previousMonthNumber;

  var chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Appointments per Week',
        data: values,
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          precision: 0
        }
      }
    }
  });
}

$(document).ready(function () {
  var weeksData = []; // Array to store all the week data
  var currentWeekIndex = 0; // Index of the current week being displayed

  // Function to update the bar graph with the current week data
  function updateBarGraph(month) {
    const year = currentDate.getFullYear();
   $.ajax({
    url: '/appointments_data?month='+month+'&year='+year,
    type: 'GET',
    success: function (response) {

     createBarGraph(response,month,year );
      console.log(weeksData)
    },
    error: function (error) {
      console.log(error);
    }
  });
    var currentWeekData = weeksData[currentWeekIndex];
    createBarGraph(currentWeekData);
  }

  // Function to handle the previous week button click
  $('#previousButton').on('click', function () {
    var previousButton= document.getElementById('previousButton');
    updateBarGraph(previousButton.textContent);
  });

  // Function to handle the next week button click
  $('#nextButton').on('click', function () {
    var nextButton= document.getElementById('nextButton');
    updateBarGraph(nextButton.textContent);
  });

  // Fetch the data for 'weeks' variable using AJAX
const currentDate = new Date();
const year = currentDate.getFullYear();
const month = currentDate.getMonth() + 1; // Months are zero-based, so we add 1
const day = currentDate.getDate();
const formattedDate = `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;

  $.ajax({
    url: '/appointments_data?month='+month+'&year='+year,
    type: 'GET',
    success: function (response) {

     createBarGraph(response,month, year );
      console.log(weeksData)
    },
    error: function (error) {
      console.log(error);
    }
  });
});*/

var nextButton= document.getElementById('nextButton');
var previousButton= document.getElementById('previousButton');
var canvas = document.getElementById('appointmentChart');
var ctx = canvas.getContext('2d');
var existingChart = window.appointmentChart;
function clearCanvas() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

    var myChart = new Chart(ctx);
    myChart.destroy();

}

// Call the clearCanvas function whenever you want to remove the previous graph



function createBarGraph(data) {
    let chartStatus = Chart.getChart("appointmentChart"); // <canvas> id
    if (chartStatus != undefined) {
      chartStatus.destroy();
    }


  weekData=data['data']


  var labels = weekData.map(function (item) {
    return item[0];
  });
  var values = weekData.map(function (item) {
    return item[1];
  });

  window.appointmentChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'les rendez-vous par jour dans le mois '+data['month']+' en '+ data['year'],
        data: values,
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          precision: 0
        }
      }
    }
  });
}

$(document).ready(function () {
  var currentMonth; // Variable to store the current month
  var currentYear; // Variable to store the current year

  // Function to update the bar graph with the specified month and year
  function updateBarGraph(month, year) {
    $.ajax({
      url: '/appointments_data?month=' + month + '&year=' + year,
      type: 'GET',
      success: function (response) {
        createBarGraph(response);
        /*
        nextButton.textContent=response['next_month']
        previousButton.textContent=response['previous_month']*/
        nextButton.className = response['next_month'];
        previousButton.className=response['previous_month']
        nextButton.setAttribute('year', response['year']);
        previousButton.setAttribute('year', response['year']);
      },
      error: function (error) {
        console.log(error);
      }
    });
  }

  // Function to handle the previous month button click
  $('#previousButton').on('click', function () {


    updateBarGraph(previousButton.className,2023);
  });

  // Function to handle the next month button click
  $('#nextButton').on('click', function () {

    updateBarGraph(nextButton.className, 2023);
  });

  // Fetch the current month and year
  const currentDate = new Date();
  currentMonth = currentDate.getMonth() + 1; // Months are zero-based, so we add 1
  currentYear = currentDate.getFullYear();

  // Update the bar graph with the current month and year
  updateBarGraph(currentMonth, currentYear);
});


