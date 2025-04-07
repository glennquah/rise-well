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
        // bluetooth.uartWriteString("Easy level start!\n");
    }
    if (incomingMessage === "Medium") {
        difficulty = "Medium";
        // bluetooth.uartWriteString("Medium level start!\n");
    }
    if (incomingMessage === "Hard") {
        difficulty = "Hard";
        // bluetooth.uartWriteString("Hard level start!\n");
    }
    selectedThreshold = shakeThresholds.find(threshold => threshold.type === difficulty).code;
    shakeCount = selectedThreshold;
});


// bluetooth.onUartDataReceived(serial.delimiters(Delimiters.NewLine), function () {
//     let incomingMessage = bluetooth.uartReadUntil(serial.delimiters(Delimiters.NewLine));
//     incomingMessage = incomingMessage.substr(0, incomingMessage.length - 1)
//     basic.showString(incomingMessage)
//     if (incomingMessage === "Easy") {
//         difficulty = "Easy";
//         bluetooth.uartWriteString("Easy level selected\n");
//     } else if (incomingMessage === "Medium") {
//         difficulty = "Medium";
//         bluetooth.uartWriteString("Medium level selected\n");
//     } else if (incomingMessage === "Hard") {
//         difficulty = "Hard";
//         bluetooth.uartWriteString("Hard level selected\n");
//     }
// });

input.onGesture(Gesture.Shake, function () {
    if (gameOver) {
        init();
    };

    selectedThreshold--;
    // bluetooth.uartWriteString(shakeCount.toString());
    basic.showNumber(selectedThreshold);

    if (selectedThreshold === 0) {
        gameOver = true;
        // bluetooth.uartWriteString("Game Over\n");
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


