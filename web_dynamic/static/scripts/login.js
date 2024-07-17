$(document).ready(function () {
  const HOST = 'localhost:5000';

  $('.login-form').on('submit', function (e) {
    e.preventDefault();
    const form = $(this);
    const formData = form.serializeArray().reduce((obj, item) => {
      obj[item.name] = item.value;
      return obj;
    }, {});

    $.ajax({
      type: 'POST',
      url: `http://${HOST}/api/v1/auth/login`,
      data: JSON.stringify(formData),
      contentType: 'application/json',
      xhrFields: {
        withCredentials: true
      },
      success: function (response) {
        console.log('Login success');
        console.log(response);
        window.location.href = '/home';
      },
      error: function (err) {
        console.log('Login failed');
        console.log('Error: ', err);
        $('#error-msg').html('Wrong Email or Password');
      }
    });
  });
});
