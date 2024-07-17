document.addEventListener('DOMContentLoaded', () => {
  const HOST = 'localhost:5000';

  async function getCurrentUser () {
    try {
      await $.ajax({
        type: 'GET',
        url: `http://${HOST}/api/v1/auth/current_user`,
        xhrFields: {
          withCredentials: true
        },
        success: function (response) {
          console.log(response);
          $('.login-link').addClass('hide').removeClass('show');
          $('.logout-btn').addClass('show').removeClass('hide');
          $('.mybike').addClass('show').removeClass('hide');
        }
      });
    } catch (err) {
      console.log(err);
    }
  }
  getCurrentUser();

  $('.logout-btn').on('click', function () {
    try {
      $.ajax({
        type: 'GET',
        url: `http://${HOST}/api/v1/auth/logout`,
        xhrFields: {
          withCredentials: true
        },
        success: function (response, status, xhr) {
          if (xhr.status === 200) {
            $('.login-link').addClass('show').removeClass('hide');
            $('.logout-btn').addClass('hide').removeClass('show');
            $('.mybike').addClass('hide').removeClass('show');
            window.location.href = '/home';
          } else {
            console.log('Logout failed');
          }
        }
      });
    } catch (err) {
      console.log(err);
    }
  });
});
