let pastTime = input.runningTime()
let delay = 0
let limit = 15
let buffer: number[] = []
let prerun = 0
let prerunLimit = 5
let tresholdDone = false

basic.forever(()=>{
    if (pins.analogReadPin(DigitalPin.P1) > 650) {
        if (prerun<prerunLimit){
            prerun +=1
        }else if (tresholdDone){
            basic.showIcon(IconNames.Heart)

            delay +=1
            let currentTime = input.runningTime()
            let interval = currentTime - pastTime
            buffer.push(interval)
            pastTime = currentTime

            if (delay > limit) {
                delay = 0
                let sum = 0
                for (let i = 0; i < buffer.length; i++) {
                    sum += 60000 / buffer[i]
                }
                let hearRateAvg = sum/buffer.length
                serial.writeLine(hearRateAvg.toString())
                buffer = []
            }
        }else{
            pause(100) // delay to be sure it's not due to noise
            tresholdDone = true
        }
    }else{
        tresholdDone = false
        basic.clearScreen()
    }
})