function predict() {

    document.getElementById("result").innerText =
        "Bike Rental Forecast for next 5 days";

    const ctx = document.getElementById("myChart");

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ["06/03", "07/03", "08/03", "09/03", "10/03"],
            datasets: [{
                label: 'Predicted Rentals',
                data: [400, 450, 500, 520, 600]
            }]
        }
    });
}
