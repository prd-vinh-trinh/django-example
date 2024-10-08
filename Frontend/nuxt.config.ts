// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  // Using if wanna try nuxt 4 structure
  // future: {
  //   compatibilityVersion: 4
  // },

  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss', '@pinia/nuxt'],
})