import { Vue } from '../../vue'

import store from '../../store'

import cartItems from './components/cartItems.vue'


var cart = new Vue({
    name: 'cart',
    el: '#cart',
    store,
    components: {
        'cart-items': cartItems
    },
    data: {
        orderMinPrice: 5000,
        orderUrl: '/orders/',
        cartInitial: {
            items: [],
        }
    },
    computed: {
        cart() {
            if (!this.cartIsReady) {
                return 
            }
            return this.$store.state.cart.cart
        },
        cartIsReady() {
            return this.$store.state.cart.isReady
        },
        orderAllowed() {
            return (this.cartIsReady && (this.cart.total_price > this.orderMinPrice))
        }
    },
    methods: {
        orderRedirect() {
            window.location.href = this.orderUrl;
        }
    }
});

