let shakeCount = 0;
let gameOver = false;
let difficulty = '';
type Difficulty = 'Easy' | 'Medium' | 'Hard';
let selectedThreshold = 0;

bluetooth.startUartService();
bluetooth.setTransmitPower(7)

function init() {
    shakeCount = 0;
    gameOver = false;
    difficulty = '';
}
const shakeThresholds = [
    { type: 'Easy', code: 5 },
    { type: 'Medium', code: 10 },
    { type: 'Hard', code: 15 }
]

bluetooth.onUartDataReceived(serial.delimiters(Delimiters.NewLine), function () {
    let incomingMessage = bluetooth.uartReadUntil(serial.delimiters(Delimiters.NewLine));
    incomingMessage = incomingMessage.substr(0, incomingMessage.length - 1)

    if (incomingMessage === "Easy") {
        difficulty = "Easy";
    }
    if (incomingMessage === "Medium") {
        difficulty = "Medium";
    }
    if (incomingMessage === "Hard") {
        difficulty = "Hard";
    }
    selectedThreshold = shakeThresholds.find(threshold => threshold.type === difficulty).code;
    shakeCount = selectedThreshold;
});

input.onGesture(Gesture.Shake, function () {
    if (gameOver) {
        init();
    };

    selectedThreshold--;
    basic.showNumber(selectedThreshold);

    if (selectedThreshold === 0) {
        gameOver = true;
        bluetooth.uartWriteString(shakeCount.toString());
        basic.showString("END");
    }
});

bluetooth.onBluetoothConnected(function () {
    basic.showIcon(IconNames.Giraffe)
})


bluetooth.onBluetoothDisconnected(function () {
    basic.showIcon(IconNames.No)
})


