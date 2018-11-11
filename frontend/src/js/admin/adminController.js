import {Vue} from './../vue.js'
import VueMaterial from 'vue-material'
import VueRouter from 'vue-router'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css'


Vue.use(VueMaterial)
Vue.use(VueRouter)

import app from './app.vue'

import store from './../store';


const routes = [
]
  
const router = new VueRouter({
    routes
})

var appController = new Vue({
    name: 'appController',
    el: '#app',
    store,
    router,
    data: {
        menuVisible: false,
        routerState: 1,
    },
    components: {
        'app': app
    },
    methods: {
        toggleMenu () {
            this.menuVisible = !this.menuVisible
        },
        route(arg) {
            router.push({ path: arg })
        },
        hideNavigation() {
            if ( this.menuVisible ) {
                this.menuVisible = false;
            }
        }
    }
})

// router.replace({ path: '/upload', redirect: '*' })