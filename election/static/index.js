const name = document.getElementById("name");
const content = document.getElementById("content");
const submit = document.getElementById("submit");
function handleClick() {
  const name1 = document.getElementById("email");
  const content = document.getElementById("password");
  if (!name1.value) {
    document.getElementById("comment").innerHTML = "Please enter your email!";
  } else if (!content.value) {
    document.getElementById("comment").innerHTML =
      "Please Enter your Password! ";
  }

  if (!(name1.value && content.value)) return false;
  return true;
}

function rerouteHome() {
  location.href = `${window.origin}/home`;
}
/////
// window.onload = () => {
//   if (document.cookie.length != 0) {
//     let user = getCookie("username");
//     document.getElementById("name").value = user;
//   }
// };

// function getCookie(cname) {
//   let name = cname + "=";
//   let ca = document.cookie.split(";");
//   for (let i = 0; i < ca.length; i++) {
//     let c = ca[i];
//     while (c.charAt(0) == " ") {
//       c = c.substring(1);
//     }
//     if (c.indexOf(name) == 0) {
//       return c.substring(name.length, c.length);
//     }
//   }
//   return "";
// }

// function setCookie(cname, cvalue, exdays) {
//   if (cvalue) {
//     const d = new Date();
//     d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1000);
//     let expires = "expires=" + d.toUTCString();
//     document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
//   }
// }