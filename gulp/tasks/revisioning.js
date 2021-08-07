"use strict";

const { src, dest, series } = require("gulp");
const config = require("../config");
const rev = require("gulp-rev");
const revNapkin = require("gulp-rev-napkin");
const revCSS = require("gulp-rev-css-url");

const clean = require("./clean");
const styles = require("./styles");
const scripts = require("./scripts");

const revisioningTask = async () => {
  return src(config.paths.revisioning, { base: config.paths.build })
    .pipe(rev())
    .pipe(revCSS())
    .pipe(dest(config.paths.build))
    .pipe(revNapkin({ verbose: false }))
    .pipe(rev.manifest())
    .pipe(dest(config.paths.manifest));
};

module.exports = revisioningTask;
