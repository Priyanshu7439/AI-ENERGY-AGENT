window.initSimulation = function () {
    console.log("Simulation loaded");
};

window.runSimulation = async function () {
    try {
        const hours = document.getElementById("hours").value;

        const res = await fetch(`http://127.0.0.1:8000/simulate?hours=${hours}`);
        const result = await res.json();

        const data = result.data;

        const time = data.map(d => d.time);
        const demand = data.map(d => d.demand);
        const price = data.map(d => d.price);

        // CHARTS
        createChart("demandChart", time, demand, "Demand");
        createChart("priceChart", time, price, "Price");

        // AGENT LOG
        const log = document.getElementById("agentLog");
        log.innerHTML = "";
        data.forEach(d => {
            const li = document.createElement("li");
            li.textContent = `Hour ${d.time} → ${d.selected_agent}`;
            log.appendChild(li);
        });

        // INSIGHTS
        const peakDemand = Math.max(...demand);
        const peakHour = data.find(d => d.demand === peakDemand).time;

        const maxPrice = Math.max(...price);
        const priceHour = data.find(d => d.price === maxPrice).time;

        document.getElementById("simInsights").innerHTML = `
            <div class="card">
                <h3>📊 Key Insights</h3>
                <p>Peak demand at hour <b>${peakHour}</b></p>
                <p>Highest price at hour <b>${priceHour}</b></p>
                <p>Reduce usage during high price hours</p>
            </div>
        `;

    } catch (err) {
        console.error(err);
    }
};

function createChart(id, labels, data, label) {
    const ctx = document.getElementById(id);

    if (ctx.chart) ctx.chart.destroy();

    ctx.chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{ label: label, data: data }]
        }
    });
}