"use strict";

const { src, dest, series, task } = require("gulp");
const gutil = require("gulp-util");
const stylus = require("gulp-stylus");
const environments = require("gulp-environments");
const concat = require("gulp-concat");

const config = require("../config");

const production = environments.production;

const stylusTask = async () => {
  const compress = production();
  return src(config.paths.css.src)
    .pipe(
      stylus({
        compress,
      })
    )
    .pipe(dest(config.paths.temp));
};

const tasks = [stylusTask];

for (let key in config.paths.css.bundles) {
  const taskName = `styles:${key}`;
  // use deprecated gulp.task to get good dynamic task names
  task(taskName, async () => {
    const destination = production()
      ? config.paths.css.dest.production
      : config.paths.css.dest.development;

    return src(config.paths.css.bundles[key])
      .pipe(concat(`${key}.css`))
      .pipe(dest(destination));
  });
  tasks.push(taskName);
}

module.exports = series(...tasks);
