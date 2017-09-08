import Vue from 'vue'
import SearchPerson from './components/SearchPerson.vue'
import BootstrapAlpha from './bootstrapAlpha.js'

/* eslint-disable no-new */
/* eslint-disable no-undef */
new Vue({
  el: '#app',
  components: {
    'search-person': SearchPerson
  },
  delimiters: ['${', '}'],
  data: {
    newCustodians: [],
    removedCustodiansIds: []
  },
  computed: {
    newCustodiansIds: function() {
      return this.newCustodians.map((item) => {
        return item.id
      })
    }
  },
  methods: {
    onSelectCustodian: function (person) {
      if (this.newCustodiansIds.indexOf(person.id) === -1) {
        this.newCustodians.push(person)
      }
      let index = this.removedCustodiansIds.indexOf(person.id)
      if (index > -1) {
        this.removedCustodiansIds.splice(index, 1)
      }
    },
    removeCustodian: function (personId, event) {
      event.preventDefault()
      this.removedCustodiansIds.push(personId)
    },
    isVisible: function(personId) {
      return this.removedCustodiansIds.indexOf(personId)
    }
  },
  mounted: function () {
    BootstrapAlpha.navtabs($)
  }
})
