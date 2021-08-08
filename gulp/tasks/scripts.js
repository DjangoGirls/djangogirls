"use strict";

const { src, dest } = require("gulp");
const { production } = require("gulp-environments");
const uglify = require("gulp-uglify");

const config = require("../config");

/**
 * uses uglify to minify distributed JS
 * skipped for local builds
 */
const scriptsTask = () => {
  const destination = production()
    ? config.paths.js.dest.production
    : config.paths.js.dest.development;

  return (
    src(config.paths.js.src)
      // passing uglify into the production function means uglify only runs during produciton builds
      .pipe(production(uglify()))
      .pipe(dest(destination))
  );
};

module.exports = scriptsTask;
