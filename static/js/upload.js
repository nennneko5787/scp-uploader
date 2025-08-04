const localizationTable = {
  "tag.duplication": {
    ja: "タグを重複して設定することはできません。",
    en: "You cannot set duplicate tags.",
  },
  "file.notSelected": {
    ja: "ファイルが選択されていません",
    en: "No file selected",
  },
  "file.label": {
    ja: "ファイルを選択",
    en: "Select file",
  },
  "form.draft": {
    ja: "フォームが書きかけです！見落としているところがないか確認してください。",
    en: "The form is incomplete! Please check to make sure you haven't missed anything.",
  },
  "file.sizeOver": {
    ja: "ファイルのサイズは20MBを超えてはいけません！",
    en: "The file size must not exceed 20MB!",
  },
  "file.mustBeSCP": {
    ja: "アップロードするファイルの拡張子は.scpである必要があります。",
    en: "The file extension of the uploaded file must be .scp.",
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
  const submitButton = document.getElementById("submit");

  const fileInput = document.querySelector("#fileElement input[type=file]");
  const fileName = document.querySelector("#fileElement .file-name");
  const fileLabel = document.querySelector("#fileElement span.file-label");

  fileName.textContent = localizationTable["file.notSelected"][COOKIES.getCookie("localization", "ja")];
  fileLabel.textContent = localizationTable["file.label"][COOKIES.getCookie("localization", "ja")];

  fileInput.onchange = () => {
    if (fileInput.files.length > 0) {
      fileName.textContent = fileInput.files[0].name;
    }
  };

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

  submitButton.addEventListener("click", async () => {
    submitButton.classList.add("is-loading");
    submitButton.disabled = true;

    if (nameInput.value == "" || descriptionInput == "" || fileInput.files.length <= 0) {
      alert(localizationTable["form.draft"][COOKIES.getCookie("localization", "ja")]);
    }

    const sizeInMB = fileInput.files[0] / (1024 * 1024);
    if (sizeInMB > 20) {
      alert(localizationTable["file.sizeOver"][COOKIES.getCookie("localization", "ja")]);
    }

    if (!fileInput.files[0].name.endsWith(".scp")) {
      alert(localizationTable["file.mustBeSCP"][COOKIES.getCookie("localization", "ja")]);
    }

    const formData = new FormData();
    formData.append("name", nameInput.value);
    formData.append("description", descriptionInput.value);
    formData.append("tags", JSON.stringify(tags));
    formData.append("file", fileInput.files[0]);

    const response = await fetch("/api/upload", { method: "POST", body: formData });
    const jsonData = await response.json();

    submitButton.classList.remove("is-loading");
    submitButton.disabled = false;

    if (response.status != 201) {
      notifications.innerHTML = `<div class="notification is-danger"><button class="delete"></button>${jsonData.detail}</div>`;
      (document.querySelectorAll(".notification .delete") || []).forEach(($delete) => {
        const $notification = $delete.parentNode;

        $delete.addEventListener("click", () => {
          $notification.parentNode.removeChild($notification);
        });
      });
      return;
    }

    window.location.href = `/files/${jsonData.id}`;
  });
});
