"use strict";

const config = require("../config");
const del = require("del");

const cleanTask = async () => del(config.paths.build);

module.exports = cleanTask;
