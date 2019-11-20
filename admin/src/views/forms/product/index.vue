<template>
    <div class="app-container" v-loading="loadingOverall">
        <div class="app-view" v-if="initializedOverall">
            <div class="app-view-controls">
                <el-button type="primary" :disabled="!saveIsAvailable" @click="saveChanges">
                    Сохранить
                </el-button>
                <el-button type="danger" :disabled="!deleteIsAvailable" @click="triggerDelete">
                    Удалить
                </el-button>
            </div>
            <el-tabs v-model="activeName">
                <el-tab-pane label="Основное" name="main">
                    <el-row :gutter="20">
                        <el-col :span="12">
                            <div class="field">
                                <div class="field-label">
                                    Название:
                                </div>
                                <div class="field-value">
                                    <el-input v-model="instance.name" @input="handleNameInput">
                                    </el-input>
                                </div>
                            </div>
                            <div class="field">
                                <div class="field-label">
                                    Категория
                                </div>
                                <div class="field-value">
                                    <el-select v-model="instance.category_id" filterable placeholder="Выбрать">
                                        <el-option
                                            v-for="item in categoriesOptions"
                                            :key="item.id"
                                            :label="item.name"
                                            :value="item.id"
                                        >
                                        </el-option>
                                    </el-select>
                                </div>
                            </div>
                            <div class="field">
                                <div class="field-label">
                                    Артикул:
                                </div>
                                <div class="field-value">
                                    <el-input v-model="instance.vendor_code">
                                    </el-input>
                                </div>
                            </div>
                            <div class="field">
                                <div class="field-label">
                                    URL:
                                </div>
                                <div class="field-value">
                                    <el-input v-model="instance.url">
                                    </el-input>
                                </div>
                            </div>
                            <div class="field">
                                <div class="field-label">
                                    Цена:
                                </div>
                                <div class="field-value">
                                    <el-input-number v-model="instance.price" controls-position="right">
                                    </el-input-number>
                                </div>
                            </div>
                            <div class="field">
                                <div class="field-label">
                                    Старая цена:
                                </div>
                                <div class="field-value">
                                    <el-input-number v-model="instance.old_price" controls-position="right">
                                    </el-input-number>
                                </div>
                            </div>
                            <div class="field field_block">
                                <div class="field-label">
                                    Описание:
                                </div>
                                <div class="field-value">
                                    <el-input type="textarea" rows="3">
                                    </el-input>
                                </div>
                            </div>
                            <div class="field">
                                <div class="field-label">
                                    Meta-title:
                                </div>
                                <div class="field-value">
                                    <el-input v-model="instance._meta_title">
                                    </el-input>
                                </div>
                            </div>
                            <div class="field field_block">
                                <div class="field-label">
                                    Meta-keywords:
                                </div>
                                <div class="field-value">
                                    <el-input type="textarea" v-model="instance._meta_keywords" :rows="4">
                                    </el-input>
                                </div>
                            </div>
                            <div class="field field_block">
                                <div class="field-label">
                                    Meta-description:
                                </div>
                                <div class="field-value">
                                    <el-input type="textarea" v-model="instance._meta_description" :rows="3">
                                    </el-input>
                                </div>
                            </div>
                        </el-col>
                        <el-col :span="12">
                            <div class="images-wrapper">
                                <img :src="instance.thumbnail">
                            </div>
                        </el-col>
                    </el-row>
                </el-tab-pane>
                <el-tab-pane label="Атрибуты" name="attributes">
                    <el-row>
                        <el-col :span="12">
                            <div class="field" v-for="(value, propertyName) in instance.attributes" :key="propertyName">
                                <div class="field-label">
                                    {{propertyName}}
                                </div>
                                <div class="field-value">
                                    <el-input v-model="instance.attributes[propertyName]">
                                    </el-input>
                                </div>
                            </div>
                        </el-col>
                    </el-row>
                </el-tab-pane>
                <el-tab-pane label="Изображения" name="images">
                    <images
                        :instance="instance"
                        :activeTab="activeName"
                        @change="handleImagesChange"
                        ref="images"
                    >
                    </images>
                </el-tab-pane>
            </el-tabs>
        </div>
    </div>
</template>

<script>
import request from '@/utils/request'
const equal = require('fast-deep-equal');
import cyrillToLatin from '@/utils/cyrillToLatin';

import Images from './components/Images'


export default {
    name: 'Product',
    data: () => ({
        pk: null,
        instance: null,
        instanceProxy: null,
        loading: true,
        activeName: 'main',
        hasChanged: false,
        imagesChanged: false,
        initialized: false,
        categoriesOptions: [],
        categoriesReceived: false
    }),
    components: {
        'images': Images
    },
    computed: {
        saveIsAvailable() {
            return (this.hasChanged || this.imagesChanged)
        },
        deleteIsAvailable() {
            if (this.pk === null) {
                return false
            }
            return true;
        },
        loadingOverall() {
            return (this.loading && !this.categoriesReceived)
        },
        initializedOverall() {
            return (this.initialized && this.categoriesReceived)
        },
        creationMode() {
            return (this.pk === null)
        }
    },
    created() {
        this.initialize();
    },
    methods: {
        initialize() {
            this.getCategories();
            let identifier = this.$route.params.id;
            if (identifier === 'create') {
                this.creationInitialize();
            } else {
                this.pk = identifier;
                this.getInstance();
            }
        },
        creationInitialize() {
            this.instance = {
                vendor_code: '',
                name: '',
                description: '',
                url: '',
                price: 0,
                old_price: 0,
                is_in_stock: true,
                is_bestseller: false,
                is_published: false,
                is_new_product: false,
                attributes: {},
                scoring: 0,
                category_id: null,
                _meta_title: '',
                _meta_description: '',
                _meta_keywords: ''
            }
            this.copyInstance();
            this.loading = false;
            this.initialized = true;
        },
        saveChanges() {
            if (this.pk === null) {
                this.createInstance();
            } else {
                if (this.hasChanged) {
                    this.updateInstance();
                }
                if (this.imagesChanged) {
                    this.$refs.images.saveChanges()
                }
            }
        },
        getInstance() {
            this.loading = true;
            request.get(`/products/${this.pk}/`).then(
                response => {
                    this.handleSuccessfulGetReponse(response);
                },
                response => {
                    this.handleFailedGetResponse(response);
                }
            )
        },
        createInstance() {
            this.loading = true;
            request.post('/products/', this.instance).then(
                response => {
                    this.handleSuccessfulCreateResponse(response);
                },
                response => {
                    this.handleFailedCreateResponse(response);
                }
            )
        },
        updateInstance() {
            this.loading = true;
            delete this.instance.image;
            delete this.instance.thumbnail;
            request.put(`/products/${this.pk}/`, this.instance).then(
                response => {
                    this.handleSuccessfulUpdateResponse(response);
                },
                response => {
                    this.handleFailedUpdateResponse(response);
                }
            )
        },
        deleteInstance() {
            this.loading = true;
            request.delete(`/products/${this.pk}/`).then(
                response => {
                    this.handleSuccessfulDeleteResponse(response);
                },
                response => {
                    this.handleFailedDeleteResponse(response);
                }
            )
        },
        handleSuccessfulGetReponse(response) {
            this.instance = response.data;
            this.copyInstance();
            if (this.initialized === false) {
                this.initialized = true;
            }
            this.loading = false;
        },
        handleFailedGetResponse(response) {
        },
        handleSuccessfulCreateResponse(response) {
            this.instance = response.data;
            this.pk = this.instance.id;
            this.hasChanged = false;
            this.copyInstance();
            this.loading = false;
            this.$notify({
                title: 'Успешно',
                message: 'Товар успешно сохранён',
                type: 'success'
            });
        },
        handleFailedCreateResponse(response) {
            this.$notify.error({
                title: 'Ошибка',
                message: 'Во время сохранения произошла ошибка',
            });
        },
        handleSuccessfulUpdateResponse(response) {
            this.instance = response.data;
            this.hasChanged = false;
            this.copyInstance();
            this.loading = false;
            this.$notify({
                title: 'Успешно',
                message: `Товар ${this.instance.vendor_code} успешно обновлён`,
                type: 'success'
            });
        },
        handleFailedUpdateResponse(response) {
            this.$notify.error({
                title: 'Ошибка',
                message: 'Во время сохранения произошла ошибка',
            });
        },
        handleSuccessfulDeleteResponse(response) {
            this.$notify({
                title: 'Успешно',
                message: `Товар ${this.instance.vendor_code} успешно удалён`,
                type: 'success'
            });
            this.$router.push({path: '/products/'});
        },
        handleFailedDeleteResponse(response) {
            this.$notify.error({
                title: 'Ошибка',
                message: 'Во время удаления произошла ошибка',
            });
        },
        copyInstance() {
            this.instanceProxy = JSON.parse(JSON.stringify(this.instance));
        },
        rollbackChanges() {
            this.instance  = JSON.parse(JSON.stringify(this.instanceProxy));
        },
        checkForChanges() {
            this.hasChanged = !equal(this.instance, this.instanceProxy);
        },
        triggerDelete() {

        },
        getCategories() {
            request.get('/categories/').then(
                response => {
                    this.handleSuccessfilGetCategoriesResponse(response);
                },
                response => {
                    this.handleFailedGetCategoriesResponse(response);
                }
            )
        },
        handleSuccessfilGetCategoriesResponse(response) {
            this.categoriesOptions = response.data;
            this.categoriesReceived = true;
        },
        handleFailedGetCategoriesResponse(response) {

        },
        handleImagesChange(status) {
            this.imagesChanged = status;
        },
        handleNameInput() {
            console.log('tost')
            this.instance.url = cyrillToLatin(this.instance.name).replace(/ /g,"-").toLowerCase();
        }
    },
    watch: {
        instance: {
            handler() {
                if (this.initialized) {
                    this.checkForChanges();
                }
            },
            deep: true
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .app-view-controls {
        padding: 10px 0px 30px 0px;
    }
    .field {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }
    .field_block {
        display: block;
        .field-label {
            margin-bottom: 10px;
        }
    }
    .field-label {
        margin-right: 20px;
        width: 140px;
    }
    .field-value {
        width: 100%;
    }
</style>
