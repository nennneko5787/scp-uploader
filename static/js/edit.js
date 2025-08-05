const localizationTable = {
  "tag.duplication": {
    ja: "タグを重複して設定することはできません。",
    en: "You cannot set duplicate tags.",
  },
  "form.draft": {
    ja: "フォームが書きかけです！見落としているところがないか確認してください。",
    en: "The form is incomplete! Please check to make sure you haven't missed anything.",
  },
};

const tags = [];

function addTag(tagString) {
  const tagsElement = document.getElementById("tags");

  if (tags.includes(tagString)) {
    alert(localizationTable["tag.duplication"][COOKIES.getCookie("localization", "ja")]);
    return;
  }
  tags.push(tagString);

  const tagElement = document.createElement("span");
  tagElement.className = "tag is-link";
  tagElement.textContent = tagString;

  const deleteButton = document.createElement("button");
  deleteButton.className = "delete is-small";
  deleteButton.addEventListener("click", () => {
    deleteButton.parentElement.remove();
    tags = tags.filter(function (e) {
      return e !== tagString;
    });
  });

  tagElement.append(deleteButton);
  tagsElement.append(tagElement);
}

document.addEventListener("DOMContentLoaded", () => {
  const tagInput = document.getElementById("tag");
  const submitTagButton = document.getElementById("submit-tag");

  const nameInput = document.getElementById("name");
  const descriptionInput = document.getElementById("description");
  const publicCheckbox = document.getElementById("public");
  const submitButton = document.getElementById("submit");

  const deleteButton = document.getElementById("delete");

  tagInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      if (tagInput.value == "") return;
      const tagString = tagInput.value;
      tagInput.value = "";
      addTag(tagString);
    }
    return false;
  });

  submitTagButton.addEventListener("click", () => {
    if (tagInput.value == "") return;
    const tagString = tagInput.value;
    tagInput.value = "";
    addTag(tagString);
  });

  deleteButton.addEventListener("click", async () => {
    deleteButton.classList.add("is-loading");
    deleteButton.disabled = true;

    if (!confirm("ファイルを削除すると、サーバーからファイルのデータが削除されます。\nよろしいですか？")) {
      deleteButton.classList.remove("is-loading");
      deleteButton.disabled = false;

      return;
    }

    const response = await fetch(`/api/files/${fileId}`, {
      method: "DELETE",
      headers: { "content-type": "application/json" },
    });
    const jsonData = await response.json();

    deleteButton.classList.remove("is-loading");
    deleteButton.disabled = false;

    if (response.status != 200) {
      notifications.innerHTML = `<div class="notification is-danger"><button class="delete"></button>${jsonData.detail}</div>`;
      (document.querySelectorAll(".notification .delete") || []).forEach(($delete) => {
        const $notification = $delete.parentNode;

        $delete.addEventListener("click", () => {
          $notification.parentNode.removeChild($notification);
        });
      });
      return;
    }

    notifications.innerHTML = `<div class="notification is-success"><button class="delete"></button>削除しました。</div>`;
    (document.querySelectorAll(".notification .delete") || []).forEach(($delete) => {
      const $notification = $delete.parentNode;

      $delete.addEventListener("click", () => {
        $notification.parentNode.removeChild($notification);
      });
    });

    setTimeout(() => {
      window.location.href = "/";
    }, 3000);
  });

  submitButton.addEventListener("click", async () => {
    submitButton.classList.add("is-loading");
    submitButton.disabled = true;

    if (nameInput.value == "" || descriptionInput == "") {
      alert(localizationTable["form.draft"][COOKIES.getCookie("localization", "ja")]);
    }

    const response = await fetch(`/api/files/${fileId}/edit`, {
      method: "PATCH",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        name: nameInput.value,
        description: descriptionInput.value,
        tags: tags,
        public: publicCheckbox.checked,
      }),
    });
    const jsonData = await response.json();

    submitButton.classList.remove("is-loading");
    submitButton.disabled = false;

    if (response.status != 200) {
      notifications.innerHTML = `<div class="notification is-danger"><button class="delete"></button>${jsonData.detail}</div>`;
      (document.querySelectorAll(".notification .delete") || []).forEach(($delete) => {
        const $notification = $delete.parentNode;

        $delete.addEventListener("click", () => {
          $notification.parentNode.removeChild($notification);
        });
      });
      return;
    }

    notifications.innerHTML = `<div class="notification is-success"><button class="delete"></button>編集しました。</div>`;
    (document.querySelectorAll(".notification .delete") || []).forEach(($delete) => {
      const $notification = $delete.parentNode;

      $delete.addEventListener("click", () => {
        $notification.parentNode.removeChild($notification);
      });
    });
  });
});
