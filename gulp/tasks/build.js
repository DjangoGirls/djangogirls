"use strict";

const { series } = require("gulp");

const setProduction = require("./environment");
const clean = require("./clean");
const styles = require("./styles");
const scripts = require("./scripts");
const copyFiles = require("./copy");
const revisioning = require("./revisioning");

const buildTask = series(
  setProduction,
  clean,
  styles,
  scripts,
  copyFiles,
  revisioning
);

module.exports = buildTask;
