var gulp = require('gulp'),
  config = require('../config');


gulp.task('local', ['styles', 'scripts', 'copyfiles']);
