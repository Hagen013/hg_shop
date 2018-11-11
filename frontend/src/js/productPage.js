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

});
