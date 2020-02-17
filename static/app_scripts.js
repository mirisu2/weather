function show_temp(labels, temp, feels_like){
    let ctx1 = document.getElementById('temp').getContext('2d');
    let myChart1 = new Chart(ctx1, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Температура',
                backgroundColor: 'rgba(51, 112, 183, 1.0)',
                borderColor: 'rgba(51, 112, 183, 1.0)',
                data: temp,
                fill: false,
            },{
                label: 'Ощущаемая температура',
                backgroundColor: 'rgba(26, 8, 241, 1.0)',
                borderColor: 'rgba(26, 8, 241, 1.0)',
                data: feels_like,
                fill: false,
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    display: true,
                    ticks: {
                        callback: function(value, index, values) {
                            return  value + ' °C';
                        }
                    }
                }]
            }
        }
    });
}

function show_pressure(labels, pressure){
    let ctx2 = document.getElementById('pressure').getContext('2d');
    let myChart2 = new Chart(ctx2, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Давление',
                backgroundColor: 'rgba(229, 66, 232, 0.2)',
                borderColor: 'rgba(229, 66, 232, 0.5)',
                data: pressure
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    display: true,
                    ticks: {
                        callback: function(value, index, values) {
                            return  value + ' мм рт. ст.';
                        }
                    }
                }]
            }
        }
    });
}

function show_humidity(labels, humidity){
    let ctx2 = document.getElementById('humidity').getContext('2d');
    let myChart2 = new Chart(ctx2, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Влажность воздуха',
                backgroundColor: 'rgba(114, 226, 151, 0.2)',
                borderColor: 'rgba(114, 226, 151, 0.5)',
                data: humidity
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    display: true,
                    ticks: {
                        callback: function(value, index, values) {
                            return  value + ' %';
                        }
                    }
                }]
            }
        }
    });
}

function get_data_for_chart(data){
    if (data.length > 0) {

        let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {

                let res = JSON.parse(this.responseText);
                if (res['status'] == true) {
                    show_temp(res['labels'], res['temp'], res['feels_like']);
                    show_pressure(res['labels'], res['pressure']);
                    show_humidity(res['labels'], res['humidity']);

                }
            }
        }
        xhttp.open("GET", "/api/weather/" + data, true);
        xhttp.send();
    }
}
