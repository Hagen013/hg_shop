import { Vue } from '../../vue.js'

import store from '../../store'


var overlays = new Vue({
    name: 'overlays',
    el: '#overlays',
    store,
    data: {
    },
    computed: {
        pageOverlayIsActive() {
            return this.$store.state.pageOverlay.isActive
        }
    }
});

