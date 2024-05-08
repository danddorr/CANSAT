let drp;
window.addEventListener("load", function (event) {
    drp = new DateRangePicker('datetimerange-input1',
        {
            timePicker: true,
            timePicker24Hour: true,
            timePickerSeconds: true,
            alwaysShowCalendars: true,
            showCustomRangeLabel: false,
            opens: 'center',
            startDate: moment().subtract(1800, 'seconds').startOf('seconds'),
            endDate: moment().endOf('seconds'),
            ranges: {
                'Today': [moment().startOf('day'), moment().endOf('day')],
                'Last 1 Minute': [moment().subtract(60, 'seconds').startOf('seconds'), moment().endOf('seconds')],
                'Last 10 Minutes': [moment().subtract(600, 'seconds').startOf('seconds'), moment().endOf('seconds')],
                'Last 30 Minutes': [moment().subtract(1800, 'seconds').startOf('seconds'), moment().endOf('seconds')],
            },
            locale: {
                format: "YYYY-MM-DD HH:mm:ss",
            }
        },
        function (start, end) {
            onDatetimeRangeChange(start, end);
        }
    );
});