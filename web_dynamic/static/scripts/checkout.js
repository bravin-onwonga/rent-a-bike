$(document).ready(function () {
  const HOST = 'localhost:5000';
  let user_id = null;

  // Cart logic starts here

  const cart = JSON.parse(localStorage.getItem('cart')) || {};
  let totalPrice = parseFloat(localStorage.getItem('totalPrice')) || 0;

  if (cart.length === 0) {
    totalPrice = 0;
    localStorage.setItem('totalPrice', totalPrice);
    cartDisplay();
  }

  const cartIcon = $('.cart-icon');
  const cartPage = $('.cart-page');
  const closeImg = $('.close-img');
  const orderBtn = $('.order-btn');

  orderBtn.on('click', function () {
    localStorage.clear();
    cartDisplay();
  });

  cartIcon.on('click', function () {
    cartPage.addClass('show');
    cartDisplay();
  });

  closeImg.on('click', function () {
    cartPage.removeClass('show');
    cartDisplay();
  });

  $(document).on('click', '.remove-img', function () {
    const model = $(this).data('model');
    removeItem(model);
    cartDisplay();
  });

  function cartDisplay () {
    const cartList = document.getElementById('cart-list');

    cartList.innerHTML = '';
    for (const [model, price] of Object.entries(cart)) {
      const cartItem = document.createElement('li');
      $(cartItem).addClass('list-group-item');
      const cartItemImg = $('<img>', { src: `../static/images/${model}.png`, class: 'bike-cart-img' });
      $(cartItem).append(cartItemImg);
      $(cartItem).append(`${model} - ${price}`);
      const closeImg = $('<img>', { src: '../static/images/remove.png', class: 'remove-img', 'data-model': model });
      $(cartItem).append(closeImg);

      cartList.appendChild(cartItem);
    }

    $('#total').html(`${totalPrice}`);
  }
  cartDisplay();

  function removeItem (model) {
    if (model && cart[model]) {
      totalPrice -= parseFloat(cart[model]);

      delete cart[model];

      localStorage.setItem('cart', JSON.stringify(cart));
      localStorage.setItem('totalPrice', totalPrice.toFixed(2));
      cartDisplay();
    }
  }
  cartDisplay();

  // Payment logic starts here

  $('.checkout-form').on('submit', async function (e) {
    e.preventDefault();
    const form = $(this);
    const formData = form.serializeArray().reduce((obj, item) => {
      obj[item.name] = item.value;
      return obj;
    }, {});

    const returnDate = formData.return_date;
    delete formData.return_date;

    phonenumber = formData.phone_number;

    if (phonenumber.length < 9) {
      $('#error-msg').html('Invalid phone number');
      return;
    }

    phonenumber = '2547' + phonenumber.slice(-8);

    const data = {
      amount: totalPrice,
      phone_number: phonenumber
    };

    if (!$.isEmptyObject(cart)) {
      try {
        const payResponse = await $.ajax({
          type: 'POST',
          url: `http://${HOST}/api/v1/pay`,
          data: JSON.stringify(data),
          contentType: 'application/json'
        });

        console.log(payResponse.ResponseCode);
        if (Number(payResponse.ResponseCode) === 0) {
          console.log('Payment initiated');
          paymentStatus = await checkPayment();
        }

        if (paymentStatus == 'TIMEOUT' || paymentStatus == 'SUCCESS') {
          console.log('Payment made');

          await checkLogin();

          console.log(user_id);

          if (user_id === null) {
            console.log('User not logged in');
            $.ajax({
              type: 'POST',
              url: `http://${HOST}/api/v1/users`,
              data: JSON.stringify(formData),
              contentType: 'application/json',
              success: function (response) {
                console.log(response.id);
                cartPage.removeClass('show');
                updateBikeDetails(response.id, returnDate);
              },
              error: function (err) {
                console.log('Error: ', err);
              }
            });
          } else if (user_id !== null) {
            console.log('User logged in');
            const myLst = ['firstname', 'lastname', 'email', 'phone_number', 'id_number', 'password'];

            for (const key in formData) {
              if (myLst.includes(key)) {
                delete formData[key];
              }
            }

            if (formData.county === '') {
              formData.county = 'Nairobi';
            }

            $.ajax({
              type: 'PUT',
              url: `http://${HOST}/api/v1/users/${user_id}`,
              data: JSON.stringify(formData),
              contentType: 'application/json',
              success: function (response) {
                const userId = response.id;
                cartPage.removeClass('show');
                updateBikeDetails(userId, returnDate);
              },
              error: function (err) {
                console.log('Error: ', err);
              }
            });
          }
        } else if (paymentStatus == 'CANCELLED') {
          $('#error-msg').html('Payment cancelled');
        } else {
          $('#error-msg').html('Payment Request Timeout');
        }
      } catch (err) {
        console.log('Error: ', err);
        $('#error-msg').html('An error occurred');
      }
    } else {
      $.ajax({
        type: 'POST',
        url: `http://${HOST}/api/v1/users`,
        data: JSON.stringify(formData),
        contentType: 'application/json',
        success: function (response) {
          console.log(response.id);
          cartPage.removeClass('show');
        },
        error: function (err) {
          console.log('Error: ', err);
        }
      });
    }

    // Check payment details here

    async function checkPayment () {
      const interval = 3000;
      const maxAttempts = 8;
      let attempts = 0;

      while (true) {
        console.log('Still waiting..........');
        try {
          const callback_data = await $.ajax({
            type: 'GET',
            url: `http://${HOST}/api/v1/check_payment`,
            contentType: 'application/json'
          });
          if (!$.isEmptyObject(callback_data)) {
            result_code = callback_data.Body.stkCallback.ResultCode;
            if (Number(result_code) === 0) {
              console.log('Payment successful');
              return ('SUCCESS');
            } else if (Number(result_code) === 1032) {
              console.log('Payment cancelled');
              return ('CANCELLED');
            } else {
              console.log('Payment request timeout');
              return ('TIMEOUT');
            }
          }
          attempts += 1;

          if (attempts > maxAttempts) {
            return ('TIMEOUT');
          }
          await new Promise(resolve => setTimeout(resolve, interval));
        } catch (err) {
          console.log('Error: ', err);
          $('#error-msg').html('Something went wrong. Please try again');
          break;
        }
      }
    }

    // Update bike details here after payment

    async function updateBikeDetails (userId, returnDate) {
      for (const model in cart) {
        await $.ajax({
          type: 'GET',
          url: `http://${HOST}/api/v1/bikes`,
          success: function (response) {
            for (const bike of response) {
              if (bike.model === model) {
                const data = {
                  user_id: userId,
                  available: false,
                  return_date: returnDate
                };
                $.ajax({
                  type: 'PUT',
                  url: `http://${HOST}/api/v1/bikes/${bike.id}`,
                  data: JSON.stringify(data),
                  contentType: 'application/json',
                  xhrFields: {
                    withCredentials: true
                  },
                  success: function (response) {
                    console.log(response);
                  },
                  error: function (err) {
                    console.log('Error: ', err);
                  }
                });
              }
            }
          },
          error: function (err) {
            console.log('Error: ', err);
          }
        });
      }
    }
  });

  // Checks whether the user is logged in or not

  async function checkLogin () {
    try {
      await $.ajax({
        type: 'GET',
        url: `http://${HOST}/api/v1/auth/current_user`,
        xhrFields: {
          withCredentials: true
        },
        success: function (response, status, xhr) {
          if (Number(xhr.status) === 200) {
            console.log(response);
            $('.name-section input').removeAttr('required').parent().hide();
            $('.email-section input').removeAttr('required').parent().hide();
            $('.id-section input').removeAttr('required').parent().hide();

            $('.name-section').hide();
            $('.email-section').hide();
            $('.id-section').hide();
            user_id = response.id;
            return (user_id);
          }
          logged_in = false;
        }
      });
    } catch (err) {
      console.log(err);
      return (false);
    }
  }
  checkLogin();
});
