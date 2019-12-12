mode = "entire"; //entire, month, or week
function modeChange(){
	switch(document.getElementById('mode').value){
		case 'entire':
		mode = 'entire';
		document.getElementById('startdate').style.display = 'none';
		document.getElementById('startdatebr').style.display = 'none';
		document.getElementById("dump").onclick = function (){window.location.href = "/wsgi_bin/dump/" + "?mode=entire&fgt=" + fgt +"&timeoffset=" + new Date().getTimezoneOffset()};
		break;
		case 'month':
		mode = 'month';
		document.getElementById('startdate').style.display = 'block';
		document.getElementById('startdatebr').style.display = 'inline';
		document.getElementById("dump").onclick = function (){window.location.href = "/wsgi_bin/dump/" + "?mode=month&fgt=" + fgt +"&timeoffset=" + new Date().getTimezoneOffset()};
		break;
		case 'week':
		mode = 'week';
		document.getElementById('startdate').style.display = 'block';
		document.getElementById('startdatebr').style.display = 'inline';
		document.getElementById("dump").onclick = function (){window.location.href = "/wsgi_bin/dump/" + "?mode=week&fgt=" + fgt +"&timeoffset=" + new Date().getTimezoneOffset()};
		break;
	}
}
function dateChange(parameter){
	switch(parameter){
		case 'year':
			$.ajax({
				type: 'POST',
				url: '/wsgi_bin/data/dates/',
				data: JSON.stringify ({fgt: fgt, mode: 'months', time: $("#year option:selected").val()}),
				success: function(data){
					$("#month").empty();
					for (var i=0; i < data.length; i++){
						$("#month").append(new Option (data[i], data[i]));
					};
					$("#month option:last").attr("selected", "selected");
					$.ajax({
						type: 'POST',
						url: '/wsgi_bin/data/dates/',
						data: JSON.stringify({fgt:fgt, mode: 'days', time: $('#month option:selected').val() + '/' + $('#year option:selected').val()}),
						success: function(data){
							$("#day").empty();
							for (var i=0; i < data.length; i++){
								$("#day").append(new Option (data[i], data[i]));
							};
						},
						contentType: "application/json"
					});
				},
				contentType: "application/json"
			});
		break;
		case 'month':
			$.ajax({
				type: 'POST',
				url: '/wsgi_bin/data/dates/',
				data: JSON.stringify ({fgt: fgt, mode: 'days', time: $("#month option:selected").val()+"/"+ $("#year option:selected").val()}),
				success: function(data){
					$("#day").empty();
					for (var i=0; i < data.length; i++){
						$("#day").append(new Option (data[i], data[i]));
					};
					$("#day option:last").attr("selected", "selected");
				},
				contentType: "application/json"
			});
		break;
	}
}
