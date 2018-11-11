<template>
    <div class="edit-form">
        <div class="header">
            Редактирование товара: {{code}}
        </div>
        <div class="content" v-if="showContent">
            <div class="content__left">
                <div class="field">
                    <input class="input" v-model="product.name">
                </div>
                <div class="field">
                    <input class="input" v-model="product.price">
                </div>
                <div class="field">
                    <input class="input" v-model="product.old_price">
                </div>
                <div class="field">
                    <textarea class="textarea" v-model="product.description">
                    </textarea>
                </div>
                <div class="field">
                    <input type="checkbox" v-model="product.is_in_stock">
                </div>
                <div class="field">
                    <input type="checkbox" v-model="product.is_bestseller">
                </div>
                <div class="field">
                    <input type="checkbox" v-model="product.is_new_product">
                </div>
                <div class="field">
                    <input type="checkbox" v-model="product.is_published">
                </div>
                <div class="field">
                    <input class="input" v-model="product.scoring">
                </div>
                <div class="attributes">
                    <div class="attribute" v-for="item in product.attributes"
                    >
                    </div>
                </div>
                <div class="meta-tags">
                    <div class="field">
                        <input class="input" v-model="product._meta_title">
                    </div>
                    <div class="field">
                        <textarea class="textarea" v-model="product._meta_description">
                        </textarea>
                    </div>
                    <div class="field">
                        <textarea class="textarea" v-model="product._meta_keywords">
                        </textarea>
                    </div>
                </div>
            </div>
            <div class="content__right">
            </div>
        </div>
        <div class="content content_error" v-if="showErrorContent">
            <div>
            </div>
        </div>
    </div>
</template>


<script>
export default {
    name: 'editForm',
    props: ["code", "pk"],
    data: () => ({
        originalProduct: null,
        product: null,
        apiUrl: '/api/products/',
        apiResponseRecieved: false,
        apiResponseFailed: false
    }),
    created() {
        this.apiUrl = `${this.apiUrl}${this.pk}/`;
        this.$http.get(this.apiUrl).then(
            response => {
                this.handleSuccessfulResponse(response);
            },
            response => {
                this.handleFailedResponse(response);
            }
        )
    },
    computed: {
        showContent() {
            return (this.apiResponseRecieved && !this.apiResponseFailed)
        },
        showErrorContent() {
            return (this.apiResponseRecieved && this.apiResponseFailed)
        }
    },
    methods: {
        handleSuccessfulResponse(response) {
            this.product = response.body;
            this.originalProduct = Object.assign({}, this.product);
            this.apiResponseRecieved  = true;
        },
        handleFailedResponse(response) {
            this.apiResponseFailed = true;
        }
    },
    watch: {
        product: {
            deep: true,
            handler() {

            }
        }
    }
}
</script>

<style lang="scss" scoped>
    .edit-form {
        position: fixed;
        height: 100%;
        width: 100%;
        background-color: white;
    }
    .header {
        height: 55px;
        line-height: 55px;
        padding: 0px 16px 0px 16px;
        color: white;
        background-color: rgb(32,32,32);
    }
</style>
