import { Vue } from '../../vue'

import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css'

Vue.use(VueMaterial)

import loginForm from './loginForm.vue'


var adminLogin = new Vue({
    name: 'admin-login',
    el: "#app",
    components: {
        'login-form': loginForm
    },
    data: {},
    methods: {
    }
});
