var gulp = require('gulp');


gulp.task('build', gulp.series('set-production', 'clean', 'styles', 'scripts', 'copyfiles', 'revisioning'));
