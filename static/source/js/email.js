document.addEventListener("DOMContentLoaded", () => {
  const addRsvpButtons = document.querySelectorAll(".rsvp-buttons button");
  const emailContent = document.querySelector("#id_text");

  addRsvpButtons.forEach((btn) =>
    btn.addEventListener("click", handleRsvpButtonClick),
  );

  emailContent.addEventListener("keyup", () => {
    updateEmailPreview(emailContent.value);
  });

  /**
   *
   * @param {Event} event
   */
  function handleRsvpButtonClick(event) {
    const button = event.currentTarget;

    const option = button.dataset.value;

    if (option === "yes" || option === "no") {
      const rsvp_link = `\n[rsvp-url-${option}]`;
      const content = emailContent.value;
      const newContent = `${content} ${rsvp_link}`;

      emailContent.value = newContent;
      updateEmailPreview(newContent);
    }
  }

  function updateEmailPreview(content) {
    content = content.replaceAll(
      "[rsvp-url-yes]",
      '<a href="">https://djangogirls.org/rsvp-YES-generated-url</a>',
    );
    content = content.replaceAll(
      "[rsvp-url-no]",
      '<a href="">https://djangogirls.org/rsvp-NO-generated-url</a>',
    );

    /* This preview is only used to show what the user themselves have currently
       written into the text box. It is thus safe to use innerHTML to
       insert user-created content. */
    document.querySelector("#preview").innerHTML = content;
  }
});
