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
  const cartCount = $('.item-count');

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
    cartCount.html(Object.keys(cart).length);
  }

  document.querySelectorAll('.rent-btn').forEach((cartButton) => {
    cartButton.addEventListener('click', () => {
      const bikeModel = cartButton.getAttribute('data-model');
      const price = Number(cartButton.getAttribute('data-price'));

      console.log(price);

      if (!cart[bikeModel]) {
        cart[bikeModel] = price;
        totalPrice += price;
      }
      localStorage.setItem('cart', JSON.stringify(cart));
      localStorage.setItem('totalPrice', totalPrice.toFixed(2));
      cartDisplay();
    });
  });

  function removeItem (model) {
    if (model && cart[model]) {
      totalPrice -= parseFloat(cart[model]);

      delete cart[model];

      localStorage.setItem('cart', JSON.stringify(cart));
      localStorage.setItem('totalPrice', totalPrice.toFixed(2));
    }
  }

  cartCount.html(Object.keys(cart).length);
});
