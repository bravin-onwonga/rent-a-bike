$(document).ready(function () {
  const currentPage = window.location.pathname.split('/').pop();
  $('.nav-items .navlinks li').each(function (index, element) {
    if ($(element).find('a').attr('href').split('/').pop() === currentPage) {
      $(element).addClass('active');
    }
  });
});
