"use strict";

const { series } = require("gulp");

const config = require("../config");

const clean = require("./clean");
const styles = require("./styles");
const scripts = require("./scripts");
const copyFiles = require("./copy");

/**
 * Perform a local build. Similar to production, but doesn't do asset revisioning and has a different path
 */
module.exports = series(clean, styles, scripts, copyFiles);
