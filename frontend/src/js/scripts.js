import header from './blocks/header/header'

import overlays from './blocks/overlays/overlays'
import productCardAnimate from './scripts/productCardAnimate'

import store from './store'

store.dispatch('initAll');


$(document).ready(function() {
 	
    var slider = $("#site-slider");

   slider.owlCarousel({

   autoplay: 5000,

   loop: true,
   autoplayHoverPause: true,
   // singleItem:true
   // "singleItem:true" is a shortcut for:
   items : 1, 
   // itemsDesktop : false,
   // itemsDesktopSmall : false,
   // itemsTablet: false,
   // itemsMobile : false
   });


   $("#arrow-right").click(function(){
       slider.trigger('next.owl.carousel');
   })
   $("#arrow-left").click(function(){
       slider.trigger('prev.owl.carousel');
   })
});

