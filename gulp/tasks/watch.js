"use strict";

const { watch, series } = require("gulp");
const config = require("../config");

const clean = require("./clean");
const styles = require("./styles");
const scripts = require("./scripts");
const copyFiles = require("./copy");

const watchPaths = async () => {
  watch(config.paths.css.src, styles);
  watch(config.paths.js.src, scripts);
  watch(config.paths.copy.src, copyFiles);
};

/**
 * watches js and CSS for filesystem changes
 */
const watchTask = series(clean, styles, scripts, copyFiles, watchPaths);

module.exports = watchTask;
