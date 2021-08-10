"use strict";

const { production, current } = require("gulp-environments");
const log = require("fancy-log");

/**
 * Sets a global production marker that other tasks can read
 */
const setProductionTask = async () => {
  log("Setting environment to production");
  current(production);
};

module.exports = setProductionTask;
