//vue.config.js
module.exports = {
    pages: {
        client: {
            entry: './src/client/main.js',
            template: 'public/client/index.html',
            filename: 'client/index.html',
            title: 'Client',
            chunks: ['chunk-vendors', 'any-other-chunk', 'client'],
        },
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