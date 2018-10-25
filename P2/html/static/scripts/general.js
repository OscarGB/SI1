
function change_contador(){
	var a = Math.floor(Math.random() * 100) + 1;
	$(".contador").html(a);
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			$(".contador").html(this.responseText);
		}
	};
	xhttp.open("GET", "/index.wsgi/contador/", true);
	xhttp.send();
}

$(document).ready(function(){
	change_contador();
    $("#sidebar-handle").click(function(){
        $(".sidebar").toggle();
    });

	setInterval(change_contador, 3000);

});