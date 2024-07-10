$(document).ready(function () {
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

  $('.checkout-form').on('submit', function (e) {
    e.preventDefault();
    const form = $(this);
    const formData = form.serializeArray().reduce((obj, item) => {
      obj[item.name] = item.value;
      return obj;
    }, {});

    const returnDate = formData.return_date;
    delete formData.return_date;

    $.ajax({
      type: 'POST',
      url: 'http://localhost:5000/api/v1/users',
      data: JSON.stringify(formData),
      contentType: 'application/json',
      success: function (response) {
        const userId = response.id;
        const data = {
          'amount': totalPrice,
          'phone_number': formData.phone_number
        }

        $.ajax({
          type: 'POST',
          url: 'http://localhost:5000/api/v1/pay',
          data: JSON.stringify(data),
          contentType: 'application/json',
          success: function (response) {
            console.log(response);
            $.ajax({
              type: 'GET',
              url: 'http://localhost:5000/api/v1/callback',
              data: JSON.stringify(data),
              contentType: 'application/json',
              success: function (response) {
                console.log(response);
              },
              error: function (err) {
                console.log('Error: ', err);
              }
            })
            updateBikeDetails(userId, returnDate);
          },
          error: function (err) {
            console.log('Error: ', err);
          }

        });
        cartPage.removeClass('show');
      },
      error: function (err) {
        console.log('Error: ', err);
      }
    });

    function updateBikeDetails (userId, returnDate) {
      for (const model in cart) {
        $.ajax({
          type: 'GET',
          url: 'http://localhost:5000/api/v1/bikes',
          success: function (response) {
            for (const bike of response) {
              if (bike.model === model) {
                const data = {
                  user_id: userId,
                  available: false,
                  rent_date: new Date().toISOString(),
                  return_date: returnDate
                };
                $.ajax({
                  type: 'PUT',
                  url: `http://localhost:5000/api/v1/bikes/${bike.id}`,
                  data: JSON.stringify(data),
                  contentType: 'application/json',
                  success: function (response) {
                    console.log(response);
                  },
                  error: function (err) {
                    console.log('Error: ', err);
                  }
                });
                break;
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
});
