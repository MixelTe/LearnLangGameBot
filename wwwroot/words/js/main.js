import { getData, saveResult } from "./api.js";
import { ErrorPage } from "./errorPage.js";
import { feedbackLoadingEnd, feedbackLoadingStart } from "./functions.js";
import { Div, getDiv, H1, SetContent } from "./littleLib.js";
import { ResultPage } from "./resultPage.js";
import { testerInputWord } from "./testerInputWord.js";
import { TesterSelectWord } from "./testerSelectWord.js";
const pageEl = Div("page-container");
const pageHeader = H1(["header", "gradientText"]);
SetContent(getDiv("root"), [
    pageHeader,
    pageEl,
]);
start(true);
async function start(firstStart = false) {
    if (!firstStart)
        feedbackLoadingStart();
    const data = await getData();
    feedbackLoadingEnd();
    pageHeader.innerText = data.title;
    const loader = document.getElementById("loader");
    if (loader) {
        loader.classList.add("loader_hidden");
        setTimeout(() => document.body.removeChild(loader), 350);
    }
    if (data.loadError) {
        await runPage(new ErrorPage(data.loadError));
        start();
        return;
    }
    // await runPage(new ResultPage([{ "id": 1, "result": false }, { "id": 2, "result": false }, { "id": 3, "result": true }]));
    const results = [];
    for (const q of data.questions) {
        const pageCls = {
            WordSelect: TesterSelectWord,
            WordInput: testerInputWord,
        }[q.type];
        if (pageCls == undefined) {
            console.error(`wrong tester type: ${q.type}`);
            continue;
        }
        const r = await runPage(new pageCls(q));
        results.push({
            id: q.id,
            result: r,
        });
    }
    saveResult(results);
    await runPage(new ResultPage(results));
    start();
}
async function runPage(newPage) {
    for (let i = 0; i < pageEl.children.length; i++) {
        const page = pageEl.children[i];
        page.classList.add("page_fading");
        setTimeout(() => pageEl.removeChild(page), 300);
    }
    const page = newPage.generate();
    page.classList.add("page_hidden");
    pageEl.appendChild(page);
    setTimeout(() => page.classList.remove("page_hidden"));
    setTimeout(() => document.body.querySelectorAll(".gradientBack, .gradientText").forEach(_el => {
        const el = _el;
        el.style.setProperty("--bx", `-${el.offsetLeft}px`);
        el.style.setProperty("--by", `-${el.offsetTop}px`);
    }), 100);
    return newPage.run();
}
