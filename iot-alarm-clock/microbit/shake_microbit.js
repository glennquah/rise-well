let shakeCount = 0;
let gameOver = false;
let difficulty = "";
type Difficulty = "Easy" | "Medium" | "Hard";
let selectedThreshold = 0;

function init() {
    shakeCount = 0;
    gameOver = false;
    difficulty = "";
}

const shakeThresholds = [
    { type: "Easy", code: 5 },
    { type: "Medium", code: 10 },
    { type: "Hard", code: 15 }
];

// Read difficulty from USB Serial
serial.onDataReceived(serial.delimiters(Delimiters.NewLine), function () {
    let incomingMessage = serial.readUntil(serial.delimiters(Delimiters.NewLine));
    incomingMessage = incomingMessage.trim();

    if (incomingMessage === "Easy") {
        difficulty = "Easy";
    }
    if (incomingMessage === "Medium") {
        difficulty = "Medium";
    }
    if (incomingMessage === "Hard") {
        difficulty = "Hard";
    }

    let threshold = shakeThresholds.find(threshold => threshold.type === difficulty);
    if (threshold) {
        selectedThreshold = threshold.code;
    }

    shakeCount = selectedThreshold;
});

input.onGesture(Gesture.Shake, function () {
    if (gameOver) {
        init();
    }

    selectedThreshold--;
    basic.showNumber(selectedThreshold);

    if (selectedThreshold === 0) {
        gameOver = true;
        serial.writeLine(shakeCount.toString()); // Send final shake count over USB
        basic.showString("END");
    }
});


serial.redirect(SerialPin.USB_TX, SerialPin.USB_RX, BaudRate.BaudRate115200);
