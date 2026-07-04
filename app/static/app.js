const form = document.querySelector("#advisor-form");
const resultTitle = document.querySelector("#result-title");
const confidence = document.querySelector("#confidence");
const cost = document.querySelector("#cost");
const architecture = document.querySelector("#architecture");
const alternatives = document.querySelector("#alternatives");
const diagram = document.querySelector("#diagram");
const diagramCode = document.querySelector("#diagram-code");
const copyDiagram = document.querySelector("#copy-diagram");

const labels = {
  compute: "Compute",
  storage: "Storage",
  networking: "Networking",
  deployment: "Deployment",
  availability: "Availability",
};

function payloadFromForm() {
  const data = new FormData(form);

  return {
    project_name: data.get("project_name"),
    cpu: Number(data.get("cpu")),
    ram_gb: Number(data.get("ram_gb")),
    gpu_required: data.get("gpu_required") === "on",
    storage_gb: Number(data.get("storage_gb")),
    daily_users: Number(data.get("daily_users")),
    traffic_level: data.get("traffic_level"),
    budget: data.get("budget"),
    deployment_preference: data.get("deployment_preference"),
    availability: data.get("availability"),
  };
}

function renderArchitecture(items) {
  architecture.innerHTML = "";

  Object.entries(items).forEach(([key, value]) => {
    const card = document.createElement("article");
    card.className = "recommendation-card";
    card.innerHTML = `
      <h3>${labels[key] || key}</h3>
      <p>${value.recommendation}</p>
      <p>${value.reason}</p>
      <p class="tradeoff">${value.tradeoffs}</p>
    `;
    architecture.appendChild(card);
  });
}

function nodeLabel(line) {
  const match = line.match(/\[([^\]]+)\]/);
  return match ? match[1] : line.trim();
}

function renderDiagram(code) {
  const lines = code.split("\n").filter((line) => line.includes("-->"));
  const nodes = [];

  lines.forEach((line) => {
    const [left, right] = line.split("-->");
    const leftLabel = nodeLabel(left);
    const rightLabel = nodeLabel(right);

    if (!nodes.includes(leftLabel)) {
      nodes.push(leftLabel);
    }
    if (!nodes.includes(rightLabel)) {
      nodes.push(rightLabel);
    }
  });

  diagram.innerHTML = "";
  nodes.forEach((node, index) => {
    const item = document.createElement("div");
    item.className = "diagram-node";
    item.textContent = node;
    diagram.appendChild(item);

    if (index < nodes.length - 1) {
      const arrow = document.createElement("div");
      arrow.className = "diagram-arrow";
      arrow.textContent = ">";
      diagram.appendChild(arrow);
    }
  });

  diagramCode.textContent = code;
}

function renderAlternatives(items) {
  alternatives.innerHTML = "";

  items.forEach((item) => {
    const card = document.createElement("article");
    card.className = "alternative";
    card.innerHTML = `
      <strong>${item.name}</strong>
      <p>${item.description}</p>
      <p>$${item.estimated_monthly_cost_usd}/mo</p>
      <p>${item.best_for}</p>
    `;
    alternatives.appendChild(card);
  });
}

function renderResult(data) {
  resultTitle.textContent = data.project_name;
  confidence.textContent = `${Math.round(data.confidence_score * 100)}%`;
  cost.textContent = `$${data.estimated_monthly_cost.min_usd} - $${data.estimated_monthly_cost.max_usd}`;
  renderArchitecture(data.recommended_architecture);
  renderDiagram(data.architecture_diagram);
  renderAlternatives(data.alternatives);
}

async function generateRecommendation() {
  resultTitle.textContent = "Generating recommendation";

  const response = await fetch("/recommend", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payloadFromForm()),
  });

  if (!response.ok) {
    resultTitle.textContent = "Request failed";
    throw new Error(`Request failed with status ${response.status}`);
  }

  const data = await response.json();
  renderResult(data);
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  generateRecommendation().catch((error) => {
    console.error(error);
  });
});

copyDiagram.addEventListener("click", async () => {
  await navigator.clipboard.writeText(diagramCode.textContent);
  copyDiagram.textContent = "Copied";
  setTimeout(() => {
    copyDiagram.textContent = "Copy Mermaid";
  }, 1200);
});

generateRecommendation();
