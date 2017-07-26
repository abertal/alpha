var path = require('path')

module.exports = {
  entry: {
    'home': './webapp/assets/js/home.js',
    'login': './webapp/assets/js/login.js'
  },
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, 'webapp/static/js/')
  },
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js' // Use ES Module build
    }
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader'
      }
    ]
  }
}
