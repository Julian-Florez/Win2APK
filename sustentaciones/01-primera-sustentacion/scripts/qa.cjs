const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const baseUrl = process.env.QA_URL || "http://127.0.0.1:8767/";
const root = path.resolve(__dirname, "..");
const qaDir = path.join(root, "qa");
fs.mkdirSync(qaDir, { recursive: true });

(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.QA_BROWSER || "/run/current-system/sw/bin/google-chrome",
    headless: true,
  });
  const errors = [];
  const browserErrors = [];
  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
  const page = await context.newPage();
  page.on("console", (message) => {
    if (message.type() === "error") browserErrors.push(`console: ${message.text()}`);
  });
  page.on("pageerror", (error) => browserErrors.push(`pageerror: ${error.message}`));
  page.on("requestfailed", (request) => {
    const failure = request.failure()?.errorText || "unknown";
    if (failure !== "net::ERR_ABORTED") browserErrors.push(`request: ${request.url()} ${failure}`);
  });

  await page.goto(baseUrl, { waitUntil: "networkidle" });
  const slideIds = await page.locator(".slide").evaluateAll((nodes) => nodes.map((node) => node.id));

  for (let i = 0; i < slideIds.length; i += 1) {
    const id = slideIds[i];
    await page.goto(`${baseUrl}#${id}`, { waitUntil: "networkidle" });
    if (id === "arquitectura") {
      await page.keyboard.press("ArrowRight");
      await page.keyboard.press("ArrowRight");
    }
    await page.waitForTimeout(450);
    await page.screenshot({ path: path.join(qaDir, `${String(i + 1).padStart(2, "0")}-${id}-1920x1080.png`) });
    const overflow = await page.locator(".slide.active").evaluate((slide) => {
      const offenders = [];
      for (const element of slide.querySelectorAll("h1,h2,h3,p,li,table,figure,video")) {
        const rect = element.getBoundingClientRect();
        const parent = slide.getBoundingClientRect();
        if (rect.right > parent.right + 2 || rect.bottom > parent.bottom + 2 || rect.left < parent.left - 2 || rect.top < parent.top - 2) {
          offenders.push(`${element.tagName}.${element.className || ""}`);
        }
      }
      return offenders;
    });
    if (overflow.length) errors.push(`${id}: ${overflow.join(", ")}`);
  }

  for (const viewport of [{ width: 1366, height: 768 }, { width: 1280, height: 720 }]) {
    await page.setViewportSize(viewport);
    for (const id of ["inicio", "arquitectura", "demo", "cierre"]) {
      await page.goto(`${baseUrl}#${id}`, { waitUntil: "networkidle" });
      if (id === "arquitectura") {
        await page.locator("#arquitectura .fragment").evaluateAll((nodes) => nodes.forEach((node) => node.classList.remove("visible")));
        await page.keyboard.press("ArrowRight");
        await page.keyboard.press("ArrowRight");
      }
      await page.waitForTimeout(450);
      await page.screenshot({ path: path.join(qaDir, `${id}-${viewport.width}x${viewport.height}.png`) });
    }
  }

  await page.setViewportSize({ width: 1920, height: 1080 });
  const interactions = {};

  await page.goto(baseUrl, { waitUntil: "networkidle" });
  await page.locator("#next").click();
  interactions.nextButton = await page.evaluate(() => window.location.hash === "#barrera");
  await page.locator("#previous").click();
  interactions.previousButton = await page.evaluate(() => window.location.hash === "#inicio");
  await page.keyboard.press("b");
  interactions.backupShortcut = await page.evaluate(() => window.location.hash === "#backup");

  await page.keyboard.press("o");
  interactions.overviewEntered = await page.locator("body").evaluate((node) => node.classList.contains("overview"));
  await page.locator("#metodo").click();
  interactions.overviewExited = await page.evaluate(
    () => !document.body.classList.contains("overview") && window.location.hash === "#metodo",
  );

  await page.goto(`${baseUrl}#arquitectura`, { waitUntil: "networkidle" });
  await page.keyboard.press("ArrowRight");
  const firstReveal = await page.locator("#arquitectura .fragment.visible").count();
  await page.keyboard.press("ArrowRight");
  const secondReveal = await page.locator("#arquitectura .fragment.visible").count();
  await page.keyboard.press("ArrowLeft");
  const reverseReveal = await page.locator("#arquitectura .fragment.visible").count();
  interactions.progressiveReveal = firstReveal === 1 && secondReveal === 2 && reverseReveal === 1;

  await page.goto(baseUrl, { waitUntil: "networkidle" });
  interactions.fullscreenAvailable = await page.evaluate(() => document.fullscreenEnabled);
  if (interactions.fullscreenAvailable) {
    await page.locator("#fullscreen").click();
    await page.waitForTimeout(150);
    interactions.fullscreenButton = await page.evaluate(() => document.fullscreenElement !== null);
    if (interactions.fullscreenButton) await page.evaluate(() => document.exitFullscreen());
  } else {
    interactions.fullscreenButton = "not available in headless browser";
  }

  for (const [name, value] of Object.entries(interactions)) {
    if (value === false) errors.push(`interaction: ${name}`);
  }

  await page.goto(`${baseUrl}#demo`, { waitUntil: "networkidle" });
  const video = page.locator("video");
  await video.evaluate((node) => node.play());
  await page.waitForTimeout(1200);
  const videoState = await video.evaluate((node) => ({ paused: node.paused, readyState: node.readyState, currentTime: node.currentTime }));
  if (videoState.paused || videoState.readyState < 2 || videoState.currentTime <= 0) {
    errors.push(`video: ${JSON.stringify(videoState)}`);
  }

  const report = {
    generatedAt: new Date().toISOString(),
    baseUrl,
    slideCount: slideIds.length,
    checkedViewports: ["1920x1080", "1366x768", "1280x720"],
    interactions,
    videoState,
    browserErrors,
    layoutErrors: errors,
    ok: browserErrors.length === 0 && errors.length === 0,
  };
  fs.writeFileSync(path.join(qaDir, "reporte.json"), `${JSON.stringify(report, null, 2)}\n`);
  await browser.close();

  if (!report.ok) {
    process.stderr.write(`${JSON.stringify(report, null, 2)}\n`);
    process.exit(1);
  }
  process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
})().catch((error) => {
  process.stderr.write(`${error.stack}\n`);
  process.exit(1);
});
