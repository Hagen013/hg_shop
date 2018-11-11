import { Vuex } from '../vue.js'

import pageOverlay from './modules/pageOverlay'
import cart from './modules/cart'
import cartModal from './modules/cartModal'
import modal from './modules/modal'


export default new Vuex.Store({
    modules: {
        pageOverlay: modal,
        cart: cart,
        cartModal: modal,
        pageControls: modal,
        productPageEditForm: modal
    },
    actions: {
        initAll({ commit, state, dispatch, getters }, payload) {
            dispatch('cart/initCart');
        },
        addToCart({ commit, state, dispatch }, payload) {
            dispatch('cart/add', payload);
        },
    }
})