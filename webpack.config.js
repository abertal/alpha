var path = require('path')
var ExtractTextPlugin = require('extract-text-webpack-plugin')

let extractLESS = new ExtractTextPlugin('../css/[name].css')

module.exports = {
  entry: {
    'alpha': './webapp/assets/js/alpha.js',
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
        test: /\.less$/,
        loader: extractLESS.extract(['css-loader', 'less-loader'])
      },
      {
        test: /\.vue$/,
        loader: 'vue-loader'
      }
    ]
  },
  plugins: [
    extractLESS
  ]
}
