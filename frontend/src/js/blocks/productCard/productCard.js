import { Vue } from '../../vue.js';

import store from '../../store'


var productCard = new Vue({
    name: 'product-card',
    el: '#product-card',
    store,
    data: {
        productQuantity: 1,
        productQuantityMax: 999,
        productQuantityMultiplier: 1
    },
    created() {
        if (IS_STAFF === 'True') {
            this.$store.commit("pageControls/show");
        }
    },
    methods: {
        incrementProductQuantity() {
            let possibleValue = this.productQuantity + this.productQuantityMultiplier;
            if ( possibleValue <= this.productQuantityMax) {
                this.productQuantity += this.productQuantityMultiplier;
            }
        },
        decrementProductQuantity() {
            let possibleValue = this.productQuantity + this.productQuantityMultiplier;
            if ( possibleValue > this.productQuantityMultiplier+1 ) {
                this.productQuantity -= this.productQuantityMultiplier;
            }
        },
        handeValueInput() {

        },
        handleValueChange() {
            if (this.productQuantity > this.productQuantityMax) {
                this.productQuantity = this.productQuantityMax;
            } else if (this.productQuantity < this.productQuantityMultiplier) {
                this.productQuantity = this.productQuantityMultiplier;
            }
        },
        addToCart(itemID) {
            this.$store.dispatch('addToCart', {
                offer_identifier: itemID,
                quantity: this.productQuantity
            });
            this.$store.commit('cartModal/show');
        }
    }
});

