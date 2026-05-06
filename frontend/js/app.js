async function showSection(section) {
    const res = await fetch(`pages/${section}.html`);
    const html = await res.text();

    document.getElementById("content").innerHTML = html;

    if (section === "dashboard") {
        await loadScript("js/user.js");
        if (window.initUser) window.initUser();
    }

    if (section === "optimize") {
        await loadScript("js/user.js");
        if (window.initUser) window.initUser();
    }

    if (section === "simulation") {
        await loadScript("js/simulation.js");
        if (window.initSimulation) window.initSimulation();
    }

    if (section === "iot") {
        await loadScript("js/iot.js");
        if (window.initIoT) window.initIoT();
    }
}


// ✅ Proper async loader
function loadScript(src) {
    return new Promise((resolve, reject) => {
        // remove old script if exists
        const existing = document.querySelector(`script[src="${src}"]`);
        if (existing) existing.remove();

        const script = document.createElement("script");
        script.src = src;

        script.onload = () => resolve();
        script.onerror = () => reject();

        document.body.appendChild(script);
    });
}


// load default page
showSection("dashboard");