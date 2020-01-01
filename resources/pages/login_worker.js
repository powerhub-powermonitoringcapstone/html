self.onmessage = function(msg){
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			self.postMessage(this.responseText);
		}
	}	
	xhttp.open("POST", "/wsgi_bin/login/", true);
	xhttp.setRequestHeader("Content-Type", "application/json");
	xhttp.send(JSON.stringify({fgt:msg.data.fgt})); 
	};
