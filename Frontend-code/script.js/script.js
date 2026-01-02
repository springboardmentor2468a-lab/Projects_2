let hourChart = null;
let dayChart = null;

/* Populate Years */
function populateYears() {
  for (let y = 2011; y <= 2026; y++) {
    hourYear.innerHTML += `<option>${y}</option>`;
    dayYear.innerHTML += `<option>${y}</option>`;
  }
}
populateYears();

/* Navigation */
function scrollToApp() {
  app.scrollIntoView({ behavior: "smooth" });
}

function showHour() {
  hourSection.classList.remove("hidden");
  daySection.classList.add("hidden");
}

function showDay() {
  daySection.classList.remove("hidden");
  hourSection.classList.add("hidden");
}

/* HOUR-WISE */
function predictHour() {
  const ctx = document.getElementById("hourChart").getContext("2d");

  const start = Number(hour.value);
  const temp = Number(hourTemp.value);
  const hum = Number(hourHum.value);
  const wind = Number(hourWind.value);
  const holiday = Number(hourHoliday.value);

  let labels = [];
  let data = [];

  for (let i = 1; i <= 6; i++) {
    labels.push(`Hour ${(start + i) % 24}`);
    data.push(Math.round(90 + i*12 + temp*50 - hum*35 - wind*25 - holiday*15));
  }

  if (hourChart) hourChart.destroy();

  hourChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Predicted Rentals",
        data,
        backgroundColor: "#0072ff"
      }]
    },
    options: {
      plugins: {
        datalabels: {
          color: "#000",
          anchor: "end",
          align: "top",
          font: { weight: "bold" }
        }
      },
      scales: { y: { beginAtZero: true } }
    },
    plugins: [ChartDataLabels]
  });
}

/* DAY-WISE */
function predictDay() {
  const ctx = document.getElementById("dayChart").getContext("2d");

  const temp = Number(dayTemp.value);
  const hum = Number(dayHum.value);
  const wind = Number(dayWind.value);
  const work = Number(dayWork.value);

  let labels = ["Day +1","Day +2","Day +3","Day +4","Day +5","Day +6"];
  let data = labels.map((_, i) =>
    Math.round(130 + i*18 + temp*60 - hum*40 - wind*30 + work*20)
  );

  if (dayChart) dayChart.destroy();

  dayChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Predicted Rentals",
        data,
        backgroundColor: "#00c6ff"
      }]
    },
    options: {
      plugins: {
        datalabels: {
          color: "#000",
          anchor: "end",
          align: "top",
          font: { weight: "bold" }
        }
      },
      scales: { y: { beginAtZero: true } }
    },
    plugins: [ChartDataLabels]
  });
}
