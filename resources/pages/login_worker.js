self.onmessage = function(msg){
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			x = false;
			if (this.responseText == "True"){x = true;};
			self.postMessage(x);
		}
	}	
	xhttp.open("POST", "/wsgi_bin/login/", true);
	xhttp.setRequestHeader("Content-Type", "application/json");
	xhttp.send(JSON.stringify({fgt:msg.data.fgt})); 
	};