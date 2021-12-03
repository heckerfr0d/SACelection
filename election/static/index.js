function handleClick() {
  // function to check if the user has entered details for each input in the login
  const name1 = document.getElementById("email");
  const content = document.getElementById("password");
  if (!name1.value) {
    //checking if the input has some value entered
    document.getElementById("comment").innerHTML = "Please enter your email!"; // prompting the user to enter the details
  } else if (!content.value) {
    document.getElementById("comment").innerHTML =
      "Please Enter your Password! ";
  }

  if (!(name1.value && content.value)) return false;
  return true;
}
