let cur_cmd = "";

function onTouchStart(value, butt) {
    console.log(typeof value, "type value");
    console.log(typeof butt, "type button");
    cur_cmd = value;
}

function onTouchEnd(value, button) {
    cur_cmd = "";
}

let io_characteristic;

function connect(butt) {
    navigator.bluetooth.requestDevice({
        filters: [{ services: ['c5f50001-8280-46da-89f4-6d8051e4aeef'] }],
        optionalServices: [
            'c5f50001-8280-46da-89f4-6d8051e4aeef',
            0x180a,
            '6e400001-b5a3-f393-e0a9-e50e24dcca9e',
        ],
    })

        .then(device => { console.log("connected."); return device.gatt.connect(); })
        .then(server => {
            server.getPrimaryServices().then(services => console.log(services));
            console.log(server);
            return server.getPrimaryService('c5f50001-8280-46da-89f4-6d8051e4aeef');
        }).then(service => {
            console.log(service);
            return service.getCharacteristic('c5f50002-8280-46da-89f4-6d8051e4aeef');
        })
        .then(characteristic => {
            return characteristic.startNotifications();
        }).then(characteristic => {
            io_characteristic = characteristic;
            characteristic.addEventListener('characteristicvaluechanged',
                handleCharacteristicValueChanged);
            console.log('Notifications have been started.');
        }).catch(error => { console.error(error); });

    function handleCharacteristicValueChanged(event) {
        const value = event.target.value;
        const decoder = new TextDecoder();
        const str = decoder.decode(value);
        if (str[0] == '\x01') {
            let payload = str.substring(1);
            console.log('Received ' + payload);
            if (payload == "rdy") {
                run();
            }
        }
    }



    // if (butt.classList.contains("blue-button")) {
    //     butt.classList.remove("blue-button");
    //     butt.classList.add("red-button");
    //     document.getElementById("sportele").innerHTML = "SPORT OFF"
    //     document.getElementById("sportele").style.color = "#f00c0c";
    //     value = "10";
    // } else {
    //     butt.classList.remove("red-button");
    //     butt.classList.add("blue-button");
    //     document.getElementById("sportele").innerHTML = "SPORT ON"
    //     document.getElementById("sportele").style.color = "#5c5cff";
    //     value = "9";
    // }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
async function run() {
    var enc = new TextEncoder();
    while (true) {
        console.log("send cmd", cur_cmd);

        await io_characteristic.writeValue(enc.encode("\x06" + cur_cmd + "\n"))
            .then(_ => {
                console.log('Energy expended has been reset.');
            })
            .catch(error => { console.error(error); });
        await sleep(20);
    }

}
document.getElementById("mainTable").addEventListener("touchend", function (event) {
    event.preventDefault()
});  