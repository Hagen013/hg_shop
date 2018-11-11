import { Vue } from '../../vue.js'

import store from '../../store'


var cartModal = new Vue({
    name: 'cart-modal',
    el: '#cart-modal',
    store,
    data: {
    },
    computed: {
        isActive() {
            return this.$store.state.cartModal.isActive
        }
    },
    methods: {
        hide() {
            this.$store.commit('cartModal/hide');
        }
    }
});

