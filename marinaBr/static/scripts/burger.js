const buttonBurger = document.getElementById('burger');
const menu = document.getElementById('nav-menu');

buttonBurger.addEventListener('click', () => {
    buttonBurger.classList.toggle('open');
    menu.classList.toggle('open');
})

document.addEventListener('click', (e) => {
    if (!menu.contains(e.target) && !buttonBurger.contains(e.target)) {
      menu.classList.remove('open');
      buttonBurger.classList.remove('open');
    }
});