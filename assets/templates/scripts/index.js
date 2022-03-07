var myVar;
var scrollTopButton = document.getElementById("scroll-top")

function pageLoader() {
    myVar = setTimeout(showPage, 1000);
}

function showPage() {
    document.getElementById("loader").style.opacity = 0;
    document.getElementById("loader").style.height = 0;
}

function scrollToTop () {
    window.scrollTo(0, 0);
}



// For scrolling
window.addEventListener('scroll', _ => {
    if (window.scrollY > 100) {
        scrollTopButton.style.bottom = "20px"
    } else {
        scrollTopButton.style.bottom = "-100px"
    }
})