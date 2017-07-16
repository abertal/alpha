console.log('Aqui')

var data = {
  message: 'Greetings your majesty!'
}

/* eslint-disable no-new */
/* eslint-disable no-undef */
new Vue({
  el: '#app',
  data: data,
  delimiters: ['${', '}']
})
