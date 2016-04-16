var requireDir = require('require-dir'),
  gulp = require('gulp');


requireDir('./gulp/tasks', { recurse: true });

gulp.task('default', ['watch']);
