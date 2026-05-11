// ================= API BASE URL =================

const API_BASE =
    "https://smartmed-backend-h7qx.onrender.com";

// ================= THEME =================

function initializeTheme() {

    const savedTheme =
        localStorage.getItem("theme");

    if(savedTheme === "dark") {

        document.body.classList.add("dark-mode");
    }
}

function toggleTheme() {

    document.body.classList.toggle("dark-mode");

    if(document.body.classList.contains("dark-mode")) {

        localStorage.setItem("theme", "dark");

    } else {

        localStorage.setItem("theme", "light");
    }
}

// ================= REGISTER =================

async function registerUser() {

    const name =
        document.getElementById("registerName").value.trim();

    const email =
        document.getElementById("registerEmail").value.trim();

    const password =
        document.getElementById("registerPassword").value;

    const message =
        document.getElementById("registerMessage");

    if(password.length < 8) {

        message.innerHTML =
            "Password must contain minimum 8 characters.";

        message.style.color = "red";

        return;
    }

    try {

        const response = await fetch(
            `${API_BASE}/register`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    name,
                    email,
                    password
                })
            }
        );

        const data = await response.json();

        if(response.ok) {

            message.innerHTML =
                "Registration Successful!";

            message.style.color = "green";

            setTimeout(() => {

                window.location.href =
                    "login.html";

            }, 1000);

        } else {

            message.innerHTML =
                data.message || "Registration Failed";

            message.style.color = "red";
        }

    } catch(error) {

        console.error(error);

        message.innerHTML =
            "Server Error";

        message.style.color = "red";
    }
}

// ================= LOGIN =================

async function loginUser() {

    const email =
        document.getElementById("email").value;

    const password =
        document.getElementById("password").value;

    try {

        const response = await fetch(
            `${API_BASE}/login`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    email,
                    password
                })
            }
        );

        const data = await response.json();

        if(response.ok) {

            localStorage.setItem(
                "token",
                data.token
            );

            localStorage.setItem(
                "user",
                JSON.stringify(data.user)
            );

            window.location.href =
                "dashboard.html";

        } else {

            document.getElementById(
                "loginMessage"
            ).innerHTML =
                data.message || "Invalid Credentials";
        }

    } catch(error) {

        console.error(error);

        document.getElementById(
            "loginMessage"
        ).innerHTML =
            "Server Error";
    }
}

// ================= DASHBOARD INIT =================

function initializeDashboard() {

    initializeTheme();

    const token =
        localStorage.getItem("token");

    if(!token) {

        window.location.href =
            "login.html";

        return;
    }

    const user =
        JSON.parse(localStorage.getItem("user"));

    if(user) {

        document.getElementById("username")
            .innerHTML =
            user.name || user.email;
    }
}

// ================= HISTORY INIT =================

function initializeHistoryPage() {

    initializeTheme();

    const token =
        localStorage.getItem("token");

    if(!token) {

        window.location.href =
            "login.html";

        return;
    }

    loadHistory();
}

// ================= LOGOUT =================

function logoutUser() {

    localStorage.removeItem("token");

    localStorage.removeItem("user");

    window.location.href =
        "login.html";
}

// ================= PREDICT =================

async function predictDisease() {

    const checked =
        document.querySelectorAll(
            'input[type="checkbox"]:checked'
        );

    let symptoms = [];

    checked.forEach(item => {

        symptoms.push(item.value);
    });

    if(symptoms.length === 0) {

        alert("Please select symptoms.");
        return;
    }

    const token =
        localStorage.getItem("token");

    try {

        const response = await fetch(
            `${API_BASE}/predict`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",

                    "Authorization":
                        `Bearer ${token}`
                },

                body: JSON.stringify({
                    symptoms
                })
            }
        );

        const data = await response.json();

        if(response.ok) {

            document.getElementById(
                "resultSection"
            ).classList.remove("hidden");

            document.getElementById("result")
                .innerHTML = `

                <div class="prediction-result-box">

                    <div class="result-top">

                        <h3>
                            ${data.prediction}
                        </h3>

                        <div class="confidence-badge">
                            ${data.confidence}
                        </div>

                    </div>

                    <div class="result-section">

                        <h4>Selected Symptoms</h4>

                        <div class="symptom-tags">

                            ${symptoms.map(
                                symptom =>
                                `<span>${symptom}</span>`
                            ).join("")}

                        </div>

                    </div>

                </div>
            `;

        } else {

            alert(
                data.message ||
                "Prediction Failed"
            );
        }

    } catch(error) {

        console.error(error);

        alert("Server Error");
    }
}

// ================= LOAD HISTORY =================

async function loadHistory() {

    const token =
        localStorage.getItem("token");

    try {

        const response = await fetch(
            `${API_BASE}/history`,
            {
                method: "GET",

                headers: {
                    "Authorization":
                        `Bearer ${token}`
                }
            }
        );

        const data = await response.json();

        const table =
            document.getElementById("historyTable");

        table.innerHTML = "";

        (data.history || []).forEach(record => {

            table.innerHTML += `

            <tr>

                <td>
                    ${new Date(
                        record.created_at
                    ).toLocaleString()}
                </td>

                <td>
                    ${record.symptoms}
                </td>

                <td>
                    ${record.prediction}
                </td>

                <td>
                    ${record.confidence}
                </td>

            </tr>
            `;
        });

    } catch(error) {

        console.error(error);
    }
}