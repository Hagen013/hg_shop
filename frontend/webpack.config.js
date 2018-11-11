const webpack = require("webpack");
const path = require("path");

var CopyWebpackPlugin = require('copy-webpack-plugin');


module.exports = {
  context: path.resolve(__dirname, "./src/js"),

  entry: {
    scripts: './scripts.js',
    categoryPage: './categoryPage.js',
    productPage: './productPage.js',
    cartPage: './cartPage.js',
    orderPage: './orderPage.js',
    infoPage: './infoPage.js',
    adminLogin: './adminLogin.js',
    admin: './admin.js'
  },

  output: {
    path: path.resolve(__dirname, "./static/js"),
    publicPath: "/static/js/",
    filename: "[name].js"
  },

  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: "vue-loader",
        options: {
          loaders: {
            scss: "vue-style-loader!css-loader!sass-loader",
            sass: "vue-style-loader!css-loader!sass-loader?indentedSyntax",
            js: 'babel-loader?presets[]=es2015,presets[]=es2016&plugins=dynamic-import-webpack'
          }
        }
      },
      {
        test: /\.js$/,
        loader: "babel-loader",
        exclude: /node_modules/,
        query: {
          presets: ['es2015', 'es2016'],
          plugins: ["dynamic-import-webpack"]
        }
      },
      {
        test: /\.css$/,
        use: [ 'style-loader', 'css-loader' ]
      },
      {
        test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
        use: [{
            loader: 'file-loader',
            options: {
                name: '[name].[ext]',
                outputPath: 'fonts/'
            }
        }]
      }
    ]
  },
  resolve: {
    modules: [path.resolve(__dirname, "./src"), "node_modules"],
    alias: {
      vue$: "vue/dist/vue.common.js"
    }
  },
  devtool: 'source-map',
  devServer: {
    publicPath: "/static/js/",
    disableHostCheck: true,
    proxy: {
      "/": "http://localhost:8000"
    }
  },
};

module.exports.plugins = (module.exports.plugins || []).concat([

  new webpack.optimize.CommonsChunkPlugin({
    name: 'common',
    filename: 'common.js',
    chunks: [
      'scripts',
      'categoryPage',
      'productPage',
      'cartPage',
      'orderPage',
      'infoPage'
    ]
  }),

  new CopyWebpackPlugin([
    { from: './jquery-3.3.1.min.js', to: "./jquery-3.3.1.min.js" },
    { from: './plugins/jquery.elevateZoom-3.0.8.min.js', to: "./jquery.elevateZoom-3.0.8.min.js" },
    { from: './plugins/jQuery.verticalCarousel.js', to: "./jQuery.verticalCarousel.js" },
    { from: './plugins/owl.carousel.min.js', to: "./owl.carousel.min.js" },
    { from: './assets/', to: "./assets/" },
  ]),

]);

if (process.env.NODE_ENV === "production") {
  module.exports.devtool = false;

  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.optimize.UglifyJsPlugin({
      comments: false,
      compress: { warnings: false }
    })
  ])

}

