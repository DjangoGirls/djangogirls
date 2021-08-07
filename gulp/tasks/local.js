"use strict";

const { series } = require("gulp");
const config = require("../config");

const clean = require("./clean");
const styles = require("./styles");
const scripts = require("./scripts");
const copyFiles = require("./copy");

module.exports = series(clean, styles, scripts, copyFiles);
