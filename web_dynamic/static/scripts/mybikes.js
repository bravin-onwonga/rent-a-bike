document.addEventListener('DOMContentLoaded', () => {
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
          userId = response.id
          bikes = get_user_bikes(userId)
        }
      });
    } catch (err) {
      console.log(err)
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
        success: function (response) {
          console.log(response);
          $('.login-link').addClass('show').removeClass('hide');
          $('.logout-btn').addClass('hide').removeClass('show');
          $('.mybike').addClass('hide').removeClass('show');
        }
      });
    } catch (err) {
      console.log(err)
    }
  });

  async function get_user_bikes(userId) {
    try {
      await $.ajax({
        type: 'GET',
        url: `http://${HOST}/api/v1/users/${userId}/bikes`,
        xhrFields: {
          withCredentials: true
        },
        success: function (response) {
          console.log(response);
          for (const bike of response) {
            const bikeCard = `
            <div class="user_rental">
              <img src="${bike.model}.png" class="rental-img" alt="rental-img">
              <div class="card-body">
                <h5 class="card-title">${bike.model}</h5>
                <p class="card-text">${bike.return_date}</p>
                <a href="#" class="btn btn-primary">Return</a>
              </div>
            </div>
            `
            $('.user_rentals').append(bikeCard);
          }
        }
      });
    } catch (err) {
      console.log(err)
    }
  }
})