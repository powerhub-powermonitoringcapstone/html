//auto graph data refresh handler (c) 2019 powerhub
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function demo(e) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			self.postMessage(this.responseText);
		}
	};
	while (1){
		xhttp.open("POST", "/wsgi_bin/data/past/", true);
		xhttp.setRequestHeader("Content-Type", "application/json");
		xhttp.send(JSON.stringify({fgt:e.fgt, mode:'last'})); 
		await sleep(e.ref);
	}
}
self.onmessage = function(msg){
	demo({fgt:msg.data.fgt, ref:msg.data.ref});
};