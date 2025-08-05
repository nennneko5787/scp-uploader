let prevBtn;
let nextBtn;
let currentPage = 1;

document.addEventListener("DOMContentLoaded", async () => {
  const sectionMap = {
    new: document.getElementById("new"),
  };

  prevBtn = document.querySelector(".pagination-previous");
  nextBtn = document.querySelector(".pagination-next");

  const type = "new";
  const container = sectionMap[type];

  await loadFiles(type, container, currentPage);

  prevBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    if (currentPage > 1) {
      currentPage--;
      await loadFiles(type, container);
    }
  });

  nextBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    currentPage++;
    await loadFiles(type, container);
  });

  async function loadFiles(type, container) {
    container.innerHTML = `<div class="spinner"></div>`;

    const response = await fetch(`/api/files?page=${currentPage}&type=${type}`);
    const files = await response.json();

    container.innerHTML = "";

    files.forEach((file) => {
      const element = createFileElement(file, type);
      container.append(element);
    });

    prevBtn.disabled = currentPage <= 1;
    nextBtn.disabled = files.length === 0;
  }
});

function createFileElement(file, type) {
  const element = document.createElement("a");
  element.classList.add("column", "box");

  element.classList.add("is-half");

  element.href = `/files/${file.id}`;

  const titleElement = document.createElement("h3");
  titleElement.classList.add("file-title");
  titleElement.textContent = file.name;

  element.append(titleElement);

  const detailElement = document.createElement("div");
  detailElement.classList.add("flex");

  const viewsElement = createIconText("fa-eye", file.views);
  const downloadsElement = createIconText("fa-download", file.downloads);

  detailElement.append(viewsElement, downloadsElement);
  element.append(detailElement);

  const authorElement = document.createElement("div");
  authorElement.classList.add("is-right");

  const userIcon = document.createElement("i");
  userIcon.classList.add("fa-solid", "fa-user");

  const nameCode = document.createElement("code");
  nameCode.textContent = `${file.author.name}#${file.author.handle}`;

  authorElement.append(userIcon, nameCode);
  element.append(authorElement);

  const tagsElement = document.createElement("div");
  tagsElement.classList.add("tags");

  file.tags.forEach((tag) => {
    const tagDiv = document.createElement("div");
    tagDiv.classList.add("tag", "is-primary");
    tagDiv.textContent = tag;
    tagsElement.append(tagDiv);
  });

  element.append(tagsElement);

  return element;
}

function createIconText(iconClass, text) {
  const container = document.createElement("div");

  const icon = document.createElement("i");
  icon.classList.add("fa-solid", iconClass);

  const span = document.createElement("span");
  span.textContent = ` ${text}`;

  container.append(icon, span);
  return container;
}
