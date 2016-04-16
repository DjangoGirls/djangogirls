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
    },
    manifest: './static/',
    revisioning: ['./static/build/css/*.css']
  }
};
