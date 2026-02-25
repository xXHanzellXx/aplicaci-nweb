const API_URL = "/api"; // Al estar en el mismo servidor de Render, no necesitas poner la URL completa

// --- Lógica del Avatar (Dress to Impress) ---
function changeShirt(imgSrc) {
    const shirt = document.getElementById("shirt");
    shirt.src = imgSrc;
    shirt.style.display = "block";
}

function changePants(imgSrc) {
    const pants = document.getElementById("pants");
    pants.src = imgSrc;
    pants.style.display = "block";
}

// --- Peticiones al Servidor ---
async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const res = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (data.token) {
        localStorage.setItem("token", data.token);
        window.location.href = "home.html";
    } else {
        document.getElementById("error").innerText = data.error;
    }
}

async function saveOutfit() {
    const token = localStorage.getItem("token");
    const shirt = document.getElementById("shirt").src;
    const pants = document.getElementById("pants").src;

    const res = await fetch(`${API_URL}/outfit`, {
        method: "POST",
        headers: { 
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}` 
        },
        body: JSON.stringify({ shirt, pants })
    });
    const data = await res.json();
    alert(data.message);
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "index.html";
}
