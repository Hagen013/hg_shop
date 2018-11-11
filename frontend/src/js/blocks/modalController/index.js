import { Vue } from '../../vue'

import pageControls from './components/pageControls.vue'
const productPageEditForm = () => import('./components/productPageEditForm.vue')

import store from '../../store'

var modalController = new Vue({
    name: 'modal-controller',
    el: '#modal-controller',
    store,
    components: {
        "pageControls": pageControls,
        "product-page-edit-form": productPageEditForm
    },
    data: {
    },
    computed: {
        showPageControls() {
            return this.$store.state.pageControls.isActive;
        },
        showEditForm() {
            return this.$store.state.productPageEditForm.isActive;
        }
    },
    methods: {
    },
});

