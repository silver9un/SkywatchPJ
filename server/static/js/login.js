"use strict";

const loginId = document.getElementById('LOGIN_ID');
const loginPw = document.getElementById('LOGIN_PW');
const loginBtn = document.getElementById('LOGIN_BTN');

function color() {
    if((loginId.value.length>0)
        && loginPw.value.length>=4){
        loginBtn.style.backgroundColor = "#0095F6";
        loginBtn.disabled = false;
    }else{
        loginBtn.style.backgroundColor = "#C0DFFD";
        loginBtn.disabled = true;
    }
}

// function moveToMain(){
//     location.replace("");
// }

loginId.addEventListener('keyup', color);
loginPw.addEventListener('keyup', color);
// loginBtn.addEventListener('click',moveToMain);