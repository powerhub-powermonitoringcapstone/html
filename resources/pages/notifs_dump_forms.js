function formChange(){
	switch(document.getElementById('mode').value){
		case 'entire':
			document.getElementById('startdate').style.display = 'none';
			document.getElementById('startdatebr').style.display = 'none';
			document.getElementById("dump").onclick = function (){window.location.href = "/wsgi_bin/dump/" + "?mode=entire&fgt=" + fgt +"&timeoffset=" + new Date().getTimezoneOffset()};
			break;
		case 'month':
			document.getElementById('startdate').style.display = 'block';
			document.getElementById('startdatebr').style.display = 'inline';
			alert('placeholder!');
			break;
		case 'week':
			document.getElementById('startdate').style.display = 'block';
			document.getElementById('startdatebr').style.display = 'inline';
			alert('placeholder!');
			break;
	}
}