// add class navbarDark on navbar scroll
const header = document.querySelector('.navbar');
console.log(header)
window.onscroll = function() {
    const top = window.scrollY;
    if(top >=100) {
        header.classList.add('navbarDark');
    }
    else {
        header.classList.remove('navbarDark');
    }
}
// collapse navbar after click on small devices
const navLinks = document.querySelectorAll('.nav-item')
const menuToggle = document.getElementById('navbarSupportedContent')

navLinks.forEach((l) => {
    l.addEventListener('click', () => { new bootstrap.Collapse(menuToggle).toggle() })
})


document.getElementById('submit-btn').addEventListener('click', function(e) {
    e.preventDefault(); // Sustabdome formos siuntimą
    var nameInput = document.getElementsByName('name')[0];
    var emailInput = document.getElementsByName('email')[0];

    if (nameInput.value.trim() === '' || emailInput.value.trim() === '') {
        alert('Please fill in all required fields.'); // Atvaizduojame pranešimą, jei laukai yra tušti
    } else {
        // Siunčiame formą, jei visi laukai yra užpildyti
        document.querySelector('form').submit();
    }
});
