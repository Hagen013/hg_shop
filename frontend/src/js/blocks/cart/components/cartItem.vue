<template>
    <div class="cart-item">
        <div class="cart-item__image">
            <img :src="item.product.thumbnail" alt="Изображение"/>
        </div>
        <div class="cart-item__stats">
            <div class="cart-item__name">
                <a :href="item.product.absolute_url">{{ item.product.name }}</a>
            </div>
            <div class="cart-item__code">
                Артикул: {{ item.product.vendor_code }}
            </div>
        </div>
        <div class="cart-item__price">
            <div class="cart-item__price-title">
                Цена
            </div>
            <div class="cart-item__subtotal-price">
                <span>{{ item.price }}</span><span class="cart-item__currency">р.</span>
            </div>
            <div class="cart-item__quantity">
                <a class="quantity-minus inc-button"
                    @click="decrement(item)"
                >
                </a>
                <input type="text"
                    class="cart-item__input"
                    v-model="item.quantity"
                    maxlength="3"
                >
                <a class="quantity-plus inc-button"
                    @click="increment(item)"
                >
                </a>
                <div class="clearfix">
                </div>
            </div>
            <div class="cart-item__delete"
                @click="deleteItem"
            >
                <input type="submit" value="Удалить">
            </div>
        </div>
        <div class="clearfix">
        </div>
    </div>
</template>

<script>
    export default {
        name: 'cart-item',
        props: [
            'item'
        ],
        methods: {
			decrement() {
                if (this.item.quantity > 1) {
                    let quantity = this.item.quantity;
                    quantity -= 1;
                    let data = new FormData();
                    data.append('pk', this.item.product.id);
                    data.append('quantity', quantity);
                    this.$store.dispatch('cart/update', data);
                }
			},
			increment() {
                let quantity = this.item.quantity;
                quantity += 1;
                let data = new FormData();
                data.append('pk', this.item.product.id);
                data.append('quantity', quantity);
                this.$store.dispatch('cart/update', data);
            },
            deleteItem() {
                let data = {
                    'pk': this.item.product.id
                }
                this.$store.dispatch('cart/delete', data);
            }
		}
    }
</script>

<style lang="scss" scoped>
</style>