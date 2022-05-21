//vue.config.js
module.exports = {
    pages: {
        // client: {
        //     entry: 'src/main.js',
        //     template: 'public/client/index.html',
        //     filename: 'index.html',
        //     title: 'Client',
        //     chunks: ['chunk-vendors', 'rather-than-package-json', 'client'],
        // },
        employee: {
            entry: './src/employee/main.js',
            template: 'public/employee/index.html',
            filename: 'employee/index.html',
            title: 'Employee',
            chunks: ['chunk-vendors', 'any-other-chunk', 'employee'],
        },
      //...
    },
  }