const API = "https://TU_BACKEND_RENDER.onrender.com/api";

const token = localStorage.getItem("token");

async function loadClothes() {
  const res = await fetch(`${API}/clothes`);
  const data = await res.json();

  const catalog = document.getElementById("catalog");
  catalog.innerHTML = "";

  data.forEach(item => {
    catalog.innerHTML += `
      <div class="card">
        <h3>${item.name}</h3>
        <p>$${item.price}</p>
        <button onclick="rentClothe('${item._id}')">
          Alquilar
        </button>
      </div>
    `;
  });
}

async function rentClothe(id) {
  await fetch(`${API}/rent`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": token
    },
    body: JSON.stringify({ clothe_id: id })
  });

  alert("Alquiler realizado");
}

function changeShirt(img) {
  document.getElementById("shirt").src = img;
}

function changePants(img) {
  document.getElementById("pants").src = img;
}

async function saveOutfit() {
  await fetch(`${API}/outfit`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": token
    },
    body: JSON.stringify({
      shirt: document.getElementById("shirt").src,
      pants: document.getElementById("pants").src
    })
  });

  alert("Outfit guardado");
}

loadClothes();
function logout() {
  localStorage.removeItem("token");
  window.location.href = "index.html";
}