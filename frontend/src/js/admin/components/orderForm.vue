<template>
    <md-content v-if="showForm">
        <div class="order-form--top-bar">
            <div class="md-layout">
                <div class="md-layout-item">
                </div>
                <div class="md-layout-item">
                </div>
                <div class="md-layout-item">
                    <div class="order-form--controls">
                        <md-button class="md-accent md-raised"
                            @click="rollbackChanges"
                        >
                            Отменить
                        </md-button>
                        <md-button class="md-primary md-raised"
                            @click="saveChanges"
                        >
                            Сохранить
                        </md-button>
                    </div>
                </div>
            </div>
        </div>
        <div class="md-layout">
            <div class="md-layout-item column">
                <md-field>
                    <label>Имя клиента</label>
                    <md-input v-model="order.name"></md-input>
                </md-field>
                <md-field>
                    <label>Телефон</label>
                    <md-input v-model="order.phone"></md-input>
                </md-field>
                <md-field>
                    <label>Email</label>
                    <md-input v-model="order.email"></md-input>
                </md-field>
                <md-field>
                    <label>Адрес</label>
                    <md-input v-model="order.address"></md-input>
                </md-field>
            </div>
            <div class="md-layout-item column">
                <md-field>
                    <label>Создан</label>
                    <md-input v-model="createdAtFormated" readonly></md-input>
                </md-field>
                <md-field>
                    <label>Последнее изменение</label>
                    <md-input v-model="modifiedAtFormated" readonly></md-input>
                </md-field>
            </div>
            <div class="md-layout-item">
            </div>
        </div>
    </md-content>
</template>

<script>
import normalizeNumber from '../../core/normalizeNumber'

export default {
    name: 'orderForm',
    data: () => ({
        pk: null,
        ordersApiUrl: '/api/orders/',
        orderApiResponseRecieved: false,
        orderApiResponseFailed: false,
        order: {
            id: null,
            name: '',
            phone: '',
            email: '',
            address: '',
            created_at: '',
            modified_at: '',
            notified: '',
            order_text: '',
            status: null
        }
    }),
    created() {
        this.pk = this.$route.params.id;
        this.getInitialData();
    },
    computed: {
        createdAtFormated() {
            return this.formatDate(this.order.created_at)
        },
        modifiedAtFormated() {
            return this.formatDate(this.order.modified_at)
        },
        showForm() {
            return (this.orderApiResponseRecieved && (!this.orderApiResponseFailed))
        }
    },
    methods: {
        getInitialData() {
            this.getOrder(this.pk);
        },
        getOrder(pk) {
            let url = this.ordersApiUrl + String(this.pk);
            this.orderApiResponseRecieved = false;
            this.orderApiResponseFailed = false;

            this.$http.get(url).then(
                response => {
                    this.hanleSuccesfulOrderGetResponse(response);
                },
                response => {
                    this.handleFailedOrderGetResponse(response);
                }
            )
        },
        hanleSuccesfulOrderGetResponse(response) {
            this.orderApiResponseRecieved = true;
            this.order = response.body;
        },
        handleFailedOrderGetResponse(response) {
            this.orderApiResponseFailed = true;
            this.orderApiResponseRecieved = true;
        },
        saveChanges() {

        },
        rollbackChanges() {

        },
        formatDate(dateString) {
            let date = new Date(dateString);
            let year = date.getFullYear();
            let month = normalizeNumber(date.getMonth()+1);
            let day = normalizeNumber(date.getDate());
            let minutes = normalizeNumber(date.getMinutes());
            let hours = normalizeNumber(date.getHours());
            let seconds = normalizeNumber(date.getSeconds());
            return `${day}.${month}.${year} ${hours}:${minutes}:${seconds}`
        },
    },
    watch: {
        order: {
            deep: true,
            handler() {

            }
        }
    }
}
</script>

<style lang="scss">
    .column {
        padding-left: 16px;
    }
    .order-form--controls {
        width: 100%;
        display: flex;
        justify-content: flex-end;
    }
</style>


