'use strict';

var gulp = require('gulp'),
  config = require('../config'),
  rev = require('gulp-rev'),
  revNapkin = require('gulp-rev-napkin'),
  revCSS = require('gulp-rev-css-url');


gulp.task('revisioning', ['styles'], function () {
  return gulp.src(config.paths.revisioning, {base: config.paths.build})
    .pipe(rev())
    .pipe(revCSS())
    .pipe(gulp.dest(config.paths.build))
    .pipe(revNapkin({verbose: false}))
    .pipe(rev.manifest())
    .pipe(gulp.dest(config.paths.manifest));
});
