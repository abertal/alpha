var data = {
  username: '',
  password: ''
}

/* eslint-disable no-new */
/* eslint-disable no-undef */
new Vue({
  el: '#app',
  data: data,
  methods: {
    setLoading: function (message) {
      var el = message.target
      el.disabled = true
      el.setAttribute('value', el.getAttribute('data-loading-text'))
    }
  },
  delimiters: ['${', '}']
})
