
car_value_prediction_data = data['car_value_prediction']

car_predicted_price = car_value_prediction_data['predicted_car_price']
car_value_actual_price = car_value_prediction_data['user_inputted_car_price']

// price.toLocaleString('en-US', { style: 'currency', currency: 'USD' });

// Select the span element with class "value"
const predictedPriceSpan = document.querySelector('.predicted_price .value');
// Set its innerHTML to a new value
predictedPriceSpan.innerHTML = car_predicted_price.toLocaleString('en-US', { style: 'currency', currency: 'USD' });;
// Select the span element with class "value"
const actualPriceSpan = document.querySelector('.actual_price .value');
// Set its innerHTML to a new value
actualPriceSpan.innerHTML = car_value_actual_price.toLocaleString('en-US', { style: 'currency', currency: 'USD' });;

if (car_value_actual_price < car_predicted_price) {
    priceAssessmentLabel = 'Undervalued'
    priceAssessmentValue = car_predicted_price - car_value_actual_price
} else {
    priceAssessmentLabel = 'Overvalued'
    priceAssessmentValue = car_value_actual_price - car_predicted_price
}

// Select the span element with class "label"
const assessment_label_element = document.querySelector('.car_value_assessment .label');
// Set its innerHTML to a new value
assessment_label_element.innerHTML = priceAssessmentLabel

// Select the span element with class "value"
const assessment_value_element = document.querySelector('.car_value_assessment .value');
// Set its innerHTML to a new value
assessment_value_element.innerHTML = priceAssessmentValue.toLocaleString('en-US', { style: 'currency', currency: 'USD' });





deal_assessment = car_value_prediction_data['deal_assessment']

var header = document.querySelector('.model-header h2');
header.innerHTML = `Based on the information you provided, this car is a ${deal_assessment} deal!`


