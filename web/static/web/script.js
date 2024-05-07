let charts = [
    {id: 'temperature-chart', label: 'Teplota', parent: 'other-panel'},
    {id: 'pressure-chart', label: 'Tlak', parent: 'other-panel'},
    {id: 'solar-radiation-chart', label: 'Solárne žiarenie', parent: 'solar-radiation-panel'},
    {id: 'altitude-chart', label: 'Nadmorská výška', parent: 'solar-radiation-panel'},
];

// Create charts
charts.forEach(chart => {
    chart_h2 = document.createElement('h2')
    chart_h2.innerHTML = chart.label
    document.getElementById(chart.parent).appendChild(chart_h2)

    chart_div = document.createElement('div')
    chart_div.id = chart.id
    chart_div.className = 'chart'
    document.getElementById(chart.parent).appendChild(chart_div)

    chart.chart = bb.generate({
        bindto: `#${chart.id}`,
        color: {
            pattern: ['#1f77b4']
        },
        data: {
            xs: {
                [chart.label]: 'x',
            },
            columns: [
                ['x'],
                [chart.label],
            ],
        },
        axis: {
            x: {
                type: 'timeseries',
                tick: {
                    rotate: 0,
                    format: '%H:%M:%S',
                    fit: false,
                    count: 5
                }
            }
        },
        legend: {
            show: false
        },              
    });
});

let start_datetime = document.getElementById('datetime-range-start');
let end_datetime = document.getElementById('datetime-range-end');
const datetime_range_check = document.getElementById('datetime-range-check');

start_datetime.addEventListener('change', onDatetimeChange);
end_datetime.addEventListener('change', onDatetimeChange);
datetime_range_check.addEventListener('change', onDatetimeChange);

function onDatetimeChange() {
    if (datetime_range_check.checked) {
        if (!window.loop) {
            updateChartsByRange(start_datetime.value, end_datetime.value);
        }
    }
    else {
        if (!window.loop) {
            updateChartsByCount();
        }
    }
}

const records_amount_input = document.getElementById('records-amount-input');
records_amount_input.addEventListener('change', () => {
    if (!window.loop) {
        updateChartsByCount();
    }
});

let marker;

// Function to update all charts
function updateChartsByCount() {
    let records_amount = records_amount_input.value;
    if (records_amount < 3 || records_amount > 50) {
        return;
    }
    fetch(`/get_charts_data/${records_amount}/`)
    .then(response => response.json())
    .then(data => {
        let coords = data.coords[data.coords.length-1];
        let latitude = coords[0];
        let longitude = coords[1];
        data.charts_data.forEach((y_data, i) => {
            let x_data = data.x_data.map(datetime => new Date(datetime));

            charts[i].chart.load({
                columns: [
                    ['x', ...x_data],
                    [charts[i].label, ...y_data],
                ]
            });
        });
        if (!marker) {
            console.log('Creating marker');
            console.log(latitude, longitude);
            marker = L.marker([latitude, longitude]).addTo(map);
        }
        else if (latitude>0 && longitude>0) {
            console.log('Updating marker');
            console.log(latitude, longitude);
            marker.setLatLng([latitude, longitude]);
        }
    })
    .catch(error => console.error('Error:', error));
}

function updateChartsByRange(start_datetime, end_datetime) {
    fetch(`/charts_in_range/${start_datetime}/${end_datetime}/`)
    .then(response => response.json())
    .then(data => {
        let coords = data.coords[data.coords.length-1];
        let latitude = coords[0];
        let longitude = coords[1];
        data.charts_data.forEach((y_data, i) => {
            let x_data = data.x_data.map(datetime => new Date(datetime));

            charts[i].chart.load({
                columns: [
                    ['x', ...x_data],
                    [charts[i].label, ...y_data],
                ]
            });
        });
        if (!marker) {
            console.log('Creating marker');
            console.log(latitude, longitude);
            marker = L.marker([latitude, longitude]).addTo(map);
        }
        else if (latitude>0 && longitude>0) {
            console.log('Updating marker');
            console.log(latitude, longitude);
            marker.setLatLng([latitude, longitude]);
        }
    })
    .catch(error => console.error('Error:', error));
}


// Update the plot immediately when the page loads
updateChartsByCount();

// Start updating the plot every second
function startLoop() {
    window.loop = setInterval(() => {
        if (datetime_range_check.checked) {
            updateChartsByRange(start_datetime.value, end_datetime.value);
        } else {
            updateChartsByCount();
        }
    }, 1000);
}

// Stop updating the plot
function stopLoop() {
    clearInterval(window.loop);
}