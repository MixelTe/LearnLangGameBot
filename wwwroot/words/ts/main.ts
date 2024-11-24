import { Div, getDiv, H1, initEl, SetContent } from "./littleLib.js";

const pageEl = Div("page", [
    initEl("pre", [], JSON.stringify(TelegramGameProxy.initParams, null, 4)),
    Div([], location.href),
    initEl("pre", [], JSON.stringify(Telegram.WebApp, null, 4)),
]);
console.log(TelegramGameProxy.initParams);
SetContent(getDiv("root"), (() =>
{
    return [
        H1("header", "Learning <theme 1.2>"),
        pageEl,
    ];
})())

const loader = getDiv("loader");
loader.classList.add("loader_hidden");
setTimeout(() => document.body.removeChild(loader), 350);