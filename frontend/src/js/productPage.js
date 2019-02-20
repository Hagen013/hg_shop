import header from './blocks/header/header'

import overlays from './blocks/overlays/overlays'
import productPageControls from './blocks/productCard/productPageControls'
import productCard from './blocks/productCard/productCard'
import cartModal from './blocks/modals/cartModal'
import modalController from './blocks/modalController'

import store from './store'

store.dispatch('initAll');


$(document).ready(function() {
	$("#media-image-main").elevateZoom({
		gallery:'verticalCarousel', 
		galleryActiveClass: 'active_image',
		imageCrossfade: true,
		loadingIcon: 'http://www.elevateweb.co.uk/spinner.gif',
		borderSize: 5,
		lensBorderSize: 0,
		lensColour: "#00ef81",
		lensFadeIn: 400,
		lensFadeOut: 400,
		easing: true,
		easingAmount: 6,
		zoomWindowFadeIn: 200,
		zoomWindowFadeOut: 200,
		zoomWindowBgColour: "red",
		zoomWindowOffetx: -10,
		zoomWindowPosition: 11,
    });
    
    $("#verticalCarousel").verticalCarousel({
        currentItem: 1,
        showItems: 4,
	});
	

	$('.advantages-tab').on('click', event => {
		const clickedElement = $(event.target);
		let data = $(clickedElement).attr('data');
		if (data === undefined) {
			data = $(clickedElement).parent().attr('data');
		}
		$('.advantages-tab').each(function(index) {
			let tabData = $(this).attr('data');
			if (tabData === data) {
				$(this).addClass("active");
			} else {
				$(this).removeClass("active");
			}
		});
		$('.advantages-item').each(function(index) {
			let itemData = $(this).attr('data');
			if (itemData === data) {
				$(this).addClass("advantages-item_active");
			} else {
				$(this).removeClass("advantages-item_active");
			}
		});
	});

	$('[data-fancybox="images"]').fancybox({
		loop: true,
		keyboard: true,
		thumbs : {
			autoStart : true
		}
	});

	$('#slider-prev').click(function() {
		let activeIndex = 0;
		let quantity = $(".led-stone__item").length;
		$(".led-stone__item").each(function(index) {
			if ($(this).hasClass('active')) {
				activeIndex = index;
			}
			$(this).removeClass("active");
		})
		activeIndex = activeIndex - 1;
		if (activeIndex === -1) {
			activeIndex = quantity - 1;
		}
		$(".led-stone__item").each(function(index) {
			if (index === activeIndex) {
				$(this).addClass('active');
			}
		})
	})

	$('#slider-next').click(function() {
		let activeIndex = 0;
		let quantity = $(".led-stone__item").length;
		$(".led-stone__item").each(function(index) {
			if ($(this).hasClass('active')) {
				activeIndex = index;
			}
			$(this).removeClass("active");
		})
		activeIndex = activeIndex + 1;
		if (activeIndex === quantity) {
			activeIndex = 0;
		}
		$(".led-stone__item").each(function(index) {
			if (index === activeIndex) {
				$(this).addClass('active');
			}
		})
	})
  
});

