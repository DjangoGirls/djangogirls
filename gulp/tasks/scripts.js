var gulp = require('gulp'),
  config = require('../config'),
  environments = require('gulp-environments'),
  uglify = require('gulp-uglify');

var development = environments.development;
var production = environments.production;


gulp.task('scripts', ['clean'], function(){
  var dest = production() ? config.paths.js.dest.production : config.paths.js.dest.development;
  return gulp.src(config.paths.js.src)
    .pipe(production(uglify()))
    .pipe(gulp.dest(dest))
});