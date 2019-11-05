	//main readout & data chor
	fpt = 0; ref = 3600; today = new Date();// refresh rate, carbon footprint, today
	$.ajax({
		type: 'POST',
		url: '/wsgi_bin/settings/data/',	// we polled the carbon footprint only once
		data: JSON.stringify({fgt:fgt}),    // in the session in order to save up on data.
		success: function(data){            // we may want to poll this every five seconds instead hmm.... asynchronous function;
			fpt = data.carbfpt;
			ref = 3600/(data.refresh)*1000; //refresh rate
		},
		contentType: "application/json",
		async: false
	});
	//autorefresher
	var dyn = new Worker('main_readoutworker.js');
	dyn.postMessage({fgt:fgt, ref: ref});
	dyn.onmessage = function(e) {
		data = JSON.parse(e.data);
		if (data.notify == "True"){
			$('.overv').toggle();
		};
		wattage = data.voltage * data.current * data.pf;
		document.getElementById("voltage").innerHTML = data.voltage;
		document.getElementById("current").innerHTML = data.current;
		document.getElementById("wattage").innerHTML = wattage;
		document.getElementById("pf").innerHTML = data.pf;
		document.getElementById("kwh").innerHTML = data.kwh.toFixed(2);
		document.getElementById("carbfpt").innerHTML = (wattage * fpt / 100).toFixed(2);
	};
	$.ajax({
		type: 'POST',
		url: '/wsgi_bin/data/real/',
		data: JSON.stringify({fgt: fgt}),
		success: function(data){
			document.getElementById("voltage").innerHTML = data.voltage;
			document.getElementById("current").innerHTML = data.current;
			document.getElementById("wattage").innerHTML = data.voltage * data.current * data.pf;
			document.getElementById("nodename").innerHTML = data.nodename;
			document.getElementById("firmware").innerHTML = data.firmware;
		},
	contentType: "application/json"
		});
