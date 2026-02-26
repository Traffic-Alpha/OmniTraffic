/* ============================================================
   Traffic VQA Web Test — Frontend JS
   ============================================================ */

// ---- Quiz page: option selection ----
function selectOption(key) {
  document.getElementById("selectedInput").value = key;
  
  // Enable next button if it exists
  const nextBtn = document.getElementById("nextBtn");
  if (nextBtn) nextBtn.disabled = false;

  document.querySelectorAll(".option-item").forEach((el) => {
    el.classList.toggle("selected", el.dataset.key === key);
  });
}

// ---- Quiz page: timer ----
let timerInterval = null;
let timerSeconds = 0;

function startTimer() {
  const timerEl = document.getElementById("timer");
  if (!timerEl) return;
  timerSeconds = 0;
  timerInterval = setInterval(() => {
    timerSeconds++;
    const m = Math.floor(timerSeconds / 60);
    const s = timerSeconds % 60;
    timerEl.textContent = m + ":" + String(s).padStart(2, "0");
  }, 1000);
}

// ---- Lightbox ----
function openLightbox(src) {
  const lb = document.getElementById("lightbox");
  const img = document.getElementById("lightboxImg");
  if (lb && img) {
    img.src = src;
    lb.classList.add("open");
  }
}

function closeLightbox() {
  const lb = document.getElementById("lightbox");
  if (lb) lb.classList.remove("open");
}

// Close on ESC
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeLightbox();
});

// ---- Result page: tabs ----
document.addEventListener("DOMContentLoaded", () => {
  // Tab switching
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const tab = btn.dataset.tab;
      document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
      document.querySelectorAll(".tab-content").forEach((c) => c.classList.remove("active"));
      btn.classList.add("active");
      const target = document.getElementById("tab-" + tab);
      if (target) target.classList.add("active");
    });
  });

  // Review filter
  document.querySelectorAll(".filter-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const filter = btn.dataset.filter;
      document.querySelectorAll(".filter-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      document.querySelectorAll(".review-item").forEach((item) => {
        const isCorrect = item.dataset.correct === "yes";
        if (filter === "all") {
          item.style.display = "";
        } else if (filter === "correct") {
          item.style.display = isCorrect ? "" : "none";
        } else {
          item.style.display = isCorrect ? "none" : "";
        }
      });
    });
  });
});

// ---- Result page: charts ----
function initResultPage(chartData) {
  const chartConfigs = [
    { id: "chartCategory", data: chartData.category },
    { id: "chartTask", data: chartData.task },
    { id: "chartSubtask", data: chartData.subtask },
    { id: "chartCapability", data: chartData.capability },
  ];

  chartConfigs.forEach(({ id, data }) => {
    const canvas = document.getElementById(id);
    if (!canvas || !data) return;

    const accuracy = data.total.map((t, i) =>
      t > 0 ? Math.round((data.correct[i] / t) * 1000) / 10 : 0
    );

    new Chart(canvas, {
      type: "bar",
      data: {
        labels: data.labels,
        datasets: [
          {
            label: "Correct",
            data: data.correct,
            backgroundColor: "rgba(37, 99, 235, 0.7)",
            borderRadius: 4,
          },
          {
            label: "Wrong",
            data: data.total.map((t, i) => t - data.correct[i]),
            backgroundColor: "rgba(220, 38, 38, 0.25)",
            borderRadius: 4,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: "top" },
          tooltip: {
            callbacks: {
              afterBody: (ctx) => {
                const idx = ctx[0].dataIndex;
                return `Accuracy: ${accuracy[idx]}%`;
              },
            },
          },
        },
        scales: {
          x: { stacked: true },
          y: { stacked: true, beginAtZero: true, ticks: { stepSize: 1 } },
        },
      },
    });
  });
}

