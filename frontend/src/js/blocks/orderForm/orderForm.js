import { Vue } from '../../vue'
import MaskedInput from 'vue-text-mask';
import validateEmail from '../../core/validateEmail.js'

import store from '../../store'


var orderForm = new Vue({
    name: 'orderForm',
    el: '#order-form',
    store,
    components: {
        'masked-input': MaskedInput
    },
    data: {
        orderApiUrl: '/api/orders/',
        orderSuccessUrl: '/orders/success/',
        orderErrorUrl: '/orders/cancelled/',
        nameProceeded: false,
        phoneProceeded: false,
        emailProceeded: false,
        minPrice: 5000,
        order: {
            'status': 1,
            'order_text': '',
            'noftified': false,
            'name': '',
            'phone': '',
            'email': '',
            'address': '',
        },
    },
    computed: {
        cartIsReady() {
            return this.$store.state.cart.isReady
        },
        cartProxy() {
            return this.$store.state.cart.cart 
        },
        nameIsValid() {
            return this.order.name.length > 0 ? true : false;
        },
        phoneIsValid() {
            let index = this.order.phone.indexOf('_');
            if ( this.order.phone.length >= 17 && (index === -1) ) {
                return true
            } else {
                return false
            }
        },
        emailIsValid() {
            return validateEmail(this.order.email);
        },
        isValid() {
            return (this.nameIsValid && this.phoneIsValid && this.emailIsValid);
        },
        orderAllowed() {
            return (this.isValid && this.cartIsReady && this.cartProxy.total_price > this.minPrice)
        }
    },
    methods: {
        orderSubmit() {
            console.log('submiting');
            let formData = new FormData();

            for ( let key in this.order ) {
                formData.append(key, this.order[key]);
            }
    
            this.$http.post(this.orderApiUrl, this.order).then (
                response => {
                    this.handleSuccessfulResponse(response);
                },
                response => {
                    this.handleFailedResponse(response);
                }
            )
        },
        handleSuccessfulResponse() {
            console.log('success');
            window.location.href = this.orderSuccessUrl;
        },
        handleFailedResponse() {
            console.log('failed');
            window.location.href = this.orderErrorUrl;
        },
        processName() {
            this.nameProceeded = true;
        },
        processPhone() {
            this.phoneProceeded = true;
        },
        processEmail() {
            this.emailProceeded = true;
        }
    },
});

