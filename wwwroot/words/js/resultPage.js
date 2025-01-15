import { Button, Div, Span } from "./littleLib.js";
import { Page } from "./page.js";
export class ResultPage extends Page {
    results;
    scoreEl = Div(["RP_text", "gradientText"]);
    constructor(results) {
        super();
        this.results = results;
    }
    generate() {
        const countAll = this.results.length;
        const countRight = this.results.filter(v => v.result).length;
        const percent = Math.floor(countRight / countAll * 100);
        return Div(["page", "RP"], Div("RP_page", [
            Div(["RP_title", "gradientText"], "Итого!"),
            Div(["RP_text", "gradientText"], `Правильных ответов:`),
            Div(["RP_text", "gradientText"], `${countRight} из ${countAll} - ${percent}%`),
            this.scoreEl,
            Button(["RP_again", "gradientBack"], Span([], Span("gradientText", "Ещё раз!")), () => this.return(true)),
            this.overBtn,
        ]));
    }
    onGetScore(score) {
        this.scoreEl.innerText = `Score: ${score}`;
    }
}
