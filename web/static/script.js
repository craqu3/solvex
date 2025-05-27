let password = window.document.getElementById('password')
let verPassword = window.document.getElementById('verpassword')

if (verPassword != password){
    alert('As passwords não coincidem')
}



const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('show');
    }
  });
}, {
  threshold: 0.3 // ajusta conforme necessário
});

document.querySelectorAll('.fade-in').forEach((el) => observer.observe(el));


function scrollToSection(id) {
    document.getElementById(id).scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
}