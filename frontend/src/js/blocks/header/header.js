import { Vue } from '../../vue';

import store from '../../store'


var headerTop = new Vue({
    name: 'header',
    el: '#header',
    store,
    data: {
        searchQuery: '',
        headerFixed: false,
    },
    computed: {
        cart() {
            return this.$store.state.cart.cart
        },
        cartIsReady() {
            return this.$store.state.cart.isReady
        },
        cartCaption() {
            if (this.cartIsReady) {
                if (this.cart.count > 0) {
                    return this.cart.total_price + ' р.'
                } else {
                    return 'корзина пуста'
                }
            } else {
                return ''
            }
        },
        cartNotEmpty() {
            return ( this.cartIsReady && (this.cart.count>0) )
        },
        cartCount() {
            if (this.cartNotEmpty) {
                return this.cart.count
            } else {
                return ''
            }
        }
    },
    created() {
        window.onscroll = this.scrollFunction;
    },
    mounted() {
        this.scrollFunction();
    },
    methods: {
        rowEnter(event) {
            let link = event.target.getElementsByTagName('a')[0];
            let submenu = event.target.getElementsByTagName('ul')[0];
            if (submenu !== undefined) {
                submenu.style.height = '485px';
                submenu.style.display = 'block';
                link.classList.add('hover');
            }
        },
        rowExit(event) {
            let link = event.target.getElementsByTagName('a')[0];
            let submenu = event.target.getElementsByTagName('ul')[0];
            if (submenu !== undefined) {
                submenu.style.display = 'none';
                link.classList.remove('hover');
            }
        },
        scrollFunction(e) {
            let headerBottom = document.getElementById('header-bottom');
            let headerOffset = headerBottom.offsetTop;
            let offset = window.pageYOffset;
            let distance = headerOffset - offset;
            if ((distance <= 0) && (!this.headerFixed) ) {
                this.headerFixed = true;
                headerBottom.style.top = '0px';
                headerBottom.style.position = 'fixed';
            } else if ((this.headerFixed) && (distance >= -78) ) {
                this.headerFixed = false;
                headerBottom.style.top = 'auto';
                headerBottom.style.position = 'absolute';
            }
        },
        showOverlay() {
            this.$store.commit('pageOverlay/show');
        },
        hideOverlay() {
            this.$store.commit('pageOverlay/hide');
        }
    }
});

