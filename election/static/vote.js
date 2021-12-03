function handlevote(can_name) {
  //function to register the vote
  if (can_name != "Vote registered") {
    fetch(`${window.origin}/vote`, {
      //sending a post request
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        can_name: can_name, // sending candidate data
      }),
    }).then((resp) => {
      window.location.reload(); //reloading the window with the modified data
    });
  }
}
