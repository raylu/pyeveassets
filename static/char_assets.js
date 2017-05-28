document.addEventListener('DOMContentLoaded', () => {
	'use strict';

	const click = (evt) => {
		evt.preventDefault();
		const itemId = evt.target.dataset.id;
		const ul = document.getElementById(itemId);
		if (ul.style.display == 'block')
			ul.style.display = 'none';
		else
			ul.style.display = 'block';
	}

	document.querySelectorAll('table.assets a').forEach((a) => {
		a.addEventListener('click', click);
	});
});
