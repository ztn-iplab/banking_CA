console.log("🔥 Biometrics script loaded");

document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ DOM ready – starting biometric logger");

    let keystrokes = [];
    let mouseMoves = [];

    let keyPressTimestamps = {};
    let lastKeyUpTime = null;
    let lastKeyDownTime = null;

    let lastMouseX = null;
    let lastMouseY = null;
    let lastMouseTime = null;

    // ======== Keystroke Capture ========
    document.addEventListener("keydown", function (e) {
        const now = Date.now();

        if (!keyPressTimestamps[e.key]) {
            keyPressTimestamps[e.key] = now;
        }

        const flightTime = lastKeyUpTime ? now - lastKeyUpTime : 0;
        const upDownTime = lastKeyDownTime ? now - lastKeyDownTime : 0;
        lastKeyDownTime = now;

        keystrokes.push({
            key: e.key,
            event: "keydown",
            timestamp: now,
            rhythm: 0, // Will update on keyup
            dwell_time: 0,
            flight_time: flightTime,
            up_down_time: upDownTime
        });

        console.log(`🟡 KeyDown: ${e.key}`);
    });

    document.addEventListener("keyup", function (e) {
        const now = Date.now();
        const downTime = keyPressTimestamps[e.key];
        const dwellTime = downTime ? now - downTime : 0;
        const rhythm = dwellTime;

        lastKeyUpTime = now;

        for (let i = keystrokes.length - 1; i >= 0; i--) {
            if (keystrokes[i].key === e.key && keystrokes[i].event === "keydown" && keystrokes[i].dwell_time === 0) {
                keystrokes[i].dwell_time = dwellTime;
                keystrokes[i].rhythm = rhythm;
                break;
            }
        }

        delete keyPressTimestamps[e.key];

        console.log(`🔵 KeyUp: ${e.key} | Dwell: ${dwellTime}ms`);
    });

    // ======== Mouse Movement Capture ========
    document.addEventListener("mousemove", function (e) {
        const now = Date.now();
        let distance = 0;
        let speed = 0;
        let deltaX = 0;
        let deltaY = 0;

        if (lastMouseX !== null && lastMouseY !== null && lastMouseTime !== null) {
            deltaX = e.clientX - lastMouseX;
            deltaY = e.clientY - lastMouseY;
            distance = Math.sqrt(deltaX ** 2 + deltaY ** 2);

            const timeDiff = (now - lastMouseTime) / 1000;
            speed = timeDiff > 0 ? distance / timeDiff : 0;
        }

        lastMouseX = e.clientX;
        lastMouseY = e.clientY;
        lastMouseTime = now;

        mouseMoves.push({
            action: "move",
            coordinates: `${e.clientX},${e.clientY}`,
            button: "",
            delta: `${deltaX},${deltaY}`,
            distance: distance,
            speed: speed,
            timestamp: now
        });

        console.log(`🖱️ Mouse: (${e.clientX}, ${e.clientY}) | Δ: (${deltaX}, ${deltaY}) | Dist: ${distance.toFixed(2)} | Speed: ${speed.toFixed(2)} px/s`);
    });

    // ======== Send to Backend Every 5s ========
    setInterval(function () {
        if (keystrokes.length || mouseMoves.length) {
            console.log("📤 Sending biometric data:", {
                keystrokes: keystrokes.length,
                mouseMoves: mouseMoves.length
            });

            fetch("/api/biometrics/log", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                },
                body: JSON.stringify({
                    keystrokes: keystrokes,
                    mouse: mouseMoves,
                }),
            });

            keystrokes = [];
            mouseMoves = [];
        }
    }, 5000);

    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    }
});
