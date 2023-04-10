function submitForm() {
  // get the values of the selected radio buttons
  var sex = document.querySelector('input[name="sex"]:checked').value;
  var mode_of_delivery = document.querySelector('input[name="mode_of_delivery"]:checked').value;
  var muscle_tone = document.querySelector('input[name="muscle_tone"]:checked').value;
  var respiratory_effort = document.querySelector('input[name="respiratory_effort"]:checked').value;
  var color = document.querySelector('input[name="color"]:checked').value;
  var reflex_irritability = document.querySelector('input[name="reflex_irritability"]:checked').value;

  // get the values of the text inputs
  var heart_rate1 = document.getElementById("heart_rate1").value;
  var c_birth_weight_g2 = document.getElementById("c_birth_weight_g2").value;
  var mothers_age_cat = document.getElementById("mothers_age_cat").value;
  var c_cat_ga=document.getElementById("c_cat_ga").value;

  // create a JSON object with the input values
  var inputData = {
    "sex": sex,
    "mode_of_delivery": mode_of_delivery,
    "muscle_tone": muscle_tone,
    "respiratory_effort": respiratory_effort,
    "color": color,
    "reflex_irritability": reflex_irritability,
    "heart_rate1": heart_rate1,
    "c_birth_weight_g2": c_birth_weight_g2,
    "mothers_age_cat": mothers_age_cat,
    "c_cat_ga":c_cat_ga
  };
  console.log(inputData);

fetch('/predict', {
  method: 'POST',
  headers: {
      'Content-Type': 'application/json'
  },
  body: JSON.stringify(inputData)
})
.then(response => response.json())
.then(data => {
  console.log('Success:', data['predicted_value']);
  document.getElementById("value").innerHTML = data['predicted_value'];
})
.catch((error) => {
  console.error('Error:', error);
});
}
const form = document.querySelector('form');
form.addEventListener('submit', (event) => {
  event.preventDefault();
  submitForm();
});

