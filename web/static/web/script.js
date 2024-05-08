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

let datetime_range_check = false;
let current_start_datetime = moment().subtract(1800, 'seconds').startOf('seconds');
let datetime_diff = moment().diff(current_start_datetime, 'seconds');

function onDatetimeRangeChange(start_datetime, end_datetime) {
    datetime_range_check = true;
    current_start_datetime = start_datetime;
    datetime_diff = end_datetime.diff(start_datetime, 'seconds');
    if (!window.loop) {
        updateChartsByRange(start_datetime.format("YYYY-MM-DDTHH:mm:ss"), end_datetime.format("YYYY-MM-DDTHH:mm:ss"));
    }
}

const records_amount_input = document.getElementById('records-amount-input');
records_amount_input.addEventListener('change', () => {
    datetime_range_check = false;
    if (!window.loop) {
        console.log(records_amount_input.value);
        updateChartsByCount(records_amount_input.value);
    }
});

let marker;
let last_charts_data = [];

// Function to update all charts
function updateChartsByCount(records_amount=10) {
    if (records_amount < 3 || records_amount > 50) {
        return;
    }
    fetch(`/get_charts_data/${records_amount}/`)
    .then(response => response.json())
    .then(data => {
        if (JSON.stringify(data.charts_data) === JSON.stringify(last_charts_data)) {
            return;
        }
        last_charts_data = data.charts_data;
        data.charts_data.forEach((y_data, i) => {
            let x_data = data.x_data.map(datetime => new Date(datetime));

            charts[i].chart.load({
                columns: [
                    ['x', ...x_data],
                    [charts[i].label, ...y_data],
                ]
            });
        });
        if (data.coords.length > 0) {
            let coords = data.coords[0];
            let latitude = coords[0];
            let longitude = coords[1];
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
        }
    })
    .catch(error => console.error('Error:', error));
}

function updateChartsByRange(start_datetime, end_datetime) {
    fetch(`/charts_in_range/${start_datetime}/${end_datetime}/`)
    .then(response => response.json())
    .then(data => {
        if (JSON.stringify(data.charts_data) === JSON.stringify(last_charts_data)) {
            return;
        }
        last_charts_data = data.charts_data;
        data.charts_data.forEach((y_data, i) => {
            let x_data = data.x_data.map(datetime => new Date(datetime));

            charts[i].chart.load({
                columns: [
                    ['x', ...x_data],
                    [charts[i].label, ...y_data],
                ]
            });
        });
        if (data.coords.length > 0) {
            let coords = data.coords[0];
            let latitude = coords[0];
            let longitude = coords[1];
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
        }
    })
    .catch(error => console.error('Error:', error));
}

// Update the plot immediately when the page loads
updateChartsByCount();

// Start updating the plot every second
function startLoop() {
    if (window.loop) {
        return;
    }
    window.loop = setInterval(() => {
        if (datetime_range_check) {
            let current_end_datetime = moment();
            if (document.getElementById('datetime-range-check').checked){
                current_start_datetime = moment().subtract(datetime_diff, 'seconds');
                drp.setStartDate(current_start_datetime);
            }
            drp.setEndDate(current_end_datetime);
            drp.updateRanges({
                'Today': [moment().startOf('day'), moment().endOf('day')],
                'Last 1 Minute': [moment().subtract(60, 'seconds').startOf('seconds'), moment().endOf('seconds')],
                'Last 10 Minutes': [moment().subtract(600, 'seconds').startOf('seconds'), moment().endOf('seconds')],
                'Last 30 Minutes': [moment().subtract(1800, 'seconds').startOf('seconds'), moment().endOf('seconds')],
            });
            updateChartsByRange(current_start_datetime.format('YYYY-MM-DDTHH:mm:ss'), current_end_datetime.format('YYYY-MM-DDTHH:mm:ss'));
        } else {
            updateChartsByCount(records_amount_input.value);
        }
    }, 1000);
}

// Stop updating the plot
function stopLoop() {
    clearInterval(window.loop);
    window.loop = null;
}