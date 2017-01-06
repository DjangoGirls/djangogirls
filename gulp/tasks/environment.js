var gulp = require('gulp'),
  environments = require('gulp-environments'),
  gutil = require('gulp-util');

var development = environments.development;
var production = environments.production;


gulp.task('set-production', function(){
    gutil.log('Setting environment to production');
    environments.current(production);
});
