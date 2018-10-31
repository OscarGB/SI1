$(document).ready(function(){
        $(".detalles").click(function(){
            $(this).parents(".por_poner_algo").parents(".flex-row").children(".desplegable").fadeToggle();
        });
    });