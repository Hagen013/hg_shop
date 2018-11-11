<template>
<div class="page-container">
    <md-app md-waterfall md-mode="fixed">
        <md-app-toolbar class="md-primary">
            <span class="md-title">Администрирование TORGOSVET.RU</span>
        </md-app-toolbar>
        
    <md-app-drawer md-permanent="full">
        <md-toolbar class="md-transparent" md-elevation="0">
        Меню
        </md-toolbar>

        <md-list>
            <md-list-item @click="route('/orders')">
                <md-icon>shopping_cart</md-icon>
                <span class="md-list-item-text">Заказы</span>
            </md-list-item>

            <md-list-item @click="route('/products')">
                <md-icon>file_download</md-icon>
                <span class="md-list-item-text">Товары</span>
            </md-list-item>
        </md-list>

    </md-app-drawer>

    <md-app-content>
        <transition name="fade-fast" mode="out-in">
            <router-view></router-view>
        </transition>
    </md-app-content>

    </md-app>
</div>
</template>

<script>
import VueRouter from 'vue-router'

import orderList from './components/ordersList.vue'
import orderForm from './components/orderForm.vue'
import productsList from './components/productsList.vue'

const routes = [
    { path: '/orders', component: orderList },
    { path: '/order/:id', component: orderForm },
    { path: '/products', component: productsList },
]

const router = new VueRouter({
    routes
})

export default {
    name: 'app',
    router,
    methods: {
        route(arg) {
            router.replace({ path: arg })
        },
    }
}
</script>

<style lang="scss">
    .md-app {
        min-height: 100%;
        border: 1px solid rgba(#000, .12);
    }
    .md-app-content {
        position: relative;
    }
    .page-container {
        height: 100%;
    }
    // Demo purposes only
    .md-drawer {
        width: 230px;
        max-width: calc(100vw - 125px);
    }
</style>
