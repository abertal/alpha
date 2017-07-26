var path = require('path');

module.exports = {
  entry: './webapp/assets/js/home.js',
  output: {
    filename: 'home.bundle.js',
    path: path.resolve(__dirname, 'webapp/static/js/')
  }
};

