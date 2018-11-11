<template>
    <md-content class="orders">
        <div class="md-layout">
            <md-card class="orders__list">
                <md-card-content>
                    <table class="table">
                        <tbody>
                            <tr class="table-row">
                                <th class="table-head">
                                    <div class="table-head-container">
                                        <div class="table-head-label">
                                            №
                                        </div>
                                    </div>
                                </th>
                                <th class="table-head">
                                    <div class="table-head-container">
                                        <div class="table-head-label">
                                        СОЗДАН
                                        </div>
                                    </div>
                                </th>
                                <th class="table-head">
                                    <div class="table-head-container">
                                        <div class="table-head-label">
                                        Сумма
                                        </div>
                                    </div>
                                </th>
                                <th class="table-head">
                                    <div class="table-head-container">
                                        <div class="table-head-label">
                                        Имя клиента
                                        </div>
                                    </div>
                                </th>
                                <th class="table-head">
                                    <div class="table-head-container">
                                        <div class="table-head-label">
                                        Почта
                                        </div>
                                    </div>
                                </th>
                                <th class="table-head">
                                    <div class="table-head-container">
                                        <div class="table-head-label">
                                        Телефон
                                        </div>
                                    </div>
                                </th>
                            </tr>
                            <tr class="table-row" v-for="order in currentOrders"
                                :key=order.id
                            >
                                <td class="table-cell table-cell--colored">
                                    <a class="table-cell-container table-cell-container--clickable"
                                        @click="orderFormRedirect(order)"
                                    >
                                        <span class="md-body-2">{{order.id}}</span>
                                    </a>
                                </td>
                                <td class="table-cell table-cell-colored">
                                    <div class="table-cell-container table-cell-container--time">
                                        {{order.created_at | dataFilter}}
                                    </div>
                                </td>
                                <td class="table-cell table-cell-colored">
                                    <div class="table-cell-container table-cell-container--time">
                                        {{order.total_price}} ₽
                                    </div>
                                </td>
                                <td class="table-cell table-cell-colored">
                                    <div class="table-cell-container table-cell-container--time">
                                        {{order.name}}
                                    </div>
                                </td>
                                <td class="table-cell table-cell-colored">
                                    <div class="table-cell-container table-cell-container--time">
                                        {{order.email}}
                                    </div>
                                </td>
                                <td class="table-cell table-cell-colored">
                                    <div class="table-cell-container table-cell-container--time">
                                        {{order.phone}}
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </md-card-content>
            </md-card>
        </div>
    </md-content>
</template>

<script>
import normalizeNumber from '../../core/normalizeNumber'

export default {
    name: 'ordersList',
    data: () => ({
        apiListUrl: '/api/orders/',
        apiListResponseRecieved: false,
        apiListReponseFailed: false,
        currentOrders: [],
        totalOrdersCount: 0,
        previousPage: null,
        nextPage: null
    }),
    created() {
        this.getInitialData();
    },
    methods: {
        getInitialData() {
            this.getOrdersList();
        },
        getOrdersList() {
            this.apiListResponseRecieved = false;
            this.$http.get(this.apiListUrl).then(
                response => {
                    this.handleSuccesfulListApiResponse(response);
                },
                response => {
                    this.handleFailedListApiResponse(response);
                }
            )
        },
        handleSuccesfulListApiResponse(response) {
            this.apiListResponseRecieved = true;
            this.apiListReponseFailed = false;
            this.currentOrders = response.body.results;
            this.totalOrdersCount = response.body.count;
            this.previousPage = response.body.previosPage;
            this.nextPage = response.body.next;
        },
        handleFailedListApiResponse(response) {
            this.apiListReponseFailed = true;
        },
        orderFormRedirect(order) {
            let orderPath = `order/${order.id}`;
            this.$router.replace({path: orderPath});
        }
    },
    filters: {
        dataFilter(dataString) {
            let date = new Date(dataString);
            let year = date.getFullYear();
            let month = normalizeNumber(date.getMonth()+1);
            let day = normalizeNumber(date.getDate());
            let minutes = normalizeNumber(date.getMinutes());
            let hours = normalizeNumber(date.getHours());
            let seconds = normalizeNumber(date.getSeconds());
            return `${day}.${month}.${year} ${hours}:${minutes}:${seconds}`
        },
        capitalize(value) {
            if (!value) return ''
            value = value.toString()
            return value.charAt(0).toUpperCase() + value.slice(1)
        },
    }
}
</script>

<style lang="scss">
    $primary: #448aff;
    $accent: #F44336;
    $success: #00BFA5;

    .orders__list {
        width: 100%;
        .table {
            width: 100%;
        }
    }
    .table-cell-container {
        display: block;
        text-align: center;
    }
    .table-head {
        color: rgba(0,0,0,.54);
    }
    .table-row {
        &:nth-child(odd) {
            background: rgba(27,54,100,0.03);
        }
    }
    .table-row--new {
        .table-cell--colored {
            color: $success;
            a {
                color: $success;
            }
        }
    }
    .table-row--err {
        .table-cell--colored {
            color: $accent;
            a {
                color: $accent;
            }
        }
    }
    .table-row--done {
        .table-cell--colored {
            color: $primary;
            a {
                color: $primary;
            }
        }
    }
    .table-head-container {
        height: 56px;
        padding: 14px 0;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .table-head-label {
        height: 28px;
        padding-right: 32px;
        padding-left: 24px;
        display: inline-block;
        position: relative;
        line-height: 28px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .table-cell {
        position: relative;
        height: 48px;
        font-size: 13px;
        line-height: 18px;
    }
    .table-cell-container {
        padding: 6px 32px 6px 24px;
    }
    .table-cell-container--clickable {
        cursor: pointer;
    }
</style>


