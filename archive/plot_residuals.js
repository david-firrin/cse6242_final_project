
plot_data = data['plot_residuals']

var residuals = plot_data['residuals']
var y_train_hat = plot_data['y_train_hat']

function createData(xValues, yValues) {
    const data = xValues.map((x, index) => {
        return { x: x, y: yValues[index] };
    });
    return data;
}

data_residuals = createData(y_train_hat, residuals)

var residuals_plot = document.getElementById('residuals_model').getContext('2d');
var scatterChart = new Chart(residuals_plot, {
    type: 'scatter',
    data: {
        datasets: [{
            data: data_residuals,
            backgroundColor: 'rgba(255, 99, 132, 1)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1
        }]
    },
    options: {
        maintainAspectRatio: false,
        events: [],
        scales: {
            x: {
                display: true,
                title: {
                    display: true,
                    text: 'Predicted Value of Car'
                }
            },
            y: {
                display: true,
                title: {
                    display: true,
                    text: 'Residuals'
                }
            }
        },
        plugins: {
            legend: {
                display: false
            },
            title: {
                display: true,
                text: 'Residuals Versus Prediction',
                font: {
                    size: 18
                }
            },
        }
    }
});
