var loginworker = new Worker('/resources/pages/login_worker.js');
loginworker.postMessage({fgt: Cookies.get('fgt')});
loginworker.onmessage = function(e) {
	if (e.data == false){
		window.location.href = "/resources/pages/login.html";
	}
};