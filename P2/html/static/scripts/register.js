function checkForm(){
	var password = document.getElementById('password');
	var rep_password = document.getElementById('rep_password');
	var meter = document.getElementById('password-strength-meter');
	var errorMessage = document.getElementById("errorMessage");
	if(meter.value < 3){
		errorMessage.innerHTML="Demasiado débil";
		errorMessage.style.color = "red";
		return false;
	}
	if(password.value != rep_password.value){
		return false;
	}
	return true;
};

var strength = {
  0: "Worst",
  1: "Bad",
  2: "Weak",
  3: "Good",
  4: "Strong"
}

window.onload = function(){
	var password = document.getElementById('password');
	var rep_password = document.getElementById('rep_password');
	var meter = document.getElementById('password-strength-meter');
	var confirm = document.getElementById('confirmMessage');

	password.addEventListener('input', function() {
	  var val = password.value;
	  var result = zxcvbn(val);
	  errorMessage.innerHTML="";
	  // Update the password strength meter
	  meter.value = result.score;
	});

	document.getElementById('user').addEventListener('input', function(){
		var xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function() {
			if (this.readyState == 4 && this.status == 200) {
				if (this.responseText == "True"){
					$(".erroruser").show();
				}
				else {
					$(".erroruser").hide();
				}
			}
		};
		xhttp.open("GET", "/index.wsgi/user_exists/"+$('#user').val()+"/", true);
		xhttp.send();
	})

	function checkEqual(){
	  var val1 = password.value;
	  var val2 = rep_password.value;

	  if (val1 != val2) {
	  	confirm.innerHTML = "Contraseñas diferentes";
	  	confirm.style.color = "red";
	  }else{
	  	confirm.innerHTML = "";
	  }
	};

	rep_password.addEventListener('input', checkEqual);

	password.addEventListener('input', checkEqual);

};