<template>
	<div class="cart-items__wrapper">
		<cart-item v-for="(item, key) in cartProxy.items"
			:key=key
			:item=item
		>
		</cart-item>
		<div class="clearfix">
		</div>
	</div>
</template>

<script>
	import cartItem from './cartItem.vue'

    export default {
		name: 'cart-items',
		components: {
			'cart-item': cartItem,
		},
        computed: {
            cartProxy() {
                return this.$store.state.cart.cart
            },
        },
        methods: {
		},
		watch: {
			cartProxy: {
				handler: function() {
				},
				deep: true
			}
		}
    }
</script>

<style lang="scss" scoped>
</style>