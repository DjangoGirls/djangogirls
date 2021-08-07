const gulp = require("gulp");
const requireDir = require("require-dir");
const path = require("path");

const tasks = requireDir(path.join(__dirname, "./gulp/tasks"), {
  recurse: true,
});
module.exports = tasks;
