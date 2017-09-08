import Vue from 'vue'
import SearchPerson from './components/SearchPerson.vue'

/* eslint-disable no-new */
/* eslint-disable no-undef */
new Vue({
  el: '#app',
  components: {
    'search-person': SearchPerson
  },
  delimiters: ['${', '}'],
  methods: {
    onSelectPerson: function (personId) {
      alert(personId)
    }
  }
})
