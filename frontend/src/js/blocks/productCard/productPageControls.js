import { Vue } from '../../vue.js';

import store from '../../store'

import controls from './components/controls.vue'
const editForm = () => import('./components/editForm.vue')


var productPageControls = new Vue({
    name: 'product-page-controls',
    el: '#product-page-controls',
    store,
    components: {
        'controls': controls
    },
    data: {
        isStaff: false,
        sessionUserApiView: '/api/users/session/'
    },
    created() {
        if (IS_STAFF === 'True') {
            this.isStaff = true;
        }
    },
    methods: {
    }
});

