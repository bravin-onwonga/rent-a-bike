$(document).ready(function () {
  const HOST = 'localhost:5000';

  async function getCurrentUser() {
    try {
      await $.ajax({
        type: 'GET',
        url: `http://${HOST}/api/v1/auth/current_user`,
        xhrFields: {
          withCredentials: true
        },
        success: function (response) {
          console.log(response);
        }
      });
    } catch (err) {
      console.log(err)
    }
  }
  getCurrentUser();
});
