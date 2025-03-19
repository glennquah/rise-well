let shakeCount = 0;
let gameOver = false;
let difficulty = '';
let selectedThreshold = 0;

bluetooth.startUartService();
bluetooth.setTransmitPower(7)

function init() {
    shakeCount = 0;
    gameOver = false;
    difficulty = '';
}
const shakeThresholds = [
    { type: 'easy', code: 5 },
    { type: 'medium', code: 10 },
    { type: 'hard', code: 15 }
]

bluetooth.onUartDataReceived(serial.delimiters(Delimiters.NewLine), function () {
    let incomingMessage = bluetooth.uartReadUntil(serial.delimiters(Delimiters.NewLine));
    incomingMessage = incomingMessage.substr(0, incomingMessage.length - 1)

    if (incomingMessage === "easy") {
        difficulty = "easy";
        bluetooth.uartWriteString("Easy level start!\n");
    }
    if (incomingMessage === "medium") {
        difficulty = "medium";
        bluetooth.uartWriteString("Medium level start!\n");
    }
    if (incomingMessage === "hard") {
        difficulty = "hard";
        bluetooth.uartWriteString("Hard level start!\n");
    }
    selectedThreshold = shakeThresholds.find(threshold => threshold.type === difficulty).code;
});

input.onGesture(Gesture.Shake, function () {
    if (gameOver) {
        init();
    };

    shakeCount += 1;
    bluetooth.uartWriteString("Shake count: " + shakeCount + "\n");
    basic.showNumber(shakeCount);

    if (shakeCount >= selectedThreshold) {
        gameOver = true;
        bluetooth.uartWriteString("Game Over\n");
        basic.showString("END");
    }
});

bluetooth.onBluetoothConnected(function () {
    basic.showIcon(IconNames.Giraffe)
})


bluetooth.onBluetoothDisconnected(function () {
    basic.showIcon(IconNames.No)
})


