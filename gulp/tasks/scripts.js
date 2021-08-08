"use strict";

const { series, src, dest } = require("gulp");
const config = require("../config");
const environments = require("gulp-environments");
const uglify = require("gulp-uglify");

var development = environments.development;
var production = environments.production;

const scriptsTask = () => {
  const destination = production()
    ? config.paths.js.dest.production
    : config.paths.js.dest.development;

  return src(config.paths.js.src)
    .pipe(production(uglify()))
    .pipe(dest(destination));
};

module.exports = scriptsTask;
