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

    let sessionStart = Date.now();

    // ======== Keystroke Capture ========
    document.addEventListener("keydown", function (e) {
        const now = Date.now();
        const timestamp = new Date().toISOString();

        if (!keyPressTimestamps[e.key]) {
            keyPressTimestamps[e.key] = now;
        }

        const flightTime = lastKeyUpTime ? (now - lastKeyUpTime) / 1000 : 0;
        const upDownTime = lastKeyDownTime ? (now - lastKeyDownTime) / 1000 : 0;
        lastKeyDownTime = now;

        const sessionDuration = (now - sessionStart) / 1000;

        keystrokes.push({
            key: e.key,
            event: "press",
            timestamp: timestamp,
            rhythm: 0,
            dwell_time: 0,
            flight_time: flightTime,
            up_down_time: upDownTime,
            session_duration: sessionDuration
        });

        console.log(`🟡 KeyDown: ${e.key}`);
    });

    document.addEventListener("keyup", function (e) {
        const now = Date.now();
        const downTime = keyPressTimestamps[e.key];
        const dwellTime = downTime ? (now - downTime) / 1000 : 0;
        const rhythm = dwellTime;
        const timestamp = new Date().toISOString();
        const sessionDuration = (now - sessionStart) / 1000;

        lastKeyUpTime = now;

        // Update existing keydown
        for (let i = keystrokes.length - 1; i >= 0; i--) {
            if (keystrokes[i].key === e.key && keystrokes[i].event === "press" && keystrokes[i].dwell_time === 0) {
                keystrokes[i].dwell_time = dwellTime;
                keystrokes[i].rhythm = rhythm;
                break;
            }
        }

        // Log the release event
        keystrokes.push({
            key: e.key,
            event: "release",
            timestamp: timestamp,
            rhythm: rhythm,
            dwell_time: dwellTime,
            flight_time: 0,
            up_down_time: 0,
            session_duration: sessionDuration
        });

        delete keyPressTimestamps[e.key];

        console.log(`🔵 KeyUp: ${e.key} | Dwell: ${dwellTime.toFixed(3)}s`);
    });

    // ======== Mouse Movement Capture ========
    document.addEventListener("mousemove", function (e) {
        const now = Date.now();
        const timestamp = new Date().toISOString();
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
            timestamp: timestamp
        });

        console.log(`🖱️ Move: (${e.clientX}, ${e.clientY}) | Δ: (${deltaX}, ${deltaY}) | Dist: ${distance.toFixed(2)} | Speed: ${speed.toFixed(2)} px/s`);
    });

    // ======== Mouse Click Capture ========
    document.addEventListener("click", function (e) {
        const timestamp = new Date().toISOString();
    
        let button;
        switch (e.button) {
            case 0:
                button = "left";
                break;
            case 1:
                button = "middle";
                break;
            case 2:
                button = "right";
                break;
            default:
                button = "unknown";
        }
    
        console.log("🖱️ Captured Click Event:", {
            coordinates: `${e.clientX},${e.clientY}`,
            button: button,
            rawButton: e.button,
            timestamp: timestamp
        });
    
        mouseMoves.push({
            action: "click",
            coordinates: `${e.clientX},${e.clientY}`,
            button: button,
            delta: "0,0",
            distance: 0,
            speed: 0,
            timestamp: timestamp
        });
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
