(() => {
  "use strict";

  const slides = [...document.querySelectorAll(".slide")];
  const stage = document.getElementById("stage");
  const viewport = document.getElementById("viewport");
  const progress = document.querySelector(".progress > div");
  const notice = document.querySelector(".jump-notice");
  const backupIndex = slides.findIndex((slide) => slide.dataset.section === "backup");
  let index = 0;
  let noticeTimer;

  const fragments = (slide) => [...slide.querySelectorAll(".fragment")];

  function clamp(value, min, max) {
    return Math.max(min, Math.min(value, max));
  }

  function scaleStage() {
    if (document.body.classList.contains("overview")) return;
    const scale = Math.min(window.innerWidth / 1600, window.innerHeight / 900);
    stage.style.transform = `translate(-50%, -50%) scale(${scale})`;
  }

  function announce(message) {
    notice.textContent = message;
    notice.classList.add("show");
    clearTimeout(noticeTimer);
    noticeTimer = setTimeout(() => notice.classList.remove("show"), 1300);
  }

  function syncHash() {
    history.replaceState(null, "", `#${slides[index].id}`);
  }

  function show(next, options = {}) {
    index = clamp(next, 0, slides.length - 1);
    slides.forEach((slide, slideIndex) => {
      const active = slideIndex === index;
      slide.classList.toggle("active", active);
      slide.setAttribute("aria-hidden", String(!active));
    });
    if (!options.preserveFragments) {
      fragments(slides[index]).forEach((fragment) => fragment.classList.remove("visible"));
    }
    progress.style.width = `${((index + 1) / slides.length) * 100}%`;
    syncHash();
    document.title = `${slides[index].dataset.title || "Win2APK"} | Win2APK`;
  }

  function next() {
    const hidden = fragments(slides[index]).find((fragment) => !fragment.classList.contains("visible"));
    if (hidden) {
      hidden.classList.add("visible");
      return;
    }
    show(index + 1);
  }

  function previous() {
    const visible = fragments(slides[index]).filter((fragment) => fragment.classList.contains("visible"));
    if (visible.length) {
      visible.at(-1).classList.remove("visible");
      return;
    }
    show(index - 1);
  }

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen?.();
    } else {
      document.exitFullscreen?.();
    }
  }

  function toggleOverview() {
    document.body.classList.toggle("overview");
    scaleStage();
  }

  function toggleVideo() {
    const video = slides[index].querySelector("video");
    if (!video) return;
    if (video.paused) video.play(); else video.pause();
  }

  function fromHash() {
    const target = document.getElementById(location.hash.slice(1));
    const found = slides.indexOf(target);
    return found >= 0 ? found : 0;
  }

  document.addEventListener("keydown", (event) => {
    if (["INPUT", "TEXTAREA", "SELECT"].includes(document.activeElement?.tagName)) return;
    if (["ArrowRight", "PageDown", " ", "Enter"].includes(event.key)) { event.preventDefault(); next(); }
    if (["ArrowLeft", "PageUp", "Backspace"].includes(event.key)) { event.preventDefault(); previous(); }
    if (event.key === "Home") { event.preventDefault(); show(0); }
    if (event.key === "End") { event.preventDefault(); show(slides.length - 1); }
    if (event.key.toLowerCase() === "b" && backupIndex >= 0) { show(backupIndex); announce("Backup / preguntas"); }
    if (event.key.toLowerCase() === "f") toggleFullscreen();
    if (event.key.toLowerCase() === "o") toggleOverview();
    if (event.key.toLowerCase() === "v") toggleVideo();
  });

  document.getElementById("next")?.addEventListener("click", next);
  document.getElementById("previous")?.addEventListener("click", previous);
  document.getElementById("fullscreen")?.addEventListener("click", toggleFullscreen);
  document.getElementById("overview")?.addEventListener("click", toggleOverview);
  document.querySelector(".video-action")?.addEventListener("click", toggleVideo);

  viewport.addEventListener("click", (event) => {
    if (!document.body.classList.contains("overview")) return;
    const slide = event.target.closest(".slide");
    if (!slide) return;
    const found = slides.indexOf(slide);
    document.body.classList.remove("overview");
    show(found);
    scaleStage();
  });

  window.addEventListener("resize", scaleStage);
  window.addEventListener("hashchange", () => show(fromHash(), { preserveFragments: true }));

  if (new URLSearchParams(location.search).has("print")) {
    document.body.classList.add("print-mode");
    slides.forEach((slide) => slide.classList.add("active"));
  } else {
    index = fromHash();
    show(index);
    scaleStage();
  }
})();
