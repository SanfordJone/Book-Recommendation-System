let searchInput = document.getElementById('search-input');
let autocompleteList = document.getElementById('autocomplete-list');

searchInput.addEventListener('input', function() {
	let search = this.value.trim();

	autocompleteList.innerHTML = '';

	if (search.length < 3) {
		return;
	}

	fetch('/autocomplete?search=' + search)
		.then(response => response.json())
		.then(results => {
			results.forEach(result => {
				let div = document.createElement('div');
				div.innerText = result;
				div.addEventListener('click', function() {
					searchInput.value = result;
					autocompleteList.innerHTML = '';
				});
				autocompleteList.appendChild(div);
			});
		});
});

document.addEventListener('click', function(event) {
	if (!searchInput.contains(event.target)) {
		autocompleteList.innerHTML = '';
	}
});
