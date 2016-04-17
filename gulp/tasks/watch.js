var gulp = require('gulp'),
  config = require('../config');


gulp.task('watch', ['styles', 'scripts'], function () {
  gulp.watch(config.paths.css.src, ['styles']);
  gulp.watch(config.paths.js.src, ['scripts']);
});
