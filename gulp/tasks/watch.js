var gulp = require('gulp'),
  config = require('../config');


gulp.task('watch', ['styles'], function () {
  gulp.watch(config.paths.css.src, ['styles']);
});
