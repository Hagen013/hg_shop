<template>
    <md-dialog
        :md-active="showDialog"
        class="login-form"
        v-on:keyup.enter="submit"
        @input="resetAtuhError"
    >
        <md-dialog-title>
            Вход
        </md-dialog-title>
        <div class="login-form__content">

            <md-field md-clearable :class="messageClass">
                <label>Логин</label>
                <md-input v-model="username"></md-input>
            </md-field>

            <md-field :class="messageClass">
                <label>Пароль</label>
                <md-input v-model="password" type="password"></md-input>
            </md-field>

            <div class="login-form__controls">
                <md-button class="md-primary md-raised"
                    @click="submit"
                >
                    Далее
                </md-button>
            </div>

        </div>  
    </md-dialog>
</template>

<script>
    export default {
        name: 'login-form',
        data: () => ({
            showDialog: true,
            username: '',
            password: '',
            loginApiUrl: '/api/users/admin/login/',
            redirectUrl: '/md-admin/',
            authFailed: false
        }),
        computed: {
            messageClass() {
                return {
                    'md-invalid': this.authFailed
                }
            }
        },
        methods: {
            submit() {
                let data = new FormData();

                data.append("username", this.username);
                data.append("password", this.password);

                this.$http.post(this.loginApiUrl, data).then(
                    response => {
                        this.handleSuccessfulResponse(response);
                    },
                    response => {
                        this.handleFailedResponse(response);
                    }
                )
            },
            handleSuccessfulResponse(response) {
                window.location.href = this.redirectUrl;
            },
            handleFailedResponse(response) {
                this.authFailed = true;
            },
            resetAtuhError() {
                this.authFailed = false;
            }
		}
    }
</script>

<style lang="scss" scoped>
    .login-form {
        min-width: 480px;
    }
    .login-form__content {
        padding: 0px 16px 32px 16px;
    }
    .login-form__controls {
        display: flex;
        justify-content: flex-end;
    }
</style>
