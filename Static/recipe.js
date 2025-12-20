const API = "/api/recipes";
let currentPage = 1;
let currentLimit = 15;


loadRecipes();


async function loadRecipes(page = 1, limit = currentLimit) {
  currentPage = page;
  currentLimit = limit;

  const res = await fetch(`${API}?page=${page}&limit=${limit}`);
  const json = await res.json();

  renderTable(json.data || [], json.total || 0);
}


function renderStars(rating) {
  if (!rating) return "-";

  let html = `<div class="stars">`;
  for (let i = 1; i <= 5; i++) {
    html += `<span class="${rating >= i ? 'full' : rating >= i - 0.5 ? 'half' : ''}">★</span>`;
  }
  html += `</div>`;
  return html;
}


function renderTable(data, total) {
  const body = document.getElementById("tableBody");
  const fallback = document.getElementById("fallback");
  body.innerHTML = "";

  if (!data.length) {
    fallback.classList.remove("hidden");
    fallback.innerText = "No recipes found 🍽️";
    document.getElementById("pagination").innerHTML = "";
    return;
  }

  fallback.classList.add("hidden");

  data.forEach(r => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td class="truncate" title="${r.title}">${r.title}</td>
      <td>${r.cuisine || "-"}</td>
      <td>${renderStars(r.rating)}</td>
      <td>${r.total_time || 0} mins</td>
      <td>${r.serves || "-"}</td>
    `;
    row.onclick = () => openDrawer(r);
    body.appendChild(row);
  });

  renderPagination(total);
}

function openDrawer(r) {
  document.getElementById("drawer").classList.add("open");
  const n = r.nutrients || {};

  document.getElementById("drawerContent").innerHTML = `
    <h3>${r.title} <small>(${r.cuisine})</small></h3>

    <p><b>Description:</b> ${r.description || "-"}</p>

    <p>
      <b>Total Time:</b> ${r.total_time || 0} mins
      <button onclick="toggleTime()">▼</button>
    </p>

    <div id="timeBreakdown" class="hidden">
      <p>Prep Time: ${r.prep_time || 0} mins</p>
      <p>Cook Time: ${r.cook_time || 0} mins</p>
    </div>

    <h4>Nutrition</h4>
    <table class="nutrition">
      <tr><td>Calories</td><td>${n.calories || "-"}</td></tr>
      <tr><td>Carbohydrates</td><td>${n.carbohydrateContent || "-"}</td></tr>
      <tr><td>Cholesterol</td><td>${n.cholesterolContent || "-"}</td></tr>
      <tr><td>Fiber</td><td>${n.fiberContent || "-"}</td></tr>
      <tr><td>Protein</td><td>${n.proteinContent || "-"}</td></tr>
      <tr><td>Saturated Fat</td><td>${n.saturatedFatContent || "-"}</td></tr>
      <tr><td>Sodium</td><td>${n.sodiumContent || "-"}</td></tr>
      <tr><td>Sugar</td><td>${n.sugarContent || "-"}</td></tr>
      <tr><td>Fat</td><td>${n.fatContent || "-"}</td></tr>
    </table>
  `;
}

function toggleTime() {
  document.getElementById("timeBreakdown").classList.toggle("hidden");
}

function closeDrawer() {
  document.getElementById("drawer").classList.remove("open");
}

async function searchRecipes() {
  const params = new URLSearchParams();

  ["title", "cuisine", "rating", "total_time"].forEach(id => {
    const v = document.getElementById(id + "Search")?.value;
    if (v) params.append(id, v);
  });

  const res = await fetch(`/api/recipes/search?${params.toString()}`);
  const json = await res.json();
  renderTable(json.data || [], json.total || 0);
}

function renderPagination(total) {
  const pages = Math.ceil(total / currentLimit);
  document.getElementById("pagination").innerHTML = `
    <button ${currentPage === 1 ? "disabled" : ""} onclick="loadRecipes(${currentPage - 1})">Prev</button>
    Page ${currentPage} of ${pages}
    <button ${currentPage === pages ? "disabled" : ""} onclick="loadRecipes(${currentPage + 1})">Next</button>
    <select onchange="loadRecipes(1,this.value)">
      ${[15,25,50].map(n => `<option ${n===currentLimit?"selected":""}>${n}</option>`)}
    </select>
  `;
}
