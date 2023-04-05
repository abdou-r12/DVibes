function CheckLoginUser() {
    let user_login = document.getElementById("user_login");
    let coach_login = document.getElementById("coach_login");
    let user_btn = document.getElementById("user");
    let coach_btn = document.getElementById("coach");
    user_login.style.display = "block";
    coach_login.style.display = "none";
    user_btn.style.display = "none";
    coach_btn.style.display = "block";
}
function CheckLoginCoach() {
    let user_login = document.getElementById("user_login");
    let coach_login = document.getElementById("coach_login");
    let user_btn = document.getElementById("user");
    let coach_btn = document.getElementById("coach");
    user_login.style.display = "none";
    coach_login.style.display = "block";
    coach_btn.style.display = "none";
    user_btn.style.display = "block";
}