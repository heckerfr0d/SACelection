function handlevote(can_email) {
  //function to register the vote
  if (can_email != "Invalid") {
    fetch(`${window.origin}/vote`, {
      //sending a post request
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        can_email: can_email, // sending candidate data
      }),
    }).then((resp) => {
      window.location.reload(); //reloading the window with the modified data
    });
  }
}
