"use strict";

const del = require("del");

const config = require("../config");

/**
 * removes the files created during local and production builds
 */
const cleanTask = async () => {
  await del(config.paths.copy.dest.development);
  await del(config.paths.copy.dest.production);
  await del(config.paths.temp);
};

module.exports = cleanTask;
