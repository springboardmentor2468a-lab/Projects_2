let chart = null;

function predict() {
  const hours = Array.from({ length: 24 }, (_, i) => i);

  const bikeDemand = hours.map(() =>
    Math.floor(Math.random() * 300) + 20
  );

  const ctx = document.getElementById("chart").getContext("2d");

  if (chart) {
    chart.destroy();
  }

  chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: hours,
      datasets: [
        {
          label: "Predicted Bike Rentals",
          data: bikeDemand,
          backgroundColor: "red",
        },
      ],
    },
  });
}
