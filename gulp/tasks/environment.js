"use strict";

const environments = require("gulp-environments");
const gutil = require("gulp-util");

const production = environments.production;

// was set-production
const setProduction = async () => {
  gutil.log("Setting environment to production");
  environments.current(production);
};

module.exports = setProduction;
