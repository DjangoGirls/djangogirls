document.addEventListener("DOMContentLoaded", () => {
  const selectAllCheckbox = document.querySelector("#select-all-box");
  const applicationCheckboxes = Object.values(
    document.querySelectorAll(".application-box"),
  );
  const selectedCount = document.querySelector("#selected-count");
  const applicationStatusSelects = document.querySelectorAll(
    "select.state-change",
  );
  const applicationRsvpSelects =
    document.querySelectorAll("select.rsvp-change");

  const applicationChangeStateForm = document.querySelector(
    "form#change-state-form",
  );

  function updateSelectedCount() {
    selectedCount.textContent = document.querySelectorAll(
      ".application-box:checked",
    ).length;
  }

  function handleApplicationStatusChange(event) {
    event.preventDefault();
    const select = event.currentTarget;
    const appId = select.dataset.appId;
    const state = select.value;
    const url = document.querySelector("#applications").dataset.changeStateUrl;

    const formData = new FormData();
    formData.append("state", state);
    formData.append("application", appId);

    fetch(url, {
      method: "POST",
      body: formData,
    });

    updateApplicationStateClasses(appId, state);

    return false;
  }

  /**
   *
   * @param {Event} event
   */
  function handleApplicationRsvpChange(event) {
    event.preventDefault();
    const select = event.currentTarget;
    const appId = select.dataset.appId;
    const rsvpStatus = select.value;
    const url = document.querySelector("#applications").dataset.changeRsvpUrl;

    const formData = new FormData();
    formData.append("rsvp_status", rsvpStatus);
    formData.append("application", appId);

    fetch(url, {
      method: "POST",
      body: formData,
    });

    updateApplicationRSVPClasses(appId, rsvpStatus);
    return false;
  }

  /**
   * Update all selected applications to selected state
   * at once.
   *
   * @param {Event} event Submit event
   */
  function handleFormSubmit(event) {
    event.preventDefault();

    const form = event.currentTarget;

    const url = form.action;
    const state = form.querySelector("select").value;

    const selectedApplications = document.querySelectorAll(
      ".application-box:checked",
    );

    const selectedIds = Object.values(selectedApplications).map(
      (application) => application.value,
    );

    const formData = new FormData();
    formData.append("state", state);
    formData.append("application", selectedIds);

    fetch(url, {
      method: "POST",
      body: formData,
    });

    applicationCheckboxes.forEach((checkbox) => (checkbox.checked = false));

    selectedIds.forEach((appId) => {
      const application = document.querySelector(
        `select#application-${appId}-state`,
      );
      application.value = state;
      updateApplicationStateClasses(appId, state);
    });

    return false;
  }
  /**
   * Clears all previous state based classes and adds the new state class
   * to the select of application's state
   *
   * @param {string} appId Application ID
   * @param {string} newState state of application
   */
  function updateApplicationStateClasses(appId, newState) {
    const application = document.querySelector(
      `select#application-${appId}-state`,
    );
    application.classList.remove(
      "submitted",
      "accepted",
      "rejected",
      "default",
      "waitlisted",
    );
    application.classList.add(newState);
  }

  /**
   * Clears all previous RSVP based classes and adds the new RSVP class
   * to the select of application's RSVP
   *
   * @param {string} appId Application ID
   * @param {string} newState state of application
   */
  function updateApplicationRSVPClasses(appId, newRSVP) {
    const application = document.querySelector(
      `select#application-${appId}-rsvp-status`,
    );
    application.classList.remove("yes", "no", "waiting");
    application.classList.add(newRSVP);
  }

  selectAllCheckbox.addEventListener("change", (event) => {
    applicationCheckboxes.forEach(
      (application) => (application.checked = event.target.checked),
    );

    updateSelectedCount();
  });

  /* Listen to checkbox changes for application rows */
  applicationCheckboxes.forEach((application) => {
    application.addEventListener("change", (event) => updateSelectedCount());
  });

  /* Listen to select changes for application's status */
  applicationStatusSelects.forEach((select) => {
    select.addEventListener("change", handleApplicationStatusChange);
  });

  /* Listen to select changes for application's RSVP */
  applicationRsvpSelects.forEach((select) => {
    select.addEventListener("change", handleApplicationRsvpChange);
  });

  applicationChangeStateForm.addEventListener("submit", handleFormSubmit);
});
