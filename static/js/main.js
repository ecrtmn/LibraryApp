const slider = document.querySelector(".slider");
const slides = slider.querySelectorAll(".slide");

let currentSlide = 0;
let interval;
startTimer();

function changeSlide() {
    slider.querySelector(".slide.active").classList.remove("active");
    currentSlide++;
    currentSlide = currentSlide % slides.length;
    slides[currentSlide].classList.add("active");
}

function startTimer() {
    interval = setInterval(changeSlide, 5000);
}

function stopTimer() {
    clearInterval(interval);
}

slider.addEventListener("mouseenter", stopTimer);
slider.addEventListener("mouseleave", startTimer);

//-------------------------

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

const booksList = document.querySelector(".books__listing");
const booksTotalCount = +booksList.getAttribute("data-books-length");
const booksPerPage = +booksList.getAttribute("data-per-page");
const showMoreBtn = document.getElementById("show-more");
showMoreBtn.addEventListener("click", function(e) {
    e.preventDefault();
    const booksCount = booksList.children.length;
    const xhr = new XMLHttpRequest();
    xhr.open("get", `${window.location.href}?booksCount=${booksCount}`);
//    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.onload = function() {
        booksList.innerHTML += this.responseText;
        if (booksCount + booksPerPage >= booksTotalCount) {
            showMoreBtn.remove();
        }
    };
    xhr.send();
});
