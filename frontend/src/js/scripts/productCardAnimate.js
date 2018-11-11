(function () {
    function addAnimateClass () {
        this.classList.add('animate');
    }
    function removeAnimateClass () {
        this.classList.remove('animate');
    }
    document.addEventListener("DOMContentLoaded", function(event) {
        let productCards = document.getElementsByClassName('product-card');
    
        for (let i=0; i<productCards.length; i++) {
            let productCard = productCards[i];
            productCard.addEventListener('mouseenter', addAnimateClass);
            productCard.addEventListener('mouseleave', removeAnimateClass);
        }
    });
})();