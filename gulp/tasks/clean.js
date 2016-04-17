var gulp = require('gulp'),
  config = require('../config'),
  clean = require('gulp-clean');


gulp.task('clean', function () {
  return gulp.src(config.paths.build, {read: false})
    .pipe(clean({force: true}));
});
