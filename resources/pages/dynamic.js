//auto data refresh handler (c) 2019 powerhub
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function demo() {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			self.postMessage(this.responseText);
		}
	};
	while (1){
		xhttp.open("GET", "/wsgi_bin/data/", true);
		xhttp.send(); 
		await sleep(1000);
	}
}
self.addEventListener('message', demo(), false);