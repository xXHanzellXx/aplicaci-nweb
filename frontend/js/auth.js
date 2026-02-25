const API_URL = "TU_URL_DE_RENDER_AQUI/api";

// --- Autenticación ---
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

function logout() {
  localStorage.removeItem("token");
  window.location.href = "index.html";
}

// --- Personalización del Avatar ---
function changeShirt(imgSrc) {
  document.getElementById("shirt").src = imgSrc;
}

function changePants(imgSrc) {
  document.getElementById("pants").src = imgSrc;
}

async function saveOutfit() {
  const token = localStorage.getItem("token");
  const shirt = document.getElementById("shirt").src;
  const pants = document.getElementById("pants").src;

  const res = await fetch(`${API_URL}/outfit`, {
    method: "POST",
    headers: { 
        "Content-Type": "application/json",
        "Authorization": token 
    },
    body: JSON.stringify({ shirt, pants })
  });
  
  const data = await res.json();
  alert(data.message || "Outfit guardado");
}