import { feedbackBad, feedbackGood } from "./functions.js";
import { Button, Div, Input, Span, toCapitalCase } from "./littleLib.js";
import { Page } from "./page.js";
import { string_correction_by_smith_waterman_algorithm, string_similarity_by_smith_waterman_algorithm } from "./smith_waterman_algorithm.js";
export class testerInputWord extends Page {
    wordInput;
    root = Div();
    input = Input("TIW_input", "text");
    inputShadow = Div("TIW_inputShadow");
    btn = Button("TIW_answerBtn", ">", () => this.onAnswer());
    callback = (e) => { if (e.key == "Enter")
        this.onAnswer(); };
    constructor(wordInput) {
        super();
        this.wordInput = wordInput;
    }
    generate() {
        this.root = Div(["page", "TIW"], [
            Div(["TIW_title", "gradientText"], [
                Div([], toCapitalCase(this.wordInput.question)),
                Div([], toCapitalCase(this.wordInput.answers[0])),
            ]),
            Div("TIW_inputsContainer", [
                Div(),
                Div(["TIW_inputs", "gradientBack"], [this.input, this.inputShadow, this.btn]),
                Div(),
            ]),
            this.overBtn,
        ]);
        return this.root;
    }
    run() {
        window.addEventListener("keydown", this.callback);
        this.input.focus();
        return super.run();
    }
    async onAnswer() {
        window.removeEventListener("keydown", this.callback);
        const inp = this.input.value.trim().toLowerCase().replaceAll(/\s+/g, " ");
        const correct = this.wordInput.answers.includes(inp);
        this.root.classList.add("TIW_selected");
        this.input.disabled = true;
        if (correct) {
            this.inputShadow.appendChild(Div("gradientText", toCapitalCase(inp)));
            feedbackGood();
        }
        else {
            this.inputShadow.appendChild(Div("TIW_error", this.genInputErrorFeedback(inp)));
            feedbackBad();
        }
        this.showOverBtn(() => this.return(correct));
    }
    genInputErrorFeedback(input) {
        if (input.length == 0)
            return Span();
        const correct = this.wordInput.answers
            .map(v => ({ ans: v, sim: string_similarity_by_smith_waterman_algorithm(v, input) }))
            .sort((a, b) => b.sim - a.sim)[0];
        if (correct.sim < 0.5)
            return Span("TIW_error__ch_e", toCapitalCase(input));
        const sc = string_correction_by_smith_waterman_algorithm(correct.ans, input);
        if (sc.length >= 1) {
            sc[0].val = sc[0].val.toUpperCase();
            sc[0].cor = sc[0].cor.toUpperCase();
        }
        const r = Span([], sc.map(v => {
            if (v.val == v.cor)
                return Span("TIW_error__ch_c", v.val);
            else if (v.val == "")
                return Span("TIW_error__ch_a", v.cor);
            else if (v.cor == "")
                return Span("TIW_error__ch_e", v.val);
            else
                return Span("TIW_error__ch_w", [Span([], v.val), Span([], v.cor)]);
        }));
        return r;
    }
}
