const API = "http://127.0.0.1:8000";

let lastData = null;
let lastResponse = null;
let chartInstance = null;
let compareChart = null;
let trendChart = null;

/* ================= DOM CACHE ================= */

const units = document.getElementById("units");
const bill = document.getElementById("bill");
const prediction = document.getElementById("prediction");
const temp = document.getElementById("temp");
const score = document.getElementById("score");

const insights = document.getElementById("insights");
const costBreakdown = document.getElementById("costBreakdown");
const projection = document.getElementById("projection");

const actions = document.getElementById("actions");
const agentTrace = document.getElementById("agentTrace");
const weatherImpact = document.getElementById("weatherImpact");
const aiSummary = document.getElementById("aiSummary");

const optDevice = document.getElementById("optDevice");
const optHours = document.getElementById("optHours");
const whatif = document.getElementById("whatif");

/* ================= INPUT ================= */

function getInput() {
    return {
        state: state.value,
        appliances: {
            fan: { hours: +fan.value || 0 },
            ac: { hours: +ac.value || 0 },
            lights: { hours: +lights.value || 0 },
            fridge: { hours: +fridge.value || 0 },
            tv: { hours: +tv.value || 0 },
            washing_machine: { hours: +washing_machine.value || 0 },
            geyser: { hours: +geyser.value || 0 }
        }
    };
}

/* ================= HISTORY ================= */

function saveHistory(data, result) {
    const history = JSON.parse(localStorage.getItem("energy_history") || "[]");

    history.push({
        timestamp: Date.now(),
        input: data,
        bill: result.bill,
        optimized: result.optimized_bill
    });

    if (history.length > 10) history.shift();

    localStorage.setItem("energy_history", JSON.stringify(history));
}

/* ================= LEARNING ================= */

function learnUsagePattern() {
    const history = JSON.parse(localStorage.getItem("energy_history") || "[]");

    if (history.length < 3) return null;

    let totalUsage = 0;
    let totalBill = 0;

    history.forEach(h => {
        totalBill += h.bill;

        let usage = 0;
        Object.values(h.input.appliances).forEach(a => {
            usage += a.hours;
        });

        totalUsage += usage;
    });

    const avgUsage = totalUsage / history.length;
    const avgBill = totalBill / history.length;

    return {
        avgUsage,
        avgBill,
        costPerHour: avgBill / avgUsage
    };
}

/* ================= MAIN ================= */

window.analyzeUser = async function () {
    try {
        const data = getInput();
        lastData = data;

        const res = await fetch(`${API}/analyze`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        });

        if (!res.ok) throw new Error(await res.text());

        const r = await res.json();
        lastResponse = r;

        saveHistory(data, r);

        /* KPI */
        units.innerText = r.units?.toFixed(1) || "--";
        bill.innerText = "₹" + r.bill;
        prediction.innerText = "₹" + r.prediction;
        temp.innerText = r.temperature ? r.temperature + "°C" : "--";
        score.innerText = calculateScore(r.bill);

        /* WEATHER */
        weatherImpact.innerHTML = getWeatherMessage(r.temperature);

        /* UI */
        renderInsights(r);
        renderActions(r.cost_breakdown, r.bill);
        renderAISummary(r);

        if (r.agent_trace?.length) {
            renderAgentTrace(r.agent_trace);
        }

        renderChart(r.breakdown);
        renderCost(r.cost_breakdown);
        renderProjection(r);
        renderComparison(r.bill, r.optimized_bill || r.bill);
        renderTrendChart();

        const sorted = Object.entries(r.cost_breakdown || {})
            .sort((a,b)=>b[1]-a[1]);

        if (sorted.length) optDevice.value = sorted[0][0];

    } catch (err) {
        console.error("FULL ERROR:", err);
        alert("Check console + backend logs");
    }
};

/* ================= TREND GRAPH ================= */

function renderTrendChart() {
    const history = JSON.parse(localStorage.getItem("energy_history") || "[]");
    if (history.length < 2) return;

    const ctx = document.getElementById("trendChart");
    if (!ctx) return;

    if (trendChart) trendChart.destroy();

    trendChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: history.map((_, i) => `Run ${i+1}`),
            datasets: [{
                data: history.map(h => h.bill)
            }]
        }
    });
}

/* ================= AI SUMMARY ================= */

function renderAISummary(r) {
    if (!aiSummary) return;

    const learning = learnUsagePattern();

    let text = `
Optimized Bill: ₹${r.optimized_bill}
Savings: ₹${(r.bill - r.optimized_bill).toFixed(0)}/month
`;

    if (learning) {
        text += `
📊 Learned Pattern:
Avg usage: ${learning.avgUsage.toFixed(1)} hrs
Cost/hour: ₹${learning.costPerHour.toFixed(2)}
`;
    }

    aiSummary.innerText = text;
}

/* ================= REST (UNCHANGED CORE) ================= */

function renderChart(data) {
    const ctx = document.getElementById("chart");
    if (!ctx) return;

    if (chartInstance) chartInstance.destroy();

    chartInstance = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: Object.keys(data || {}),
            datasets: [{ data: Object.values(data || {}) }]
        }
    });
}

function renderInsights(r) {
    if (!insights) return;

    const sorted = Object.entries(r.cost_breakdown || {})
        .sort((a,b)=>b[1]-a[1]);

    if (!sorted.length) return;

    insights.innerHTML = `
        <div class="insight-box">⚡ ${sorted[0][0]} highest → ₹${sorted[0][1]}</div>
        <div class="insight-box">📉 Optimized → ₹${r.optimized_bill}</div>
    `;
}

function renderCost(data) {
    if (!costBreakdown) return;

    costBreakdown.innerHTML = "";

    Object.entries(data || {})
        .sort((a,b)=>b[1]-a[1])
        .forEach(([k,v]) => {
            costBreakdown.innerHTML += `
                <div class="cost-row">
                    <span>${k}</span>
                    <span>₹${v}</span>
                </div>
            `;
        });
}

function renderProjection(r) {
    projection.innerHTML = `
        <div class="projection-box">Daily → ₹${r.daily_bill}</div>
        <div class="projection-box">Monthly → ₹${r.monthly_bill}</div>
        <div class="projection-box">Yearly → ₹${r.yearly_bill}</div>
    `;
}

window.autoOptimize = function () {

    if (!lastData || !lastResponse) {
        alert("Run analysis first");
        return;
    }

    if (!lastResponse.optimized_plan) {
        alert("No optimized plan available");
        return;
    }

    const plan = lastResponse.optimized_plan;

    for (let key in plan) {

        const el = document.getElementById(key);

        if (el && plan[key].hours !== undefined) {
            el.value = plan[key].hours.toFixed(1);
        }
    }

    whatif.innerHTML = `
        <div class="whatif-box">
            ⚡ Best AI optimization applied successfully
        </div>
    `;
};

function renderActions(costData, totalBill) {
    if (!actions) return;

    const sorted = Object.entries(costData || {})
        .sort((a,b)=>b[1]-a[1]);

    let html = "";

    sorted.slice(0,3).forEach(([d,c])=>{
        html += `<div class="action-item">⚡ Reduce ${d} → save ₹${Math.round(c*0.2)}</div>`;
    });

    actions.innerHTML = html;
}

function renderAgentTrace(trace) {
    agentTrace.innerHTML = trace.map(s =>
        `<div class="trace-step">Step ${s.step}: ${s.action} → ₹${s.bill}</div>`
    ).join("");
}

function renderComparison(oldBill, newBill) {
    const ctx = document.getElementById("compareChart");
    if (!ctx) return;

    if (compareChart) compareChart.destroy();

    compareChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Current", "Optimized"],
            datasets: [{ data: [oldBill, newBill] }]
        }
    });
}

function calculateScore(bill) {
    if (bill < 1000) return "🔥 Excellent";
    if (bill < 2000) return "⚡ Good";
    if (bill < 3000) return "⚠️ High";
    return "❌ Very High";
}

function getWeatherMessage(temp) {
    if (!temp) return "No weather data";
    if (temp > 35) return "🔥 High temp";
    if (temp > 30) return "🌤 Moderate";
    return "❄️ Low usage";
}