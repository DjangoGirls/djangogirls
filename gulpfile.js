const build = require("./gulp/tasks/build");
const watch = require("./gulp/tasks/watch");
const local = require("./gulp/tasks/local");
const clean = require("./gulp/tasks/clean");

module.exports = {
  build,
  watch,
  local,
  clean,
  default: watch,
};
