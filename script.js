"use strict";

const sitePrefix = document.body.dataset.prefix || "./";
const sidebar = document.querySelector("#sidebar");
const menuToggle = document.querySelector("#menu-toggle");
const backdrop = document.querySelector("#menu-backdrop");
const mobileQuery = window.matchMedia("(max-width: 767px)");
let previousMenuFocus = null;

function setMenu(open, restoreFocus = true) {
  const isOpen = open && mobileQuery.matches;
  if (isOpen) previousMenuFocus = document.activeElement;
  document.body.classList.toggle("menu-open", isOpen);
  menuToggle.setAttribute("aria-expanded", String(isOpen));
  menuToggle.setAttribute("aria-label", isOpen ? "전체 메뉴 닫기" : "전체 메뉴 열기");
  backdrop.hidden = !isOpen;
  sidebar.inert = mobileQuery.matches && !isOpen;
  document.querySelector(".workspace").inert = isOpen;
  document.querySelector(".bottom-nav").inert = isOpen;
  if (isOpen) window.requestAnimationFrame(() => {
    if (document.body.classList.contains("menu-open")) sidebar.querySelector(".drawer-close").focus({ preventScroll: true });
  });
  else if (restoreFocus && previousMenuFocus?.isConnected) previousMenuFocus.focus();
}

menuToggle.addEventListener("click", () => setMenu(!document.body.classList.contains("menu-open")));
backdrop.addEventListener("click", () => setMenu(false));
document.querySelector(".drawer-close").addEventListener("click", () => setMenu(false));
mobileQuery.addEventListener("change", () => setMenu(false, false));
setMenu(false, false);
document.addEventListener("keydown", event => {
  if (!document.body.classList.contains("menu-open")) return;
  if (event.key === "Escape") { event.preventDefault(); setMenu(false); }
  if (event.key === "Tab") {
    const targets = [...sidebar.querySelectorAll("a[href], button")];
    const first = targets[0], last = targets.at(-1);
    if (event.shiftKey && (document.activeElement === first || !sidebar.contains(document.activeElement))) {
      event.preventDefault(); last.focus();
    } else if (!event.shiftKey && (document.activeElement === last || !sidebar.contains(document.activeElement))) {
      event.preventDefault(); first.focus();
    }
  }
});

const searchInput = document.querySelector("#search-input");
const postCards = [...document.querySelectorAll("[data-post]")];
const filterButtons = [...document.querySelectorAll("[data-filter]")];
const filterField = document.querySelector(".filter-strip")?.dataset.filterField || "section";
let activeFilter = "all";
function filterPosts() {
  const query = (searchInput?.value || "").trim().toLocaleLowerCase("ko");
  let count = 0;
  postCards.forEach(card => {
    const matches = (activeFilter === "all" || card.dataset[filterField] === activeFilter) && card.dataset.search.toLocaleLowerCase("ko").includes(query);
    card.hidden = !matches;
    if (matches) count += 1;
  });
  const counter = document.querySelector("#post-count");
  if (counter) counter.textContent = count;
  const empty = document.querySelector("#search-empty");
  if (empty) empty.hidden = count > 0 || (postCards.length === 0 && !query && activeFilter === "all");
  const library = document.querySelector(".empty-library");
  if (library) library.hidden = Boolean(query);
  const status = document.querySelector("#search-status");
  if (status) status.textContent = `${count}개의 기록을 찾았습니다.`;
}
searchInput?.addEventListener("input", filterPosts);
filterButtons.forEach(button => button.addEventListener("click", () => {
  activeFilter = button.dataset.filter;
  filterButtons.forEach(item => {
    const selected = item === button;
    item.classList.toggle("is-active", selected);
    item.setAttribute("aria-pressed", String(selected));
  });
  filterPosts();
}));

const interactionStatus = document.querySelector("#interaction-status");
document.querySelectorAll("[data-copy-target]").forEach(button => {
  button.addEventListener("click", async () => {
    const code = document.getElementById(button.dataset.copyTarget);
    if (!code) return;
    const label = button.querySelector("span");
    const originalLabel = label.textContent;
    try {
      await navigator.clipboard.writeText(code.textContent);
      label.textContent = originalLabel === "COPY" ? "COPIED!" : originalLabel === "[copy]" ? "[copied]" : "Copied";
      interactionStatus.textContent = "코드를 복사했습니다.";
      window.setTimeout(() => { label.textContent = originalLabel; }, 1600);
    } catch {
      label.textContent = "Select";
      const range = document.createRange();
      range.selectNodeContents(code);
      const selection = window.getSelection();
      selection.removeAllRanges(); selection.addRange(range);
      interactionStatus.textContent = "코드를 선택했습니다. 복사 단축키를 사용해 주세요.";
    }
  });
});

const cliForm = document.querySelector("#cli-form");
if (cliForm) {
  const input = document.querySelector("#cli-input");
  const output = document.querySelector("#cli-output");
  const dynamicOutput = document.querySelector("#cli-dynamic-output") || output;
  const inputDisplay = document.querySelector("#terminal-input-display");
  const commands = [];
  let historyIndex = 0;
  function textNode(tag, className, text) {
    const node = document.createElement(tag); node.className = className; node.textContent = text; return node;
  }
  const destinations = {
    all_logs: ["posts.html", "모든 기록 열기"],
    posts: ["posts.html", "모든 기록 열기"],
    projects: ["projects.html", "프로젝트"],
    dev_notes: ["development.html", "개발 노트 열기"],
    papers_ai: ["papers-ai.html", "인공지능 논문"],
    papers_security: ["papers-security.html", "정보보안 논문"],
    issues: ["issues.html", "이슈"],
    vulnerabilities: ["vulnerabilities.html", "취약점"]
  };
  function addLink(parent, route, title) {
    const link = textNode("a", "cli-output-link", `${title} ↗`);
    link.href = sitePrefix + route; parent.append(link);
  }
  function runCommand(raw) {
    const value = raw.trim();
    if (!value) { input.focus(); return; }
    const command = value.toLowerCase();
    commands.push(value); historyIndex = commands.length;
    if (command === "clear") {
      dynamicOutput.replaceChildren();
    } else {
      const entry = textNode("div", "cli-entry", "");
      entry.append(textNode("p", "command", `$ ${value}`));
      if (command === "help") {
        entry.append(textNode("p", "cli-answer", "help      Show commands\nwhoami    Profile\nposts     All logs\nprojects  Projects\nskills    Tech stack\nclear     Clear command output"));
      } else if (command === "whoami") {
        entry.append(textNode("p", "cli-answer", "uhbyeon — 배우고, 만들고, 기록합니다."));
      } else if (["about", "cat profile.json"].includes(command)) {
        entry.append(textNode("p", "cli-answer", "uhbyeon's log_\n인공지능·정보보안 논문과 이슈, 취약점, 개발 과정에서 배운 것을 기록합니다."));
      } else if (["topics", "ls ./topics"].includes(command)) {
        ["papers_ai", "papers_security", "issues", "vulnerabilities", "dev_notes"].forEach(key => addLink(entry, ...destinations[key]));
      } else if (["skills", "tech-stack --visual"].includes(command)) {
        entry.append(textNode("p", "cli-answer", document.querySelector(".tech-stack-panel")?.textContent.trim() || "0 loaded"));
      } else if (command === "contact --links") {
        entry.append(textNode("p", "cli-answer", document.querySelector(".contact-tree")?.textContent.trim() || "—"));
      } else if (destinations[command]) {
        addLink(entry, ...destinations[command]);
      } else {
        entry.append(textNode("p", "cli-answer", `알 수 없는 명령: ${value}\nhelp로 사용 가능한 명령을 확인해 주세요.`));
      }
      dynamicOutput.append(entry);
    }
    output.scrollTop = output.scrollHeight;
    input.value = ""; input.focus();
    if (inputDisplay) inputDisplay.textContent = "";
  }
  cliForm.addEventListener("submit", event => { event.preventDefault(); runCommand(input.value); });
  document.querySelectorAll("[data-command]").forEach(button => button.addEventListener("click", () => runCommand(button.dataset.command)));
  input.addEventListener("keydown", event => {
    if (event.key === "ArrowUp") { event.preventDefault(); historyIndex = Math.max(0, historyIndex - 1); input.value = commands[historyIndex] || ""; }
    if (event.key === "ArrowDown") { event.preventDefault(); historyIndex = Math.min(commands.length, historyIndex + 1); input.value = commands[historyIndex] || ""; }
  });
  input.addEventListener("input", () => { if (inputDisplay) inputDisplay.textContent = input.value; });
}

document.querySelectorAll("[data-bookmark]").forEach(button => {
  const key = `uhbyeon:bookmark:${location.pathname}`;
  try { button.setAttribute("aria-pressed", String(localStorage.getItem(key) === "true")); } catch { /* Browser-local preference is optional. */ }
  button.addEventListener("click", () => {
    const saved = button.getAttribute("aria-pressed") !== "true";
    button.setAttribute("aria-pressed", String(saved));
    try { localStorage.setItem(key, String(saved)); } catch { /* Keep the current-page state. */ }
    interactionStatus.textContent = saved ? "북마크에 저장했습니다." : "북마크를 해제했습니다.";
  });
});
document.querySelectorAll("[data-share]").forEach(button => {
  button.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(location.href);
      interactionStatus.textContent = "게시글 링크를 복사했습니다.";
    } catch { interactionStatus.textContent = "주소 표시줄의 게시글 주소를 복사해 주세요."; }
  });
});
