	//main readout & data chor
	fpt = 0; ref = 3600; today = new Date(); insig = 0// refresh rate, carbon footprint, today, notification, don't notify
	$.ajax({
		type: 'POST',
		url: '/wsgi_bin/settings/data/',	// we polled the carbon footprint only once
		data: JSON.stringify({fgt:fgt}),    // in the session in order to save up on data.
		success: function(data){            // we may want to poll this every five seconds instead hmm.... asynchronous function;
			fpt = data.carbfpt;
			ref = 3600/(data.refresh)*1000; //refresh rate
			orgref = ref; //orig refresh rate			
		},
		contentType: "application/json",
		async: false
	});
	//autorefresher
	var readoutworker = new Worker('main_readoutworker.js');
	readoutworker.postMessage({fgt:fgt, ref: ref});
	readoutworker.onmessage = function(e) {
		data = JSON.parse(e.data);
		if (data.notify == "True"){
			$('.overv').css("display", "block");
			$("#notif")[0].play();
		} else {
			insig +=1;
			if (insig > 5) {insig = 0};
			if (insig == 3) {$('.overv').css("display", "none")};
		}
		wattage = data.voltage * data.current * data.pf;
		document.getElementById("voltage").innerHTML = data.voltage;
		document.getElementById("current").innerHTML = data.current;
		document.getElementById("wattage").innerHTML = wattage.toFixed(2);
		document.getElementById("pf").innerHTML = data.pf;
		document.getElementById("kwh").innerHTML = data.kwh.toFixed(2);
		document.getElementById("carbfpt").innerHTML = (data.kwh * fpt).toFixed(2);
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
	//graphing
	var graphworker = new Worker('main_graphworker.js');
	graphworker.postMessage({fgt:fgt, ref:ref, time:parseInt(document.getElementById("displayData").value)});
	graphworker.onmessage = function(e){ 				
		e = JSON.parse(e.data);
		x = [], y = [];
		for (var i = 0; i < e.length; i++){
			x.push(i); y.push((parseFloat(e[i].voltage) * parseFloat(e[i].current) * parseFloat(e[i].pf)).toFixed(2));
		};
		Plotly.react('graph', [{x:x, y:y}], {margin: {l:0,r:0,b:0,t:0,pad:2}});
	}
	function changeGraphType(){
		// readoutworker.terminate(); graphworker.terminate();
		switch($('#displayData').children("option:selected").val()){
			case '1':
			alert('implement later');
			/*ref = orgref;
			readoutworker.postMessage({fgt:fgt, ref:ref})*/
			break;
			case '5':
			alert('implement later');
			break;
		};
	}
