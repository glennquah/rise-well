let press_count = 0

input.onButtonPressed(Button.A, function () {
    press_count += 1
    basic.showNumber(press_count) 

    if (press_count >= 10) {
        serial.writeLine("m1,stop")
        press_count = 0  
        basic.showIcon(IconNames.Asleep) 
    }
})

serial.onDataReceived(serial.delimiters(Delimiters.NewLine), function () {
    let command = serial.readUntil(serial.delimiters(Delimiters.NewLine))
    if (command == "reset") {
        control.reset() 
    }
})

serial.redirect(SerialPin.USB_TX, SerialPin.USB_RX, BaudRate.BaudRate115200);

