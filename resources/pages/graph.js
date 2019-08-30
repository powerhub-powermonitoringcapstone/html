//requires plotly
x = [], y = [], fgt = Cookies.get('fgt');
function plot(f){
	$.ajax({
		type: 'POST',
		url: '/wsgi_bin/data/graph/',
data: JSON.stringify ({fgt:fgt, mode: f}), //program _start_, _real_ time (last 50 readings)
success: function(data){
	x = [], y = [];
	for(var i = 0; i < data.length; i++){
		x.push(i); y.push(parseFloat(data[i].current));
	};
	console.log(x); console.log(y);
	Plotly.react('graph', [{x:x, y:y}]);
},
contentType: "application/json"
});
}