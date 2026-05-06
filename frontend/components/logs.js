function renderLogs(data, elementId) {
    const log = document.getElementById(elementId);
    log.innerHTML = "";

    data.forEach(d => {
        const li = document.createElement("li");
        li.innerText = `Hour ${d.time}: ${d.selected_agent}`;
        log.appendChild(li);
    });
}