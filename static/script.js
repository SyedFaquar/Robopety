const loginForm = document.getElementById("loginForm");
const signupForm = document.getElementById("signupForm");
const searchField = document.getElementById("searchField");
const filterField = document.getElementById("search-field");
const logoutBtn = document.getElementById("logout-p");

var errorField = document.getElementById("errorText");
var nameText = document.getElementById("username-display");
var filteredList = document.getElementById("filtered-list");
var userRobotContainer = document.getElementById("user-robot");

if (nameText) {
  var token = sessionStorage.getItem("token");
  fetch("/getusername", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `token=${token}`,
  })
    .then((response) => response.json())
    .then((data) => {
      nameText.innerText = data.username;
    })
    .catch((error) => console.error("Error:", error));
}

if (filteredList) {
  var token = sessionStorage.getItem("token");
  fetch("/getallrobots", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `token=${token}`,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      console.log(data.all_robots);
      console.log(data.user_robot);
      updateRobotList(filteredList, data.all_robots, data.user_robot);
    })
    .catch((error) => console.error("Error:", error));
}

if (userRobotContainer) {
  var token = sessionStorage.getItem("token");
  fetch("/getuserrobot", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `token=${token}`,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      console.log(data.robot);
      updateCurrentPet(data.robot);
    })
    .catch((error) => console.error("Error:", error));
}
// console.log(signupForm);

logoutBtn?.addEventListener("click", (event) => {
  event.preventDefault();
  sessionStorage.clear();
  window.location.href = "/login";
});
filterField?.addEventListener("input", (event) => {
  event.preventDefault();
  filterPetList(event.target.value);
});

signupForm?.addEventListener("submit", function (event) {
  event.preventDefault();
  console.log("checking inputs....");
  const formData = new FormData(event.target);
  if (!formData.get("email")) {
    errorField.innerText = "Please enter an email";
    return;
  } else if (!validateEmail(formData.get("email"))) {
    errorField.innerText = "Invalid email";
    return;
  } else if (!formData.get("password_1")) {
    errorField.innerText = "Please enter a password";
    return;
  } else if (!formData.get("password_2")) {
    errorField.innerText = "Password not match";
    return;
  }
  console.log("sign up now.....");
  fetch("/usersignup", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(response.statusText);
      }
      return response.json();
    })
    .then((user) => {
      sessionStorage.setItem("token", user["token"]);
      window.location.href = "/user/1";
    })
    .catch((error) => {
      errorField.innerText = "Authentication failed: " + error.message;
    });
});

loginForm?.addEventListener("submit", function (event) {
  event.preventDefault();

  // Get the input value
  const formData = new FormData(event.target);
  console.log(errorField);
  if (!formData.get("email")) {
    errorField.innerText = "Please enter an email";
    return;
  } else if (!validateEmail(formData.get("email"))) {
    errorField.innerText = "Invalid email";
    return;
  } else if (!formData.get("password")) {
    errorField.innerText = "Please enter a password";
    return;
  }
  // Make a POST request to the Flask server for authentication
  fetch("/userlogin", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Invalid credentials");
      }
      return response.json();
    })
    .then((user) => {
      console.log("User login.......");
      console.log(user["username"]);
      sessionStorage.setItem("token", user["token"]);
      // getPets();
      window.location.href = "/user/1";
    })
    .catch((error) => {
      errorField.innerText = "Authentication failed: " + error.message;
    });
});

function getPets() {
  fetch("/getpet")
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      const serializedPets = JSON.stringify(data);
    })
    .catch((error) => {
      console.error("Failed to obtain pet data: ", error.message);
    });
}

searchField?.addEventListener("input", (event) => {
  event.preventDefault();
  filter(event.target.value);
});

function updateRobotList(list, robots, userRobots) {
  list.innerHTML = "";
  robots?.forEach(function (item) {
    createPetElement(list, item, userRobots);
  });
}

function updateCurrentPet(robot) {
  userRobotContainer.innerHTML = "";
  // console.log(robot);
  if (robot.robot_id == -1) {
    var p = document.createElement("p");
    p.innerText = "You do not have a pet yet.";
    userRobotContainer.appendChild(p);
  } else {
    const img = createImageElement(robot.robot_name, "100px");
    const p = createNameElement(robot.robot_name);
    var btn = document.createElement("button");
    btn.innerText = "Return";
    btn.setAttribute("id", "btn-return");
    btn.addEventListener("click", function () {
      // set request to Flask server to update the database
      returnRobot(robot.robot_id);
    });
    userRobotContainer.appendChild(img);
    userRobotContainer.appendChild(p);
    userRobotContainer.appendChild(btn);
  }
}

function createPetElement(listContainer, pet, userRobot) {
  var li = document.createElement("li");
  var div = document.createElement("div");
  const img = createImageElement(pet.name, "75px");
  const p = createNameElement(pet.name);
  listContainer.appendChild(li);
  li.appendChild(div);
  div.appendChild(img);
  div.appendChild(p);
  div.setAttribute("class", "robopet");
  p.innerText = pet.name;
  if (userRobot.robot_id == -1) {
    var button = document.createElement("button");
    div.appendChild(button);
    button.innerText = "Select";
    button.setAttribute("id", "btn-select-" + pet.name);
    button.addEventListener("click", function () {
      selectUserRobot(pet.robot_id);
    });
  }
}

function selectUserRobot(robotId) {
  const token = sessionStorage.getItem("token");
  const formData = new URLSearchParams();
  formData.append("token", token);
  formData.append("robot_id", robotId);
  fetch("/setuserrobot", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData,
  })
    .then((response) => {
      return response.json();
    })
    .then((user) => {
      sessionStorage.setItem("token", user["token"]);
      window.location.href = "/user/1";
    })
    .catch((error) => {
      console.log(error.message);
    });
}
function returnRobot(robotId) {
  const token = sessionStorage.getItem("token");
  const formData = new URLSearchParams();
  formData.append("token", token);
  formData.append("robot_id", robotId);
  fetch("/returnuserrobot", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData,
  })
    .then((response) => {
      return response.json();
    })
    .then((user) => {
      sessionStorage.setItem("token", user["token"]);
      window.location.href = "/user/1";
    })
    .catch((error) => {
      console.log(error.message);
    });
}

function createNameElement(petName) {
  var p = document.createElement("p");
  p.innerText = petName[0].toUpperCase() + petName.slice(1);
  return p;
}

function createImageElement(petName, size) {
  var img = document.createElement("img");
  img.setAttribute("class", "robopet");
  img.setAttribute("src", "/getRobotImage/" + petName + ".png");
  img.setAttribute("alt", "RoboPet");
  img.setAttribute("width", size);
  img.setAttribute("height", size);
  return img;
}

function filterPetList(filterValue) {
  var token = sessionStorage.getItem("token");
  fetch("/getallrobots", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `token=${token}`,
  })
    .then((response) => response.json())
    .then((data) => {
      if (filterValue == "") {
        filter_robots = data.all_robots;
      } else {
        filter_robots = data.all_robots.filter((robot) =>
          robot.name.includes(filterValue)
        );
      }
      updateRobotList(filteredList, filter_robots, data.user_robot);
    })
    .catch((error) => console.error("Error:", error));
}

function validateEmail(email) {
  return String(email)
    .toLowerCase()
    .match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
}
