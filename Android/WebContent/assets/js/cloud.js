function emptyCheck(field, alerttxt) {
	with (field) {
		if (value==null || value=="") {
			alert(alerttxt);
			return false;
		}
		else 
			return true
	}
}

function emailCheck(field, alerttxt) {
	with (field) {
		apos=value.indexOf("@")
		dotpos=value.lastIndexOf(".")
		if (apos<1||dotpos-apos<2) {
			alert(alerttxt);
			return false;
		}
		else 
			return true;
	}
}
function equalCheck(x, y, alerttxt) {
	if (document.getElementsByName(x).value != document.getElementsByName(y).value) {
		alert(alerttxt);
		return false;
	}
	
	return true;
}

function check1(form) {
	with (form) {
		if (emptyCheck(email,"请输入邮箱！") == false) {
			email.focus();
			return false;
		}
		if (emailCheck(email,"请输入正确的邮箱！") == false) {
			email.focus();
			return false;
		}
		if (emptyCheck(password,"请输入密码！") == false) {
			password.focus();
			return false;
		}
		return true;
	}
}

function check2(form) {
	with (form) {
		if (emptyCheck(email,"请输入邮箱！") == false) {
			email.focus();
			return false;
		}
		if (emailCheck(email,"请输入正确的邮箱！") == false) {
			email.focus();
			return false;
		}
		if (emptyCheck(password,"请输入密码！") == false) {
			password.focus();
			return false;
		}
		if (emptyCheck(password1,"请再次输入密码！") == false) {
			password1.focus();
			return false;
		}
		
		return true;
	}
}

function check3(form) {
	with (form) {
		if (emptyCheck(email,"请输入邮箱！") == false) {
			email.focus();
			return false;
		}
		if (emailCheck(email,"请输入正确的邮箱！") == false) {
			email.focus();
			return false;
		}
		return true;
	}
}

function check4(form) {
	with (form) {
		if (emptyCheck(veriCode,"请输入验证码！") == false) {
			veriCode.focus();
			return false;
		}
		return true;
	}
}

function check5(form) {
	with (form) {
		if (emptyCheck(password,"请输入密码！") == false) {
			password.focus();
			return false;
		}
		if (emptyCheck(password1,"请再次输入密码！") == false) {
			password1.focus();
			return false;
		}
		return true;
	}
}

