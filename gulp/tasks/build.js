var gulp = require('gulp');


gulp.task('build', ['set-production', 'clean', 'styles', 'revisioning']);
