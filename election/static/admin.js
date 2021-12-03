// getting all required elements
const inputBox = document.querySelector(".inputField input");
const addBtn = document.querySelector(".inputField button");
const todoList = document.querySelector(".todoList");
const deleteAllBtn = document.querySelector(".footer button");

const addCandidate = () => {
  //function to add candidate
  const name = document.getElementById("modal-name");
  const email = document.getElementById("modal-email"); //getting all necessary data from html DOM
  const position = name.getAttribute("data-position");
  if (name.value && email.value) {
    fetch("/addcandidate", {
      //sending a post request
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: name.value,
        email: email.value,
        position: position, //candidate data
      }),
    }).then(
      setTimeout(() => {
        console.log(window.location.reload()); //relaoding the window after a 1s delay
      }, 1000)
    );
  }
};

window.onload = () => {
  const closeBtn = document.getElementById("close-btn");
  const modal = document.querySelector(".modal-overlay");
  closeBtn.addEventListener("click", function () {
    // adding functionality to modal's close buttons
    modal.classList.remove("open-modal");
  });
};

const getModal = (id) => {
  //function to open modal and fill it with necessary details
  let myinputbox = document.getElementById("add" + id);
  if (myinputbox.value) {
    const nameinput = document.getElementById("modal-name");
    nameinput.setAttribute("data-position", id);
    nameinput.value = myinputbox.value;
    const modal = document.querySelector(".modal-overlay");
    modal.classList.add("open-modal");
  }
};

const modifySchedule = (election_id) => {
  window.location.href = `${window.origin}/election/${election_id}`;
  //function to redirect to the modify schedule page with election_id passed in
};
const deleteCandidate = (email) => {
  const candidate = document.getElementById(email); //getting all necessary data from html DOM
  candidate.remove(); //removing the candidate from the front end
  fetch("/deletecandidate", {
    //sending a post request to remove candidate from the database
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: email, //candidate email-id
    }),
  });
};
const deleteAllCandidates = (id) => {
  const list = document.getElementById("list" + id); // getting the list containing all thecandidates
  list.innerHTML = ""; //removing the candidates from the front end
  fetch("/deleteallcandidate", {
    //sending a post request to remove all the  candidates from the database
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: id, //position_id
    }),
  });
};
