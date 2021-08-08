"use strict";

const { src, dest, series } = require("gulp");
const rev = require("gulp-rev");
const revNapkin = require("gulp-rev-napkin");
const revCSS = require("gulp-rev-css-url");

const config = require("../config");

/**
 * uses gulp-rev to "append content hash to filenames: `unicorn.css` → `unicorn-d41d8cd98f.css`"
 * Clues the browser into the fact that a static asset has changed
 */
const revisioningTask = () => {
  return src(config.paths.revisioning, {
    // this is a production-only task; otherwise use gulp-environments to get the correct path
    base: config.paths.copy.dest.production,
  })
    .pipe(rev())
    .pipe(revCSS())
    .pipe(dest(config.paths.copy.dest.production))
    .pipe(revNapkin({ verbose: false }))
    .pipe(rev.manifest())
    .pipe(dest(config.paths.manifest));
};

module.exports = revisioningTask;
