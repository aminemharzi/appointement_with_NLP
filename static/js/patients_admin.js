var searchInput = document.getElementById('searchInput');
var list = document.getElementById('myList').getElementsByTagName('li');
var selectedItem = document.getElementById('selectedItem');


searchInput.addEventListener('input', function() {
  var searchValue = searchInput.value.toLowerCase();

  for (var i = 0; i < list.length; i++) {
    var text = list[i].textContent.toLowerCase();

    if (text.includes(searchValue)) {
      list[i].style.display = 'flex';
    } else {
      list[i].style.display = 'none';
    }
  }
});