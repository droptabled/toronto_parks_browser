const glob = require("glob");
const path = require('path');

var entries = {};
glob.sync("./browser/src/pages/*.js").map((str) => {
    var basename = path.basename(str)
    entries[basename] = str
});

module.exports = {
    entry: entries,
    output: {
        path: path.resolve(__dirname, './static/browser/js'),
        filename: '[name]',
    },
    module: {
        rules: [
        {
            test: /\.js$/,
            exclude: /node_modules/,
            use: {
                loader: "babel-loader"
            }
        }
        ]
    },
    cache: false,
};