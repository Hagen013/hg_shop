import {Vue} from '../../vue.js'

export default {
    namespaced: true,
    state: function(){
        return {
            cart: null,
            isReady: false
        }
    },
    mutations: {
        ready(state) {
            state.isReady = true;
        },
        getData(state, payload) {
            state.cart = payload;
        }
    },
    actions: {
        initCart({ state, commit, dispatch }, payload) {
            dispatch('syncCart');
        },
        syncCart({commit, state, dispatch}) {
            Vue.http.get('/api/cart/').then(
                response => {
                    commit('ready');
                    commit('getData', response.body);
                },
                response => {

                }
            )
        },
        add({commit, state, dispatch}, payload) {
            let data = new FormData()
            data.append('pk', payload.offer_identifier);
            data.append('quantity', payload.quantity);
            Vue.http.post('/api/cart/', data).then(
                response => {
                    dispatch('syncCart');
                },
                response => {

                }
            )
        },
        update({commit, state, dispatch}, payload) {
            Vue.http.put('/api/cart/', payload).then(
                response => {
                    dispatch('syncCart');
                },
                response => {

                }
            )
        },
        delete({commit, state, dispatch}, payload) {
            Vue.http.delete('/api/cart', {params: payload}).then(
                response => {
                    dispatch('syncCart');
                },
                response => {

                }
            )
        }
    }
};
