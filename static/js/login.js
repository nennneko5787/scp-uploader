const localizationTable = {
  "login.failed": {
    ja: "ログインに失敗しました。",
    en: "Login failed.",
  },
};

/**
 * @param {string} authCode
 * @return {boolean}
 */
async function login(authCode) {
  const response = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ authCode: authCode }),
  });

  if (response.status !== 200) {
    return false;
  }
  return true;
}

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form");
  const notifications = document.getElementById("notifications");

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const authCode = form.elements["authCode"].value;
    const submitButton = form.elements["submit"];

    submitButton.classList.add("is-loading");
    submitButton.disabled = true;

    login(authCode, submitButton).then((result) => {
      submitButton.classList.remove("is-loading");
      submitButton.disabled = false;

      if (result == false) {
        notifications.innerHTML = `<div class="notification is-danger"><button class="delete"></button>${
          localizationTable["login.failed"][COOKIES.getCookie("localization", "ja")]
        }</div>`;
        (document.querySelectorAll(".notification .delete") || []).forEach(($delete) => {
          const $notification = $delete.parentNode;

          $delete.addEventListener("click", () => {
            $notification.parentNode.removeChild($notification);
          });
        });
        return;
      }

      window.location.href = "/";
    });
  });
});
