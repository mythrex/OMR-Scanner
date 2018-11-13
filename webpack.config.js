// var HtmlWebpackPlugin = require('html-webpack-plugin');
var LiveReloadPlugin = require('webpack-livereload-plugin');

module.exports = {
	entry: './client/index.js',
	output: {
		path: '/',
		filename: 'bundle.js'
	},
	mode: 'development',
	module: {
		rules: [
			{
				use: ['style-loader', 'css-loader'],
				test: /\.css$/
			},
			{
				test: /\.sass|\.scss$/,
				use: [
					{
						loader: 'style-loader'
					},
					{
						loader: 'css-loader',
						options: {
							sourceMap: true
						}
					},
					{
						loader: 'sass-loader',
						options: {
							sourceMap: true
						}
					}
				]
			}
		]
	},
	plugins: [new LiveReloadPlugin()]
};
