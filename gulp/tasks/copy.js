"use strict";

const { task, series, src, dest } = require("gulp");
const config = require("../config");
const environments = require("gulp-environments");

const production = environments.production;

// was called copyfiles
const copyFiles = () => {
  const destination = production()
    ? config.paths.copy.dest.production
    : config.paths.copy.dest.development;
  return src(config.paths.copy.src).pipe(dest(destination));
};

module.exports = copyFiles;
