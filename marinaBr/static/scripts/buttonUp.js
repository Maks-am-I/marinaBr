const btnUp = document.getElementById('button-up');

window.addEventListener('scroll', () => {
    btnUp.classList.toggle('visible', window.scrollY > 300);
})