let charts = [
    {id: 'temperature-chart', label: 'Teplota', parent: 'other-panel'},
    {id: 'pressure-chart', label: 'Tlak', parent: 'other-panel'},
    {id: 'infrared-chart', label: 'Infračervené žiarenie', parent: 'solar-radiation-panel'},
    {id: 'ultraviolet-chart', label: 'Ultrafialové žiarenie', parent: 'solar-radiation-panel'},
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
                    rotate: -30,
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

const records_amount_input = document.getElementById('records-amount-input');
records_amount_input.addEventListener('change', () => {
    if (!window.loop) {
        updateCharts();
    }
});

// Function to update all charts
function updateCharts() {
    let records_amount = records_amount_input.value;
    if (records_amount < 3 || records_amount > 50) {
        return;
    }
    fetch(`/get_charts_data/${records_amount}/`)
    .then(response => response.json())
    .then(data => {
        data.charts_data.forEach((y_data, i) => {
            let x_data = data.x_data.map(datetime => new Date(datetime));

            charts[i].chart.load({
                columns: [
                    ['x', ...x_data],
                    [charts[i].label, ...y_data],
                ]
            });
        });
    })
    .catch(error => console.error('Error:', error));
}

// Update the plot immediately when the page loads
updateCharts();

// Start updating the plot every second
function startLoop() {
    window.loop = setInterval(updateCharts, 1000);
}

// Stop updating the plot
function stopLoop() {
    clearInterval(window.loop);
}