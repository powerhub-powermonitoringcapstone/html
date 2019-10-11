function isLogin(fgt){
	var x = 0;
	if(fgt!=undefined){
		$.ajax({
		type: 'POST',
		url: '/wsgi_bin/login/',
		data: JSON.stringify ({fgt: fgt}),
		success: function(data){
			if (data != "True"){
				Cookies.set('fgt',''); x = 0;
			} else if (data == "True"){x = 1};
		},
		contentType: "application/json",
		async: false
		});
	} else {/*return ("False");*/ x = 0;};
	return x;
}