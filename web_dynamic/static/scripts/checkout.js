$(document).ready(function(){
  const cart = JSON.parse(localStorage.getItem('cart')) || {};
  let totalPrice = parseFloat(localStorage.getItem('totalPrice')) || 0;

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

  cartDisplay();
});