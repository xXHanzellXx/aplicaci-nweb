// CORRECCIÓN: URL completa de Render para que Netlify la encuentre
const API_URL = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
    ? "http://127.0.0.1:5000/api" 
    : "https://aplicaci-nweb.onrender.com/api";

// --- Lógica del Avatar ---
function changeShirt(imgSrc) {
    const shirt = document.getElementById("shirt");
    if (shirt) {
        shirt.src = imgSrc;
        shirt.style.display = "block";
    }
}

function changePants(imgSrc) {
    const pants = document.getElementById("pants");
    if (pants) {
        pants.src = imgSrc;
        pants.style.display = "block";
    }
}

// --- Autenticación ---
async function register() {
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const errorDiv = document.getElementById("error");

    if (!name || !email || !password) {
        if (errorDiv) errorDiv.innerText = "Por favor, completa todos los campos";
        return;
    }

    try {
        const res = await fetch(`${API_URL}/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, password })
        });

        const data = await res.json();

        if (res.ok) {
            alert("Registro exitoso, ahora inicia sesión");
            window.location.href = "index.html";
        } else {
            if (errorDiv) errorDiv.innerText = data.error || "Error en el registro";
        }
    } catch (err) {
        if (errorDiv) errorDiv.innerText = "No se pudo conectar con el servidor de Render";
        console.error("Error detallado:", err);
    }
}

async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const errorDiv = document.getElementById("error");

    try {
        const res = await fetch(`${API_URL}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await res.json();

        if (res.ok && data.token) {
            localStorage.setItem("token", data.token);
            window.location.href = "home.html";
        } else {
            if (errorDiv) errorDiv.innerText = data.error || "Credenciales incorrectas";
        }
    } catch (err) {
        if (errorDiv) errorDiv.innerText = "Error de conexión";
        console.error("Error:", err);
    }
}

// --- Guardar Outfit ---
async function saveOutfit() {
    const token = localStorage.getItem("token");
    const shirt = document.getElementById("shirt");
    const pants = document.getElementById("pants");

    if (!token) {
        alert("Debes iniciar sesión para guardar tu outfit");
        return;
    }

    try {
        const res = await fetch(`${API_URL}/outfit`, {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}` 
            },
            body: JSON.stringify({ 
                shirt: shirt ? shirt.src : "", 
                pants: pants ? pants.src : "" 
            })
        });

        const data = await res.json();
        if (res.ok) {
            alert(data.message || "¡Outfit guardado con éxito!");
        } else {
            alert(data.error || "Error al guardar outfit");
        }
    } catch (err) {
        alert("Error de red al intentar guardar");
    }
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "index.html";
}
