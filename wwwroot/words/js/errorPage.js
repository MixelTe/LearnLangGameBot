import { feedbackBad } from "./functions.js";
import { Div } from "./littleLib.js";
import { Page } from "./page.js";
export class ErrorPage extends Page {
    error;
    constructor(error) {
        super();
        this.error = typeof error == "string" ? error : "";
    }
    generate() {
        return Div(["page", "EP"], Div("EP_page", [
            Div("gradientText", "Произошла ошибка"),
            Div("gradientText", this.error),
            this.overBtn,
        ]));
    }
    run() {
        feedbackBad();
        this.showOverBtn(() => this.return(true));
        return super.run();
    }
}
