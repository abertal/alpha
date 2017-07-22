
var data = {
  loading: false,
  response: null,
  personId: null,
  results: null,
  searchString: null
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
      vm.personId = null
      vm.results = []
      vm.loading = true
      axios.get('/webapp/ajax/person/')
      .then(function (response) {
        vm.response = response
        vm.results = response.data.data
        el.setAttribute('value', 'Buscar')
        vm.loading = false
      })
    },
    selectPerson: function (personId) {
      vm.personId = personId
    }
  },
  delimiters: ['${', '}']
})
