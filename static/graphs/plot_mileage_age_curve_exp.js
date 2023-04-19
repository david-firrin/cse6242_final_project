
const ctx2 = document.getElementById('plot_mileage_age_curve_exp').getContext('2d');

plot_data = data['plot_mileage_age_curves']

const df1_x = plot_data['age_pd_X']
const df1_y = plot_data['age_pd_exp']

const df2_x = plot_data['miles_pd_X']
const df2_y = plot_data['miles_pd_exp']

function createData(xValues, yValues) {
    const data = xValues.map((x, index) => {
        return { x: x, y: yValues[index] };
    });
    return data;
}

data_2_1 = createData(df1_x, df1_y)
data_2_2 = createData(df2_x, df2_y)
// console.log(data1)
// console.log(data2)


const plot_mileage_age_curve_2 = new Chart(ctx2, {
    type: 'line',
    data: {
        datasets: [
            // {
            //     label: "Your Car's PD of Price on Total Miles",
            //     data: [{
            //         x: plot_data['user_miles_PD']['user_input'],
            //         y: plot_data['user_miles_PD']['PD']
            //     }],
            //     borderColor: 'black',
            //     backgroundColor: 'rgb(255, 99, 132)',
            //     pointRadius: 6,
            //     pointHoverRadius: 8,
            // },
            // {
            //     label: "Your Car's PD of Price on Age",
            //     data: [{
            //         x: plot_data['user_car_age_PD']['user_input'],
            //         y: plot_data['user_car_age_PD']['PD']
            //     }],
            //     borderColor: 'black',
            //     backgroundColor: 'rgb(54, 162, 235)',
            //     pointRadius: 6,
            //     pointHoverRadius: 8,
            // },
            {
                label: 'PD of Price on Car Miles',
                data: data_2_1,
                borderColor: 'rgb(255, 99, 132)',
                xAxisID: 'x-axis-1',
                tension: 0.1,
            }, {
                label: 'PD of Price on Car Age',
                data: data_2_2,
                borderColor: 'rgb(54, 162, 235)',
                xAxisID: 'x-axis-2',
                tension: 0.1,
            },

        ],
    },
    options: {
        maintainAspectRatio: false,
        scales: {
            'x-axis-1': {
                type: 'linear',
                position: 'bottom',
                title: {
                    display: true,
                    color: 'white',
                    text: 'Number of Miles (in Thousands)',
                    font: {
                        size: 15
                    }
                }
            },
            'x-axis-2': {
                type: 'linear',
                position: 'top',
                title: {
                    display: true,
                    text: 'Age of Car (in Years)',
                    color: 'white',
                    font: {
                        size: 15
                    }
                }
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    color: 'white',
                    text: 'Multiplicative Effect on Used Car Price',
                    font: {
                        size: 15
                    }
                }
            }
        },
        plugins: {
            title: {
                display: true,
                color: 'white',
                text: ['Partial Dependence of Price on Miles Driven', 'and Age of Car'],
                font: {
                    size: 16,
                }
            }
        }
    }
});