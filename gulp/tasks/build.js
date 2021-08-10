"use strict";

const { series } = require("gulp");

const setProduction = require("./environment");
const local = require("./local");
const revisioning = require("./revisioning");

/**
 * A production build is a local build with a different environment and revision control enabled
 */
const buildTask = series(setProduction, local, revisioning);

module.exports = buildTask;
