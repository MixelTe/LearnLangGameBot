import { Div, getDiv, H1, SetContent } from "./littleLib.js";

const pageEl = Div("page", [
    Div([], JSON.stringify(TelegramGameProxy.initParams)),
    Div([], location.href),
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