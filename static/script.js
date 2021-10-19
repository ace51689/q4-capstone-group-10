document.getElementById('page-title').innerHTML=document.title;
feather.replace();
if (location.search.includes('song_link')) {
	document.querySelector('#create-post #id_body').value = new URLSearchParams(location.search).get('song_link') + '\n'
}

element = document.querySelectorAll('.post-body > p');
if (element.length > 0) {
	element.forEach(e => {
		song_uri = e.innerHTML.match(/(\w*:\w*:\w*)/g);
		if (song_uri) {
			e.innerHTML = e.innerHTML.replace(song_uri, `<a href="https://open.spotify.com/embed/${song_uri[0].split(':').slice(1).join('/')}" target="_blank">${song_uri}</a>`)
		}
	})
}

search_form = document.getElementById('query-search-bar');
if (search_form) {
	search_form.addEventListener('submit', e => {
		e.preventDefault()
		location.assign(`?query=${document.querySelector('#query-search-bar > input').value}`)
	});
}
