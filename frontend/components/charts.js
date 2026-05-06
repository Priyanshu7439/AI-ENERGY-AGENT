function renderSimulationChart(data) {
    const time = data.map(d => d.time);
    const demand = data.map(d => d.demand);

    new Chart(document.getElementById("simChart"), {
        type: "line",
        data: {
            labels: time,
            datasets: [
                { label: "Demand", data: demand }
            ]
        }
    });
}

function renderIoTChart(data) {
    new Chart(document.getElementById("iotChart"), {
        type: "line",
        data: {
            labels: data.map(d => d.time),
            datasets: [
                { label: "Power", data: data.map(d => d.power) }
            ]
        }
    });
}