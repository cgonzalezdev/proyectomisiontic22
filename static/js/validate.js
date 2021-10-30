var enableFormSubmitRegister = false;
function compareRetypePassword() {
  var password = document.getElementById("password").value;
  var retypePassword = document.getElementById("retypePassword").value;
  if (retypePassword.localeCompare(password)) {
	enableFormSubmitRegister = false;
	document.getElementById("errorRetypePassword").innerText = "Ambas contraseñas deben ser iguales";
	document.getElementById("retypePassword").value = "";
  } else{
	enableFormSubmitRegister = true;
	document.getElementById("errorRetypePassword").innerText = "";	
  }
};

function ValidateEmailRegister(email) {
 if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email.value)) {
	enableFormSubmitRegister = true;
	document.getElementById("errorEmail").innerText = "";	    
  } else {
	enableFormSubmitRegister = false;
	document.getElementById("errorEmail").innerText = "Ingrese un email valido";
	email.value = "";
  }
};

function ValidateNumberRegister(n, nameID) {
if (n.value !== "") {	
	let num = n.value;
 if (/^[0-9]+$/.test(num)) { 
	enableFormSubmitRegister = true;
	document.getElementById(nameID).innerText = "";	
 } else {	
    enableFormSubmitRegister = false;
	document.getElementById(nameID).innerText = "Debe ingresar un numero entero";
	n.value = ""; 		
 }
}
};

$('#imgUpload').change(function(e){
	var fileSize = e.target.files[0].size;
	document.getElementById("sizeImageUpload").innerText = fileSize+" bytes";
	if(fileSize > 104327){
		enableFormSubmitRegister = false;
		alert("El archivo es muy grande.");			
	} else {
		enableFormSubmitRegister = true;
	}
});

$('#imagen').change(function(e){
	var fileSize = e.target.files[0].size;
	document.getElementById("sizeImageUpload").innerText = fileSize+" bytes";
	if(fileSize > 104327){
		enableFormSubmitRegister = false;
		alert("El archivo es muy grande.");			
	} else {
		enableFormSubmitRegister = true;
	}
});

function formSubmitRegister() {
	if (enableFormSubmitRegister) { 
		return true;
	} else {
		return false;
	}
};