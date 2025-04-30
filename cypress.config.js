const { defineConfig } = require("cypress");
const { exec } = require("child_process");

module.exports = defineConfig({
  e2e: {
    baseUrl: "http://127.0.0.1:8000",
    viewportWidth: 1920,
    viewportHeight: 1080,
    watchForFileChanges: false,
    pageLoadTimeout: 120000,
    setupNodeEvents(on, config) {
      on("task", {
        resetDb() {
          return new Promise((resolve, reject) => {
            exec("rm -f db.sqlite3", (err, stdout, stderr) => {
              if (err) return reject(err);
              resolve(stdout || stderr);
            });
          });
        },
      });
    },
  },
});
