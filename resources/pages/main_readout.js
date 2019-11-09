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
		document.getElementById("wattage").innerHTML = wattage.toFixed(2);
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
	//graphing
	var dyg = new Worker('main_graphworker.js');
	dyg.postMessage({fgt:fgt, ref:ref});
	dyg.onmessage = function(e){ 				
		e = JSON.parse(e.data);
		x = [], y = [];
		for (var i = 0; i < e.length; i++){
			x.push(i); y.push((parseFloat(e[i].voltage) * parseFloat(e[i].current) * parseFloat(e[i].pf)).toFixed(2));
		};
		Plotly.react('graph', [{x:x, y:y}], {margin: {l:0,r:0,b:0,t:0,pad:2}});
	}
	function changeGraphType(){
		switch($('#displayData').children("option:selected").val()){
			case 'average':
				x = [], y = [];
				$.ajax({
					type: 'POST',
					url: '/wsgi_bin/data/past/',
					data: JSON.stringify({fgt: fgt, time: String(today.getUTCMonth()+ 1)+"/"+String(today.getUTCDate()-2)+"/"+String(today.getUTCFullYear()), mode:'day'}),
					contentType: "application/json",
					success: function(data){
						if (data.length != 0){
							$('select[name="displayDates"]').append(new Option(today.toLocaleString('default', {month:'long'}) + " " + String(today.getDate()-2), "todayAvg"));
							$('select[name="displayDates"]').append(new Option(today.toLocaleString('default', {month:'long'}) + " " + String(today.getDate()-2) + " - " + today.toLocaleString('default', {month:'long'}), "todayAvg") + " " + String(today.getDate()), "ThreeDaysTogether");
							// for (var i = 0; i < data.length; i++){
							// 	x.push(i); y.push((parseFloat(data[i].voltage) * parseFloat(data[i].current) * parseFloat(data[i].pf)).toFixed(2));
							// 	console.log(y);
							// } LETS USE A WORKER INSTEAD FOR THE GRAPH CHANGING
						}
					}
				});
				$.ajax({
					type: 'POST',
					url: '/wsgi_bin/data/past/',
					data: JSON.stringify({fgt: fgt, time: String(today.getUTCMonth()+ 1)+"/"+String(today.getUTCDate()-1)+"/"+String(today.getUTCFullYear()), mode:'day'}),
					contentType: "application/json",
					success: function(data){
						if (data.length != 0){
							$('select[name="displayDates"]').append(new Option(today.toLocaleString('default', {month:'long'}) + " " + String(today.getDate()-1), "todayAvg"));
							// for (var i = 0; i < data.length; i++){
							// 	x.push(i); y.push((parseFloat(data[i].voltage) * parseFloat(data[i].current) * parseFloat(data[i].pf)).toFixed(2));
							// } LETS USE A WORKER INSTEAD FOR THE GRAPH CHANGING
						}else{alert('fegelein!')}
					}
				});
				$.ajax({
					type: 'POST',
					url: '/wsgi_bin/data/past/',
					data: JSON.stringify({fgt: fgt, time: String(today.getUTCMonth()+ 1)+"/"+String(today.getUTCDate())+"/"+String(today.getUTCFullYear()), mode:'day'}),
					contentType: "application/json",
					success: function(data){
						if (data.length != 0){
							$('select[name="displayDates"]').append(new Option(today.toLocaleString('default', {month:'long'}) + " " + String(today.getDate()), "todayAvg"));
							// for (var i = 0; i < data.length; i++){
							// 	x.push(i); y.push((parseFloat(data[i].voltage) * parseFloat(data[i].current) * parseFloat(data[i].pf)).toFixed(2));
							// 	console.log(y);
							// } LETS USE A WORKER INSTEAD
						}
					}
				});
				document.getElementById("graphcontrols").style.display = "block";
			break;
			case 'instantaneous':
				document.getElementById("graphcontrols").style.display = "none";
				var dyg = new Worker('main_graphworker.js');
			break;	
			case 'overall':
				document.getElementById("graphcontrols").style.display = "none";
			break;
		};
	}