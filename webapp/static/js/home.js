
var data = {
  loading: false,
  response: null,
  person: null,
  results: null
}

/* eslint-disable no-new */
/* eslint-disable no-undef */
var vm = new Vue({
  el: '#app',
  data: data,
  methods: {
    clickSearch: function (message) {
      var el = message.target
      el.setAttribute('value', 'Buscando...')
      vm.results = []
      vm.loading = true
      axios.get('/webapp/ajax/person/')
      .then(function (response) {
        vm.response = response
        console.dir(response)
        vm.results = [{name: 'A'}, {name: 'B'}]
        el.setAttribute('value', 'Buscar')
        vm.loading = false
      })
    }
  },
  delimiters: ['${', '}']
})
