<template>
    <div class="page-controls">
        <div class="page-controlls__button"
            @click="showEditForm"
        >
            <i class="icon icon_create"></i>
        </div>
    </div>
</template>

<script>
    import store from '../../../store'

    export default {
        name: 'page-controls',
        store,
        methods: {
            showEditForm() {
                this.$store.commit('productPageEditForm/show');
            }
		}
    }
</script>

<style lang="scss" scoped>
    .page-controls {
        position: fixed;
        padding: 200px 0px 0px 24px;
        height: 100%;
        width: 100px;
        height: 100%;
        top: 0px;
        left: 0px;
        background: rgba(0,0,0,0.1);
        z-index: 9000;
    }
    .page-controlls__button {
        display: flex;
        justify-content: center;
        align-items: center;
        transition: width 500ms;
        width: 48px;
        height: 48px;
        background-color: #f45057;
        margin-right: 16px;
        position: relative;
        border-radius: 24px;
        box-shadow: 0 2px 8px 0 rgba(0,0,0,.24);
        background-repeat: no-repeat;
        color: white;
        cursor: pointer;
        .icon {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
            width: 100%;
            font-size: 20px;
        }
    }
</style>