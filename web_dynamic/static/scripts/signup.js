$(document).ready(function () {
  const HOST = 'localhost:5000';

  $('.signup-form').on('submit', function (e) {
    e.preventDefault();
    const form = $(this);
    const formData = form.serializeArray().reduce((obj, item) => {
      obj[item.name] = item.value;
      return obj;
    }, {});

    $.ajax({
      type: 'POST',
      url: `http://${HOST}/api/v1/users`,
      data: JSON.stringify(formData),
      contentType: 'application/json',
      success: function (response, status, xhr) {
        console.log(response);
        if (xhr.status === 201) {
          window.location.href = '/login';
        } else {
          $('#error-msg').html('Signup failed');
        }
      },
      error: function (err) {
        console.log('Error: ', err);
      }
    });
  });
});
