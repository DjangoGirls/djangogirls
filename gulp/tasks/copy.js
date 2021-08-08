"use strict";

const { task, series, src, dest } = require("gulp");
const { production } = require("gulp-environments");

const config = require("../config");

/**
 * copies generated files to their final place (depending on environment)
 */
const copyFilesTask = () => {
  const destination = production()
    ? config.paths.copy.dest.production
    : config.paths.copy.dest.development;
  return src(config.paths.copy.src).pipe(dest(destination));
};

module.exports = copyFilesTask;
