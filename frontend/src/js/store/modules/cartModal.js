export default {
    namespaced: true,
    state: function(){
        return {
            isActive: false
        }
    },
    mutations: {
        show(state) {
            state.isActive = true;
        },
        hide(state) {
            state.isActive = false;
        }
    }
};
