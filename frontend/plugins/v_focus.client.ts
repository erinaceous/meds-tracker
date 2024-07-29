export default defineNuxtPlugin((nuxtApp) => {
    return nuxtApp.vueApp.directive('v-focus', {
        mounted (el) {
            this.$nextTick(() => {
                el.focus()
            })
        }
    })
})