<template>
    <div class="productPageEditForm form form_fullscreen form_fixed"
        v-if="ready"
    >
        <el-header
            class="form_header bg-purple"
        >
            <h2 class="form__title">Редактирование артикула: {{product.vendor_code}}</h2>
            <div class="form__close bg-purple-dark"
                @click="close"
            >
                <i class="el-icon-close"></i>
            </div>
        </el-header>
        <el-main>
            <el-row :gutter="20">
                <el-col :span="16">
                    <div class="grid-content">

                        <el-row class="form__row">
                            <div class="form__input-label">
                                Название:
                            </div>
                            <el-input placeholder="Название товара"
                                v-model="product.name"
                                class="form__input"
                            >
                            </el-input>
                        </el-row>

                        <el-row class="form__row">
                            <div class="form__input-label">
                                Артикул:
                            </div>
                            <el-input placeholder="Артикул"
                                v-model="product.vendor_code"
                                class="form__input"
                                :disabled=true
                            >
                            </el-input>
                        </el-row>

                        <el-row class="form__row">
                            <div class="form__input-label">
                                Категория:
                            </div>
                            <el-autocomplete
                                class="form__autocomplete"
                                v-model="category"
                                :fetch-suggestions="categorySearchQuery"
                                popper-class="my-autocomplete"
                                placeholder="Выберите категорию"
                                @select="handleCategorySelect"
                            >
                                <template slot-scope="{ item }">
                                    <div class="value">{{ item.name }}</div>
                                </template>
                            </el-autocomplete>
                        </el-row>

                        <el-row class="form__row">
                            <div class="form__input-label">
                                Цена:
                            </div>
                            <el-input-number
                                v-model="product.price"
                                class="form__input"
                            >
                            </el-input-number>
                        </el-row>

                        <el-row class="form__row">
                            <el-checkbox v-model="product.is_in_stock" label="В наличии" border>
                            </el-checkbox>
                            <el-checkbox v-model="product.is_bestseller" label="Хит продаж" border>
                            </el-checkbox>
                            <el-checkbox v-model="product.is_new_product" label="Новинка" border>
                            </el-checkbox>
                        </el-row>

                        <el-row class="form__row">
                            <div class="form__input-label">
                                Скоринг
                            </div>
                            <el-input-number
                                v-model="product.scoring"
                                class="form__input"
                            >
                            </el-input-number>
                        </el-row>

                        <el-row class="form__row">
                            <el-input
                            type="textarea"
                            :rows="8"
                            v-model="product.description">
                            </el-input>
                        </el-row>

                    </div>
                </el-col>
                <el-col :span="8">
                    <div class="grid-content">
                        <el-card>
                            <div class="image-preview">
                                <img :src="product.image">
                            </div>
                        </el-card>
                    </div>
                </el-col>
            </el-row>

            <div class="form__controls">
                <el-button type="primary"
                    :disabled="!hasChanged"
                    @click="saveChanges"
                >
                    <i class="el-icon-check"></i>
                    Сохранить
                </el-button>
                <el-button type="warning"
                    :disabled="!hasChanged"
                    @click="rollBack"
                >
                    <i class="el-icon-close"></i>
                    Откатить
                </el-button>
            </div>

        </el-main>
    </div>
</template>

<script>
    import { Vue } from '../../../vue'
    import Element from 'element-ui'
    import "element-ui/lib/theme-chalk/index.css";
    import store from '../../../store'
    var equal = require('fast-deep-equal');

    Vue.use(Element)

    export default Vue.component('product-page-edit-form', {
        name: 'product-page-edit-form',
        data: () => ({
            productApiUrl: "/api/products/",
            categoriesListApiUrl: "/api/categories/",
            product: null,
            proxyProduct: null,
            apiResponseRecieved: false,
            requestError: false,
            requestErrorCode: null,
            loading: true,
            hasChanged: false,
            categoriesList: [],
            categorisListResponseRecieved: false,
        }),
        store,
        props: {
            id: {
                type: String,
                required: true,
            }
        },
        created() {
            this.setInitialData();
            this.initializeProduct();
            this.getCategories();
        },
        computed: {
            productInitError() {
                return ( (this.apiResponseRecieved===true) && (this.product!==null) )
            },
            showForm() {
                return true
            },
            ready() {
                return ( (this.apiResponseRecieved) && (this.categorisListResponseRecieved) )
            },
            category() {
                if (this.ready) {
                    if (this.product.category_id === null) {
                        return ""
                    }
                    else {
                        for (let i=0; i<this.categoriesList.length; i++) {
                            if (this.product.category_id === this.categoriesList[i].id) {
                                return this.categoriesList[i].name
                            }
                        }
                        return ""
                    }
                }
                return ""
            }
        },
        methods: {
            setInitialData() {
                this.productApiUrl = `${this.productApiUrl}/${this.id}/`;
            },
            initializeProduct() {
                this.$http.get(this.productApiUrl).then(
                    response => {
                        this.handleSuccessfulRequest(response);
                    },
                    response => {
                        this.handleFailedRequest(response);
                    }
                )
            },
            handleSuccessfulRequest(response) {
                this.apiResponseRecieved = true;
                this.product = response.body;
                this.loading = false;
            },
            handleFailedRequest(response) {
                this.apiResponseRecieved = true;
                this.requestError = true;
                this.loading = false;
            },
            checkProductProxyChanges() {
                this.hasChanged = !equal(this.product, this.proxyProduct);
            },
            saveChanges() {
                let data = JSON.parse(JSON.stringify(this.product));
                delete data.image;
                delete data.thumbnail;
                console.log(data);
                this.$http.put(this.productApiUrl, data).then(
                    response => {
                        this.handleSuccessfulUpdateResponse(response); 
                    },
                    response => {
                        this.handleFailedUpdateResponse(response);
                    }
                )
            },
            rollBack() {
                this.product = JSON.parse(JSON.stringify(this.proxyProduct));
            },
            handleSuccessfulUpdateResponse(response) {
                this.proxyProduct = response.body;
                this.product = JSON.parse(JSON.stringify(this.proxyProduct));
            },
            handleFailedUpdateResponse(response) {

            },
            close() {
                this.$store.commit("productPageEditForm/hide");
            },
            getCategories() {
                this.$http.get(this.categoriesListApiUrl).then(
                    response => {
                        this.handleSuccessfulCategoriesListResponse(response);
                    },
                    response => {
                        this.handleFailedCategoriesListResponse(response);
                    }
                )
            },
            handleSuccessfulCategoriesListResponse(response) {
                this.categoriesList = response.body;
                this.categorisListResponseRecieved = true;
            },
            handleFailedCategoriesListResponse(response) {

            },
            handleCategorySelect(category) {
                this.category = category.name;
                this.product.category_id = category.id;
                this.checkProductProxyChanges();
            },
            categorySearchQuery(queryString, cb) {
                let categories = this.categoriesList;
                let results = queryString ? categories.filter(this.createFilter(queryString)) : categories
                cb(results);
            },
            createFilter(queryString) {
                return (link) => {
                    return (link.name.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
                };
            },
        },
        watch: {
            product: {
                handler() {
                    if (this.proxyProduct !== null) {
                        this.checkProductProxyChanges();
                    } else {
                        this.proxyProduct = JSON.parse(JSON.stringify(this.product));
                    }
                },
                deep: true
            },
        }
    })
</script>

<style lang="scss">
    .bg-purple-dark {
        background: #99a9bf;
    }
    .bg-purple {
        background: #d3dce6;
    }
    .form {
    }
    .form_fullscreen {
        height: 100%;
        width: 100%;
        background: white;
    }

    .form__title {
        display: flex;
        align-items: center;
        height: 100%;
        width: 100%;
        color: #1c1c1c;
    }
    .form_fixed {
        position: fixed;
        top: 0px;
        left: 0px;
        z-index: 10000;
    }
    .form__input {
        max-width: 500px;
    }
    .form__autocomplete {
        width: 500px;
    }
    .form__row {
        display: flex;
        margin-bottom: 16px;
    }
    .form__controls {
        margin-top: 30px;
    }
    .form__input-label {
        display: inline-block;
        width: 130px;
        line-height: 40px;
    }
    .image-preview {
        width: 100%;
        height: 300px;
        img {
            height: 100%;
            width: auto;
        }
    }
    .form__close {
        position: absolute;
        display: flex;
        justify-content: center;
        align-items: center;
        top: 0px;
        right: 0px;
        height: 60px;
        width: 60px;
        color: white;
        font-size: 24px;
        cursor: pointer;
    }
    .my-autocomplete {
        z-index: 200000000 !important;
        width: 100%;
        li {
        line-height: normal;
        padding: 7px;
            .value {
                text-overflow: ellipsis;
                overflow: hidden;
            }
            .link {
                font-size: 12px;
                color: #b4b4b4;
            }
        }
    }

</style>