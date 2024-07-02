$(document).ready(function(){
  const cart = JSON.parse(localStorage.getItem('cart')) || {};
  let totalPrice = parseFloat(localStorage.getItem('totalPrice')) || 0;

  const cartIcon = $('.cart-icon');
  const cartPage = $('.cart-page');
  const closeBtn = $('.close-btn');

  cartIcon.on('click', function () {
    cartPage.addClass('show');
    cartDisplay();
  });

  closeBtn.on('click', function () {
    cartPage.removeClass('show');
    cartDisplay();
  });

  function cartDisplay() {
    const cartList = document.getElementById('cart-list');
    const totalPriceDiv = document.getElementById('total-price');

    cartList.innerHTML = '';
    for (const [model, quantity] of Object.entries(cart)) {
      const cartItem = document.createElement('li');
      $(cartItem).addClass('list-group-item');
      const cartItemImg = $('<img>', { src: `../static/images/${model}.png`, class: 'cart-item'});
      $(cartItem).append(cartItemImg);
      $(cartItem).append(`${model} - ${quantity}`);

      cartList.appendChild(cartItem);
    };

    $(totalPriceDiv).html(`${totalPrice}`);
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
      localStorage.setItem('cart', JSON.stringify(cart));
      localStorage.setItem('totalPrice', totalPrice.toFixed(2));
      cartDisplay();
      console.log(cart);
    })
  });
});