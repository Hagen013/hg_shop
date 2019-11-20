<template>
    <div class="dashboard-container" v-loading="loading">
        <div class="view-container">
            <div class="view-controls">
                <el-button type="primary"
                    @click="instanceRedirect()"
                >
                    Создать
                </el-button>
                <div class="pagination">
                    <div class="pagination--page-size">
                        <div class="field">
                            <div class="field-label">
                                Отображать по
                            </div>
                            <el-select v-model="pageSize"
                                size="medium"
                            >
                                <el-option
                                    v-for="option in pageSizeOptions"
                                    :key="option.value"
                                    :label="option.label"
                                    :value="option.value"
                                >
                                </el-option>
                            </el-select>
                        </div>
                    </div>
                    <div class="pagination--info">
                        <div class="pagination--current-count">
                            {{offset}} - {{currentCount}}
                        </div>
                        <span class="pagination--delimeter">из</span>
                        <div class="pagination--total-count">
                            {{totalCount}}
                        </div>
                    </div>
                    <div class="pagination--buttons">
                        <el-button circle
                            :disbled="!hasPreviousPage"
                            @click="previousPage"
                        >
                            <i class="el-icon-back"></i>
                        </el-button>
                        <el-button circle
                            :disabled="!hasNextPage"
                            @click="nextPage"
                        >
                            <i class="el-icon-right"></i>
                        </el-button>
                    </div>
                </div>
            </div>
            <div class="view-filters">
                <div class="search">
                    <el-input
                        placeholder="Поиск по артикулу"
                        prefix-icon="el-icon-search"
                        v-model="searchProxy"
                        size="medium"
                    >
                    </el-input>
                </div>
            </div>
            <div class="view-content">
                <table class="table">
                    <tr class="table-heading">
                        <th class="table-head">
                            <div class="table-label">
                                Фото
                            </div>
                        </th>
                        <th class="table-head">
                            <div class="table-label">
                                Артикул
                            </div>
                        </th>
                        <th class="table-head">
                            <div class="table-label">
                                Цена
                            </div>
                        </th>
                        <th class="table-head">
                            <div class="table-label">
                                Создан
                            </div>
                        </th>
                        <th class="table-head">
                            <div class="table-label">
                                В наличии
                            </div>
                        </th>
                    </tr>
                    <tr class="table-row" v-for="item in results" :key="item.id" @click="instanceRedirect(item.id)">
                        <td class="table-cell">
                            <div class="table-contaier">
                                <div class="image-wrapper">
                                    <img :src="item.thumbnail">
                                </div>
                            </div>
                        </td>
                        <td class="table-cell">
                            <div class="table-container">
                                {{item.vendor_code}}
                            </div>
                        </td>
                        <td class="table-cell">
                            <div class="table-container">
                                {{item.price}} ₽
                            </div>
                        </td>
                        <td class="table-cell">
                            <div class="table-container">
                                {{item.created_at|dateFilter}}
                            </div>
                        </td>
                        <td class="table-cell">
                            <div class="table-container">
                                {{item.is_in_stock|avaiabilityFilter}}
                            </div>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
</template>
<script>
import request from '@/utils/request'
import normalizeNumber from '@/utils/normalizeNumber'
import debounce from 'debounce'


export default {
    name: 'Products',
    data: () => ({
        loading: true,
        pageSize: 100,
        offset: 0,
        limit: 100,
        totalCount: 0,
        results: [],
        pageSizeOptions: [
            {label: '50', value: 50},
            {label: '100', value: 100},
            {label: '200', value: 200}
        ],
        listApi: '/products/',
        searchProxy: '',
        search: ''
    }),
    computed: {
        queryParams() {
            let params = {
                limit: this.limit,
                offset: this.offset  
            }
            if (this.search.length > 0) {
                params.vendor_code=this.search;
            }
            return params
        },
        currentCount() {
            return (this.offset + this.limit)
        },
        hasPreviousPage() {
            return this.offset > 0
        },
        hasNextPage() {
            return this.currentCount < this.totalCount;
        },
    },
    created() {
        this.initialize();
    },
    methods: {
        initialize() {
            this.getList();
        },
        getList() {
            this.loading = true;
            request.get(this.listApi, {params: this.queryParams}).then(
                response => {
                    this.handleSuccessfulGetListResponse(response)
                },
                response => {
                    this.handleFailedGetListResponse(response);
                }
            )
        },
        handleSuccessfulGetListResponse(response) {
            this.totalCount = response.data.count;
            this.results = response.data.results;
            this.loading = false;
        },
        handleFailedGetListResponse(response) {
            this.loading = false;
        },
        previousPage() {
            this.offset -= this.pageSize;
        },
        nextPage() {
            this.offset += this.pageSize;
        },
        instanceRedirect(pk) {
            if (pk === undefined) {
                this.$router.push({path: `/products/create/`});
            } else {
                this.$router.push({path: `/products/${pk}/`});
            }
        }
    },
    watch: {
        queryParams: {
            handler() {
                this.getList();
            },
            deep: true
        },
        searchProxy: {
            handler: debounce(function(value) {
                this.search = this.searchProxy;
            }, 500)
        }
    },
    filters: {
        avaiabilityFilter(value) {
            if (value) {
                return 'Да'
            }
            return 'Нет'
        },
        dateFilter(dataString) {
            let date = new Date(dataString);
            let year = date.getFullYear();
            let month = normalizeNumber(date.getMonth()+1);
            let day = normalizeNumber(date.getDate());
            return `${day}.${month}.${year}`
        },
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .view-container {
        padding: 30px 10px;
    }
    .view-controls {
        display: flex;
        align-items: center;
    }
    .view-filters {
        padding: 20px 0px 10px 0px;;
    }
    .pagination {
        display: flex;
        margin-left: 50px;
        justify-content: flex-start;
        align-items: center;
    }
    .pagination--page-size {
        display: flex;
        margin-right: 20px;
    }
    .pagination--delimeter {
        margin: 0px 10px;
    }
    .pagination--info {
        display: flex;
    }
    .pagination--info {
        margin-right: 20px;
    }
    .field {
        display: flex;
        align-items: center;
    }
    .field-label {
        margin-right: 20px;
    }
    .search {
        max-width: 400px;
    }
    .image-wrapper {
        height: 80px;
        width: 80px;
        text-align: center;
        img {
            height: 100%;
            width: auto;
        }
    }
</style>
