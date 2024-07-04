$(document).ready(function(){
  const cart = JSON.parse(localStorage.getItem('cart')) || {};
  let totalPrice = parseFloat(localStorage.getItem('totalPrice')) || 0;

  const cartIcon = $('.cart-icon');
  const cartPage = $('.cart-page');
  const closeImg = $('.close-img');

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

  function cartDisplay() {
    const cartList = document.getElementById('cart-list');

    cartList.innerHTML = '';
    for (const [model, quantity] of Object.entries(cart)) {
      const cartItem = document.createElement('li');
      $(cartItem).addClass('list-group-item');
      const cartItemImg = $('<img>', { src: `../static/images/${model}.png`, class: 'bike-cart-img'});
      $(cartItem).append(cartItemImg);
      $(cartItem).append(`${model} - ${quantity}`);
      const closeImg = $('<img>', { src: '../static/images/remove.png', class: 'remove-img', 'data-model': model})
      $(cartItem).append(closeImg)

      cartList.appendChild(cartItem);
    };

    $('#total').html(`${totalPrice}`);
  }

  document.querySelectorAll('.rent-btn').forEach((cartButton) => {
    cartButton.addEventListener('click', () => {
      const bikeModel = cartButton.getAttribute('data-model');
      const price = Number(cartButton.getAttribute('data-price'));
      const availabile = Number(cartButton.getAttribute('data-availabile'));

      console.log(price);

      if (cart[bikeModel]) {
        if (cart[bikeModel] < availabile) {
          cart[bikeModel] += 1;
        }
      } else {
        cart[bikeModel] = 1;
      }
      totalPrice += price;
      console.log(totalPrice);

      localStorage.setItem('cart', JSON.stringify(cart));
      localStorage.setItem('totalPrice', totalPrice.toFixed(2));
      cartDisplay();
      console.log(cart);
    })
  });

  function removeItem(model) {
    if (model && cart[model]) {
      const itemPrice = document.querySelector(`[data-model="${model}"]`).getAttribute('data-price')
      totalPrice -= parseFloat(cart[model] * itemPrice)

      delete cart[model];

      localStorage.setItem('cart', JSON.stringify(cart));
      localStorage.setItem('totalPrice', totalPrice.toFixed(2));
    }
  }
});