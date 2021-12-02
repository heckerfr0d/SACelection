// getting all required elements
const inputBox = document.querySelector(".inputField input");
const addBtn = document.querySelector(".inputField button");
const todoList = document.querySelector(".todoList");
const deleteAllBtn = document.querySelector(".footer button");

const addCandidate = () => {
  const name = document.getElementById("modal-name");
  const email = document.getElementById("modal-email");
  const position = name.getAttribute("data-position");
  if (name.value && email.value) {
    fetch("/addcandidate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: name.value,
        email: email.value,
        position: position,
      }),
    })
      .then((resp) => console.log(resp.json()))
      .then(window.location.reload());
  }
};

window.onload = () => {
  const closeBtn = document.getElementById("close-btn");
  const modal = document.querySelector(".modal-overlay");
  closeBtn.addEventListener("click", function () {
    modal.classList.remove("open-modal");
  });
};

const getModal = (id) => {
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
};
const deleteCandidate = (email) => {
  console.log(email);
  const candidate = document.getElementById(email);
  candidate.remove();
  fetch("/deletecandidate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: email,
    }),
  }).then((resp) => console.log(resp.json()));
};
