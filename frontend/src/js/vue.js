// Импорт дополнительных библиотек
import Vue from 'vue';
import VueResource from 'vue-resource';
import Vuex from 'vuex';


// Вшивание CSRF-токена в запросы vue-resource
// и конфигурирование vue.js
import csrfToken from './core/csrfToken';

Vue.use(VueResource);
Vue.use(Vuex);

Vue.http.headers.common['X-CSRFToken'] = csrfToken();

export {
    Vue,
    VueResource,
    Vuex,
}