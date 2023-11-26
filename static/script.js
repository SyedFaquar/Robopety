attachLisener();

function attachLisener() {
  var petSelectBtns = document.querySelectorAll('button[id*="select"]'); 
  petSelectBtns.forEach(function(button){
    button.addEventListener('click', function(){
      var ids = button.id.split('-');
      pet_name = ids[2];
      if(ids.length>3){
        pet_name = ids.slice(2).join('-');
      }
      fetch(`/setpet`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
      },
        body: `data_from_button=${pet_name}`
      })
        .then(response => response.text())
        .then(data => {
          document.body.innerHTML = data;
          attachLisener() 
        }).catch(error => console.error('Error: ', error)); 
    });
  })
  
  var filterField = document.getElementById('search-field');
  
  filterField.addEventListener('input', (event)=>{
    event.preventDefault();
    filterPetList(event.target.value);
  });

  var returnBtn = document.getElementById('btn-return');
  returnBtn?.addEventListener('click', function(){ returnPet()});
}

function returnPet(){
  fetch(`/returnpet`)
    .then(response => response.text())
    .then(data => {
      document.body.innerHTML = data;
      attachLisener();
    })
    .catch(error => console.error('Error: ', error));
}

function filterPetList(filterValue) {
  if (filterValue == '') filterValue = 'None';
  console.log(filterValue);
  fetch(`/filtered/${filterValue}`)
      .then(response => response.json())
      .then(data => {
          var filteredList = document.getElementById('filtered-list');
          filteredList.innerHTML = '';
          data.filtered_list.forEach(function(item) {
            var li = document.createElement('li');
            var div = document.createElement('div');
            var img = document.createElement('img');
            var p = document.createElement('p');
            filteredList.appendChild(li);
            li.appendChild(div);
            div.appendChild(img);
            div.appendChild(p);
            div.setAttribute('class', 'robopet');
            img.setAttribute('src', item.image);
            img.setAttribute('alt', 'RoboPet');
            img.setAttribute('width', '75px');
            img.setAttribute('height', '75px');
            p.innerText = item.name;
            if(!data.currentPet){
              var button = document.createElement('button');
              div.appendChild(button);
              button.innerText = 'Select';
              button.setAttribute('id', 'btn-select-'+item.name);
              button.addEventListener('click', function(){
                var ids = button.id.split('-');
                pet_name = ids[2];
                fetch(`/setpet`, {
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                  body: `data_from_button=${item.name}`
                })
                  .then(response => response.text())
                  .then(data => {
                    document.body.innerHTML = data;
                    attachLisener() 
                  }).catch(error => console.error('Error: ', error)); 
              });
            }
          });
      })
      .catch(error => console.error('Error: ', error));

}