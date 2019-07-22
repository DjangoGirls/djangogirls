const gulp = require("gulp"),
  config = require("../config"),
  os = require("os"),
  spawn = require("child_process").spawn,
  chalk = require("chalk");

gulp.task("runserver", ["watch"], function() {
  // Compatibility across all platforms
  const pythonPath =
    (os.platform() === "win32" ? "/scripts/" : "/bin/") + "python";

  const runserver = spawn(
    process.env["VIRTUAL_ENV"] + pythonPath,
    ["manage.py", "runserver"],
    { stdio: "inherit" }
  ).on("error", function(error) {
    console.log(
      `${chalk.red(
        "Something went wrong."
      )} You probably haven't activated the virtual environment.`
    );
    process.exit();
  });

  runserver.on("close", function(code) {
    if (code !== 0) {
      console.error("Django runserver exited with error code: " + code);
    } else {
      console.log("Django runserver exited normally.");
    }
  });
});
