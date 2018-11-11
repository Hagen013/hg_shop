<template>
    <div class="controls">
        <div class="controls__button button_1"
            @click="showEditForm"
        >
        </div>
        <edit-form v-if="editFormActive"
            :code="code"
            :pk="pk"
        >
        </edit-form>
    </div>
</template>

<script>
const editForm = () => import('./editForm.vue')

export default {
    name: 'controls',
    components: {
        "edit-form": editForm
    },
    data: () => ({
        editFormActive: true
    }),
    props: ["code", "pk"],
    methods: {
        showEditForm() {
            this.editFormActive = true;
            console.log("showing edit form");
        }
    }
}
</script>

<style lang="scss" scoped>
    .controls {
        position: fixed;
        left: 0px;
        top: 0px;
        height: 100%;
        width: 180px;
        z-index: 10000;
        background: rgba(0,163,97,0.2);
    }
    .controls__button {
        height: 50px;
        width: 50px;
        border-radius: 25px;
        background-color: red;
        cursor: pointer;
    }
    .button_1 {
        position: absolute;
        top: 32px;
        left: 70px;
    }
</style>
