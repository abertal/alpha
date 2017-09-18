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
    newCustodian: null,
    removedCustodiansIds: []
  },
  computed: {
    newCustodianId: function () {
      return this.newCustodian ? this.newCustodian.id : ''
    }
  },
  methods: {
    onSelectCustodian: function (person) {
      this.newCustodian = person
    },
    removeCustodian: function (personId, event) {
      event.preventDefault()
      if (this.newCustodian && (personId === this.newCustodian.id)) {
        this.newCustodian = null
      }
      this.removedCustodiansIds.push(personId)
    },
    isVisible: function (personId) {
      return this.removedCustodiansIds.indexOf(personId)
    }
  },
  mounted: function () {
    BootstrapAlpha.navtabs($)
  }
})
