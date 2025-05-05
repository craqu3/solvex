let password = window.document.getElementById('password')
let verPassword = window.document.getElementById('verpassword')

if (verPassword != password){
    alert('As passwords não coincidem')
}



const observers = document.querySelectorAll('.fade-in');

const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('show');
        }
    });
}, {
    threshold: 0.1
});

observers.forEach(element => {
    observer.observe(element);
});


function scrollToSection(id) {
    document.getElementById(id).scrollIntoView({ behavior: 'smooth' });
}