module.exports = {
  paths: {
    project: './',
    build: './static/build/',
    css: {
      src: [
        './static/source/css/*.styl',
        '!./static/source/css/common.styl'
      ],
      dest: {
        production: './static/build/css/',
        development: './static/local/css/',
      },
      bundles: {
        global: [
          './node_modules/bootstrap/dist/css/bootstrap.min.css',
          './static/source/vendor/css/sss.css',
          './static/source/vendor/css/mapbox.min.css',
          './temp/global.css'
        ],
        community: [
          './node_modules/bootstrap/dist/css/bootstrap.min.css',
          './temp/community.css'
        ],
        event: [
          './node_modules/bootstrap/dist/css/bootstrap.min.css',
          './temp/event.css'
        ],
      }
    },
    js: {
      src: [
        './static/source/js/*.js'
      ],
      dest: {
        production: './static/build/js/',
        development: './static/local/js/',
      }
    },
    manifest: './static/',
    revisioning: ['./static/build/css/*.css', './static/build/js/*.js'],
    temp: './temp/'
  }
};
