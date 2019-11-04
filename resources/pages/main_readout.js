//readData
	function readData(){
	$.ajax({
		type: 'POST',
		url: '/wsgi_bin/data/real/',
		data: JSON.stringify({fgt: fgt}),
		success: function(data){
			$('#voltage').html(data.voltage);
			$('#current').html(data.current);
			$('#wattage').html(data.voltage * data.current);
			$('#nodename').html(data.nodename);
			$('#firmware').html(data.firmware);
		},
		contentType: "application/json"
		});
	$.ajax({
		type: 'POST',
		url: '/wsgi_bin/settings/data/',	// we polled the carbon footprint only once
		data: JSON.stringify({fgt:fgt}),    // in the session in order to save up on data.
		success: function(data){            // we may want to poll this every five seconds instead hmm.... asynchronous function
			fpt = data.carbfpt;
			// alert(fpt);
		},
		contentType: "application/json"
	});
	}
	//autorefresher
	var dyn = new Worker('main_readoutworker.js');
	dyn.postMessage(fgt);
	dyn.onmessage = function(e) {
		data = JSON.parse(e.data);
		if (data.notify == "True"){
			//console.log("yuh");
			$('.overv').toggle();
		};
		wattage = data.voltage * data.current * data.pf;
		$('#voltage').html(data.voltage);
		$('#current').html(data.current);
		$('#pf').html(data.pf);
		$('#kwh').html(parseFloat(data.kwh).toFixed(2));
		$('#wattage').html(wattage);
		$('#carbfpt').html((wattage * fpt / 100).toFixed(2));
		//console.log(data.notify);
		// console.log(data.variation);
	};