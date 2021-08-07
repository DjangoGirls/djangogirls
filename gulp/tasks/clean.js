"use strict";

const { task, src } = require("gulp");
const config = require("../config");
// TODO: gulp-clean is deprecated
const clean = require("gulp-clean");

const cleanTask = async () => {
  return src(config.paths.build, { read: false, allowEmpty: true }).pipe(
    clean({ force: true })
  );
};

module.exports = cleanTask;
