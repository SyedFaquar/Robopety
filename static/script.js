const loginForm = document.getElementById("loginForm");
const signupForm = document.getElementById("signupForm");
const searchField = document.getElementById("searchField");
const filterField = document.getElementById("search-field");
const logoutBtn = document.getElementById("logout-p");

var errorField = document.getElementById("errorText");
var nameText = document.getElementById("username-display");
var filteredList = document.getElementById("filtered-list");
var userRobotContainer = document.getElementById("user-robot");

if (
  !sessionStorage.getItem("token") &&
  window.location.pathname === "/user/1"
) {
  window.location.href = "/login";
}

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
      updateCurrentPet(data.robot);
    })
    .catch((error) => console.error("Error:", error));
}

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
  const formData = new FormData(event.target);
  email = formData.get("email");
  username = formData.get("username");
  password_1 = formData.get("password_1");
  password_2 = formData.get("password_2");
  if (!email) {
    errorField.innerText = "Please enter an email";
    signupForm.reset();
    return;
  } else if (!validateEmail(email)) {
    errorField.innerText = "Invalid email";
    signupForm.reset();
    return;
  } else if (!password_1) {
    errorField.innerText = "Please enter a password";
    signupForm.reset();
    return;
  } else if (!password_2) {
    errorField.innerText = "Password not match";
    signupForm.reset();
    return;
  } else if (password_1 != password_2) {
    errorField.innerText = "Password not match";
    signupForm.reset();
    return;
  } else if (
    !containsLowercase(password_1) ||
    !containsLowercase(password_1) ||
    !containsSymbol(password_1) ||
    !containsNumber(password_1)
  ) {
    errorField.innerText =
      "Password must be between 10 and 20 characters long and include at least one uppercase letter, one lowercase letter, and one symbol.";
    signupForm.reset();
    return;
  }

  if (!username) {
    username = "User";
  }

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
      signupForm.reset();
      errorField.innerText = "Authentication failed: " + error.message;
    });
});

loginForm?.addEventListener("submit", function (event) {
  event.preventDefault();

  // Get the input value
  const formData = new FormData(event.target);
  if (!formData.get("email")) {
    errorField.innerText = "Please enter an email";
    loginForm.reset();
    return;
  } else if (!validateEmail(formData.get("email"))) {
    errorField.innerText = "Invalid email";
    loginForm.reset();
    return;
  } else if (!formData.get("password")) {
    errorField.innerText = "Please enter a password";
    loginForm.reset();
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
      sessionStorage.setItem("token", user["token"]);
      window.location.href = "/user/1";
    })
    .catch((error) => {
      loginForm.reset();
      errorField.innerText = "Authentication failed: " + error.message;
    });
});

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
  var div = document.createElement("div");
  const img = createImageElement(pet.name, "75px");
  const p = createNameElement(pet.name);
  listContainer.appendChild(div);
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

function containsUppercase(str) {
  return /[A-Z]/.test(str);
}

function containsLowercase(str) {
  return /[a-z]/.test(str);
}

function containsSymbol(str) {
  // Define the list of special characters
  const specialChars = "`~!@#$%^&*()_+=-,./<>?;:'[]{}";

  // Escape special characters that have special meanings in regex and create a character class
  const escapedChars = specialChars.replace(/[-\/\\^$*+?.()|[\]{}]/g, "\\$&");

  // Create a regular expression using the special characters
  const regex = new RegExp("[" + escapedChars + "]");

  // Check if the string contains any of the special characters
  return regex.test(str);
}

function containsNumber(str) {
  return /\d/.test(str);
}
