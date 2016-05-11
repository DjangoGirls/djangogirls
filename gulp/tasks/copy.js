var gulp = require('gulp'),
  config = require('../config'),
  environments = require('gulp-environments');

var development = environments.development;
var production = environments.production;


gulp.task('copyfiles', ['clean'], function(){
  var dest = production() ? config.paths.copy.dest.production : config.paths.copy.dest.development;
  return gulp.src(config.paths.copy.src)
    .pipe(gulp.dest(dest))
});