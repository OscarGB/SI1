
function change_contador(){
	var a = Math.floor(Math.random() * 100) + 1;
	$(".contador").html(a);
}

$(document).ready(function(){
	change_contador();
    $("#sidebar-handle").click(function(){
        $(".sidebar").toggle();
    });

	setInterval(change_contador, 3000);

});