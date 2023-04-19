

// Get the form_data page to validate the free-text inputs
function handleNext(event) {
    event.preventDefault(); // prevent the form from submitting normally
    var form = document.getElementById("my-form");
    // console.log(form)
    // Get the Button value
    var button_name = document.getElementById('next-page-btn').name

    // create an object to hold the form data
    var formData = new FormData(form);
    // console.log(formData);
    formData.append('page', button_name)
    formData.append('direction', 'next')
    // console.log(formData)

    if (form.name == 'car_miles') {
        inputted_value = formData.get('my-form')
        const pattern = /^[0-9]+$/;
        if (!pattern.test(inputted_value)) {
            var prompt_instructions = document.getElementById("prompt_instructions")
            prompt_instructions.innerHTML = "Please enter a valid number for how many miles there are on your car."
            prompt_instructions.style.color = 'red';
            var input_box = document.getElementById("input_number");
            input_box.style.border = '3px solid red';
        } else {
            inputted_value = parseFloat(inputted_value)
            formData.set('my-form', inputted_value)
            nextPage(formData)
        }
    } else if (form.name == 'car_value') {
        inputted_value = formData.get('my-form')
        const pattern = /^[0-9]+$/;
        if (!pattern.test(inputted_value)) {
            var prompt_instructions = document.getElementById("prompt_instructions")
            prompt_instructions.innerHTML = "Please enter a valid number for the value of the car you're looking to buy or sell"
            prompt_instructions.style.color = 'red';
            var input_box = document.getElementById("input_number");
            input_box.style.border = '3px solid red';
        } else {
            inputted_value = parseFloat(inputted_value)
            formData.set('my-form', inputted_value)
            nextPage(formData)
        }
    } else {
        nextPage(formData)
    }
    function nextPage(formData) {
        // send the form data to the Flask server using fetch
        fetch('/', {
            method: 'POST',
            body: formData
        })
            .then(response => response.text())
            .then(responseData => {
                // replace the current form page with the new one
                document.getElementById('main').innerHTML = responseData;

                // const script = document.createElement('script');
                // script.src = 'static/validator_functions.js';
                // document.head.appendChild(script);

            })
            .catch(error => console.error(error));
    }
}
function handleLast(event) {
    event.preventDefault(); // prevent the form from submitting normally
    var form = document.getElementById("my-form");
    // console.log(form)
    // Get the Button value
    var button_name = document.getElementById('last-page-btn').name
    // create an object to hold the form data
    var formData = new FormData(form);
    // console.log(formData);
    formData.append('page', button_name)
    formData.append('direction', 'last')


    // log the form data to the console for debugging
    // console.log(formData);

    // send the form data to the Flask server using fetch
    fetch('/', {
        method: 'POST',
        body: formData
    })
        .then(response => response.text())
        .then(responseData => {
            // replace the current form page with the new one
            document.getElementById('main').innerHTML = responseData;
        })
        .catch(error => console.error(error));
};



