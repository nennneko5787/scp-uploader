let viewsPrevBtn, viewsNextBtn;
let downloadsPrevBtn, downloadsNextBtn;

let viewsPage = 1;
let downloadsPage = 1;

document.addEventListener("DOMContentLoaded", async () => {
  const viewsContainer = document.getElementById("views");
  const downloadsContainer = document.getElementById("downloads");

  viewsPrevBtn = document.querySelector(".views-pagination-previous");
  viewsNextBtn = document.querySelector(".views-pagination-next");
  downloadsPrevBtn = document.querySelector(".downloads-pagination-previous");
  downloadsNextBtn = document.querySelector(".downloads-pagination-next");

  await loadFiles("views", viewsContainer, viewsPage);
  await loadFiles("downloads", downloadsContainer, downloadsPage);

  viewsPrevBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    if (viewsPage > 1) {
      viewsPage--;
      await loadFiles("views", viewsContainer, viewsPage);
    }
  });

  viewsNextBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    viewsPage++;
    await loadFiles("views", viewsContainer, viewsPage);
  });

  downloadsPrevBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    if (downloadsPage > 1) {
      downloadsPage--;
      await loadFiles("downloads", downloadsContainer, downloadsPage);
    }
  });

  downloadsNextBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    downloadsPage++;
    await loadFiles("downloads", downloadsContainer, downloadsPage);
  });
});

async function loadFiles(type, container, page) {
  container.innerHTML = `<div class="spinner"></div>`;

  const response = await fetch(`/api/files?page=${page}&type=${type}`);
  const files = await response.json();

  container.innerHTML = "";

  files.forEach((file) => {
    const element = createFileElement(file, type);
    container.append(element);
  });

  const prevBtn = type === "views" ? viewsPrevBtn : downloadsPrevBtn;
  const nextBtn = type === "views" ? viewsNextBtn : downloadsNextBtn;

  prevBtn.disabled = page <= 1;
  nextBtn.disabled = files.length === 0;
}

function createFileElement(file, type) {
  const element = document.createElement("a");
  element.classList.add("column", "box", "is-half");
  element.href = `/files/${file.id}`;

  const titleElement = document.createElement("h3");
  titleElement.classList.add("file-title");
  titleElement.textContent = file.name;
  element.append(titleElement);

  const detailElement = document.createElement("div");
  detailElement.classList.add("flex");
  detailElement.append(createIconText("fa-eye", file.views), createIconText("fa-download", file.downloads));
  element.append(detailElement);

  const authorElement = document.createElement("div");
  authorElement.classList.add("is-right");
  authorElement.append(
    Object.assign(document.createElement("i"), { className: "fa-solid fa-user" }),
    Object.assign(document.createElement("code"), { textContent: `${file.author.name}#${file.author.handle}` })
  );
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
