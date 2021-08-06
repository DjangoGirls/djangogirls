var gulp = require('gulp'),
  config = require('../config');


gulp.task('watch', gulp.series('styles', 'scripts', 'copyfiles'), function () {
  gulp.watch(config.paths.css.src, ['styles']);
  gulp.watch(config.paths.js.src, ['scripts']);
  gulp.watch(config.paths.copy.src, ['copyfiles']);
});
