var loginworker = new Worker('/resources/pages/login_worker.js');
loginworker.postMessage({fgt: Cookies.get('fgt')});
loginworker.onmessage = function(e) {
	if (e.data == "False"){
		window.location.href = "/resources/pages/login.html";
	}
	if (e.data == "Setup"){
		window.location.href = "/resources/pages/intro.html";
	}
};
