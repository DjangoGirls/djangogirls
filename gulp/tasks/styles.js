"use strict";

const { src, dest, series } = require("gulp");
const stylus = require("gulp-stylus");
const { production } = require("gulp-environments");
const concat = require("gulp-concat");

const config = require("../config");

const stylusTask = () => {
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

for (const key in config.paths.css.bundles) {
  const func = () => {
    const destination = production()
      ? config.paths.css.dest.production
      : config.paths.css.dest.development;

    return src(config.paths.css.bundles[key])
      .pipe(concat(`${key}.css`))
      .pipe(dest(destination));
  };
  // give the dynamic task a custom name for debugging
  Object.defineProperty(func, "name", {
    value: `styles:${key}`,
    writable: false,
  });

  tasks.push(func);
}

/**
 * compiles CSS using stylus
 */
module.exports = series(...tasks);
