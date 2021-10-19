document.getElementById('page-title').innerHTML=document.title;
feather.replace();
if (location.search.includes('song_link')) {
	document.querySelector('#create-post #id_body').value = new URLSearchParams(location.search).get('song_link') + '\n'
}

element = document.querySelector('.post-body > p');
song_uri = element.innerHTML.match(/(\w*:\w*:\w*)/g)[0];
element.innerHTML = element.innerHTML.replace(song_uri, `<a href="https://open.spotify.com/embed/${song_uri.split(':').slice(1).join('/')}" target="_blank">${song_uri}</a>`)