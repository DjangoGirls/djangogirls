var gulp = require('gulp');


gulp.task('build', ['set-production', 'clean', 'styles', 'scripts', 'copyfiles', 'revisioning']);
