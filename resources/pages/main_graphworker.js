//auto graph data refresh handler (c) 2019 powerhub
function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}

async function demo(e) {
	error = 0;
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			error = 0;
			self.postMessage(this.responseText);
		};
		if (this.readyState == 4 && this.status == 500) {
			error +=1;
			if (error > 2){error = 0;} else {
				xhttp.open("POST", "/wsgi_bin/data/past/", true);
				xhttp.setRequestHeader("Content-Type", "application/json");
				xhttp.send(JSON.stringify({fgt:e.fgt, mode:'lastmin', time:e.time})); 
				error = 0;
			};
		};
	}
	while (1){
		xhttp.open("POST", "/wsgi_bin/data/past/", true);
		xhttp.setRequestHeader("Content-Type", "application/json");
		xhttp.send(JSON.stringify({fgt:e.fgt, mode:'lastmin', time:e.time})); 
		await sleep(e.ref);
	}
}
self.onmessage = function(msg){
	demo({fgt:msg.data.fgt, ref:msg.data.ref, msg.data.time});
};
