var gulp = require('gulp'),
  config = require('../config'),
  gutil = require('gulp-util'),
  stylus = require('gulp-stylus'),
  environments = require('gulp-environments');

var development = environments.development;
var production = environments.production;


gulp.task('styles', ['clean'], function(){
  var dest = production() ? config.paths.css.dest.production : config.paths.css.dest.development;
  var compress = production()
  return gulp.src(config.paths.css.src)
    .pipe(stylus({
      compress: production()
    }))
    .pipe(gulp.dest(dest))
});
