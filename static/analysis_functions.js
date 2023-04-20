

console.log(data)
car_value_prediction_data = data['car_value_prediction']
console.log(car_value_prediction_data)
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



// Deal Assessment

// var deal_assessment = car_value_prediction_data['deal_assessment']
var actual_car_price = car_value_prediction_data['user_inputted_car_price']
var predicted_car_price = car_value_prediction_data['predicted_car_price']
var header = document.querySelector('.model-header h2');
var recommendation_div = document.getElementById('recommendation')
console.log(predicted_car_price)
console.log(actual_car_price)
if (predicted_car_price > actual_car_price) {
    var deal_assessment = 'undervalued'
    recommendation_div.innerHTML = `If you plan on selling this car, you should consider selling it at a higher price,
and if you plan on buying this car, you should consider buying it because it's a good price according to our model.`
} else {
    var deal_assessment = 'overvalued'
    recommendation_div.innerHTML = `If you plan on selling this car, you should consider selling it at a lower price,
and if you plan on buying this car, you should consider negotiating a lower price for it because it appears high according to our model.`
}
header.innerHTML = `Based on the information you provided, this car is ${deal_assessment}.`


console.log(data)

function get_explanation(variable, effect) {
    if (effect == '+') {
        effect = 'higher'
    } else if (effect == '-') {
        effect = 'lower'
    }
    if (variable == 'Title Status') {
        title_status = data['inputs']['car_title']
        return `Cars that have a ${title_status} generally have a ${effect} list price.`
    } else if (variable == 'Car Age') {
        car_years = data['inputs']['car_years']
        return `Cars from the year ${car_years} generally have a ${effect} list price.`
    } else if (variable == 'Car Miles') {
        car_miles = data['inputs']['car_miles']
        return `Cars that have driven ${car_miles} miles generally have a ${effect} list price.`
    } else if (variable == 'Car Condition') {
        car_condition = data['inputs']['car_condition']
        return `Cars that are in ${car_condition} condition generally have a ${effect} list price.`
    } else if (variable == 'Car Cylinders') {
        car_cylinders = data['inputs']['car_cylinders']
        return `Cars that have ${car_cylinders} generally have a ${effect} list price.`
    } else if (variable == 'Car Transmission') {
        car_transmission = data['inputs']['car_transmission']
        return `Cars that have ${car_transmission} transmission generally have a ${effect} list price.`
    } else if (variable == 'Car Drive') {
        car_drive = data['inputs']['car_drive']
        return `Cars that are ${car_drive} generally have a ${effect} list price.`
    } else if (variable == 'Car Type') {
        car_type = data['inputs']['car_type']
        return `Cars that are of the type ${car_type} generally have a ${effect} list price.`
    } else if (variable == 'Car Manufacturer') {
        car_manufacturer = data['inputs']['car_manufacturer']
        return `Cars that are made by ${car_manufacturer} generally have a ${effect} list price.`
    } else if (variable == 'Car Model') {
        car_model = data['inputs']['car_model']
        return `Cars that are of the model ${car_model} generally have a ${effect} list price.`
    }
}



function colorKeyVar(element) {
    if (element == '+') {
        return '#006400'
    } else if (element == '-') {
        return '#8b0000'
    }
}

// features
var kpi_variables = data['important_parameters']

var kpi_1_var = document.getElementById('kpi_1_variable');
kpi_1_var.innerHTML = kpi_variables[0]['variable']
var kpi_1_exp = document.getElementById('kpi_1_variable_exp');
kpi_1_exp.innerHTML = kpi_variables[0]['effect']
kpi_1_exp.style.backgroundColor = colorKeyVar(kpi_variables[0]['effect'])
var kpi_1_variable_explanation = document.getElementById('kpi_1_variable_explanation');
kpi_1_variable_explanation.innerHTML = get_explanation(kpi_variables[0]['variable'], kpi_variables[0]['effect'])

var kpi_2_var = document.getElementById('kpi_2_variable');
kpi_2_var.innerHTML = kpi_variables[1]['variable']
var kpi_2_exp = document.getElementById('kpi_2_variable_exp');
kpi_2_exp.innerHTML = kpi_variables[1]['effect']
kpi_2_exp.style.backgroundColor = colorKeyVar(kpi_variables[1]['effect'])
var kpi_2_variable_explanation = document.getElementById('kpi_2_variable_explanation');
kpi_2_variable_explanation.innerHTML = get_explanation(kpi_variables[1]['variable'], kpi_variables[1]['effect'])

var kpi_3_var = document.getElementById('kpi_3_variable');
kpi_3_var.innerHTML = kpi_variables[2]['variable']
var kpi_3_exp = document.getElementById('kpi_3_variable_exp');
kpi_3_exp.innerHTML = kpi_variables[2]['effect']
kpi_3_exp.style.backgroundColor = colorKeyVar(kpi_variables[2]['effect'])
var kpi_3_variable_explanation = document.getElementById('kpi_3_variable_explanation');
kpi_3_variable_explanation.innerHTML = get_explanation(kpi_variables[2]['variable'], kpi_variables[2]['effect'])

var kpi_4_var = document.getElementById('kpi_4_variable');
kpi_4_var.innerHTML = kpi_variables[3]['variable']
var kpi_4_exp = document.getElementById('kpi_4_variable_exp');
kpi_4_exp.innerHTML = kpi_variables[3]['effect']
kpi_4_exp.style.backgroundColor = colorKeyVar(kpi_variables[3]['effect'])
var kpi_4_variable_explanation = document.getElementById('kpi_4_variable_explanation');
kpi_4_variable_explanation.innerHTML = get_explanation(kpi_variables[3]['variable'], kpi_variables[3]['effect'])



// inputted car data
car_manufacturer = data['inputs']['car_manufacturer']
car_model = data['inputs']['car_model']
// car_type = data['inputs']['car_type']
var input_car_manufacturer_model_type = document.getElementById('input_car_manufacturer_model_type');
input_car_manufacturer_model_type.innerHTML = `${car_manufacturer} ${car_model}`

car_years = data['inputs']['car_years']
var inputted_car_year_text = document.getElementById('inputted_car_year_text');
inputted_car_year_text.innerHTML = `${car_years}`

car_miles = data['inputs']['car_miles']
var inputted_car_miles_text = document.getElementById('inputted_car_miles_text');
inputted_car_miles_text.innerHTML = `${car_miles}`

car_transmission = data['inputs']['car_transmission']
var inputted_car_transmission_text = document.getElementById('inputted_car_transmission_text');
inputted_car_transmission_text.innerHTML = `${car_transmission}`

car_cylinders = data['inputs']['car_cylinders']
var inputted_car_cylinders_text = document.getElementById('inputted_car_cylinders_text');
inputted_car_cylinders_text.innerHTML = `${car_cylinders}`

car_condition = data['inputs']['car_condition']
var inputted_car_condition_text = document.getElementById('inputted_car_condition_text');
inputted_car_condition_text.innerHTML = `${car_condition}`


// anomoly detection
anomoly_detection = data['anomoly_detection']
var car_anomoly_assessment = document.querySelector('.car_anomoly_assessment .value');
console.log(anomoly_detection)
if (anomoly_detection == 'True') {
    car_anomoly_assessment.innerHTML = 'Anomaly Detected!'
} else {
    car_anomoly_assessment.innerHTML = 'None Detected!'
}
