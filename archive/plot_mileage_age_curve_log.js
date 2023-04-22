
const ctx1 = document.getElementById('plot_mileage_age_curve_1').getContext('2d');

plot_data = data['plot_mileage_age_curves']


const plot_age_curve_log_x = plot_data['age_pd_X']
const plot_age_curve_log_y = plot_data['age_pd_log']

const plot_mileage_curve_log_x = plot_data['miles_pd_X']
const plot_mileage_curve_log_y = plot_data['miles_pd_log']

function createData(xValues, yValues) {
    const data = xValues.map((x, index) => {
        return { x: x, y: yValues[index] };
    });
    return data;
}

data_age_log = createData(plot_age_curve_log_x, plot_age_curve_log_y)
data_mileage_log = createData(plot_mileage_curve_log_x, plot_mileage_curve_log_y)



const plot_mileage_age_curve_1 = new Chart(ctx1, {
    type: 'line',
    data: {
        datasets: [{
            label: 'PD of Price on Miles',
            data: data_mileage_log,
            borderColor: 'rgb(255, 99, 132)',
            xAxisID: 'x-axis-1',
            tension: 0.1,
        }, {
            label: 'PD of Price on Car Age',
            data: data_age_log,
            borderColor: 'rgb(54, 162, 235)',
            xAxisID: 'x-axis-2',
            tension: 0.1,
        }, {
            label: 'Specific Point',
            data: [{ x: 10, y: 2 }],
            borderColor: 'rgb(255, 205, 86)',
            backgroundColor: 'rgb(255, 205, 86)',
            pointRadius: 20,
            pointHoverRadius: 8,
        }],
    },
    options: {
        maintainAspectRatio: false,
        scales: {
            'x-axis-1': {
                type: 'linear',
                position: 'bottom',
                ticks: {
                    min: 0,
                    max: 40,
                },
                title: {
                    display: true,
                    text: 'Number of Miles (in Thousands)'
                }
            },
            'x-axis-2': {
                type: 'linear',
                position: 'top',
                ticks: {
                    min: 0,
                    max: 30,
                },
                title: {
                    display: true,
                    text: 'Age of Car (in Years)'
                }
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Log Predicted Price of Used Car'
                }
            }
        },
        plugins: {
            title: {
                display: true,
                text: 'Partial Dependence of Price on Miles Driven for Used Cars',
                font: {
                    size: 16,
                }
            }
        }
    }
});