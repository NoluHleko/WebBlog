const slideimages = document.querySelector ('.slide-images');
const imagesInSlide = document.querySelectorAll('.slide-images img');

//Buttons

const prevBtn = document.querySelector ('#prev-button');
const nextBtn = document.querySelector ('#next-button');

//counter

let counter = 1;
const size = imagesInSlide[0].clientWidth;

slideimages.style.transform = 'translateX('+ (-size * counter) + 'px)';

nextBtn.addEventListener ('click',() => {
    slideimages.style.transition = "transform 0.4s ease-in-out";
    counter++;
    slideimages.style.transform = 'translateX ('+ (-size * counter) + 'px)';
});

prevBtn.addEventListener ('click', () =>{
    slideimages.style.transition = "transform 0.4s ease-in-out";
    counter--;
    slideimages.style.transform = 'translateX ('+ (-size * counter) + 'px)';
});

imagesInSlide.addEventListener ('transitionend', () => {console.log ('Fired');})