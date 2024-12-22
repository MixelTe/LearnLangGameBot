import type { WordSelect } from "./api.js";
import { feedbackBad, feedbackGood } from "./functions.js";
import { Button, Div, Span, wait } from "./littleLib.js";
import { Page } from "./page.js";

export class TesterSelectWord extends Page
{
	private btns: HTMLButtonElement[] = [];
	constructor(private wordSelect: WordSelect)
	{
		super();
	}

	public generate()
	{
		this.btns = this.wordSelect.options.map((w, i) =>
			Button("TSW_option", Span("gradientText", w), () => this.onAnswer(i))
		)
		return Div(["page", "TSW"], [
			Div(["TSW_title", "gradientText"], this.wordSelect.word),
			Div(["TSW_options", "gradientBack"], Div([], this.btns)),
			this.overBtn,
		]);
	}

	private async onAnswer(selectedI: number)
	{
		this.btns.forEach((btn, i) =>
		{
			btn.disabled = true;
			btn.classList.add(i == this.wordSelect.correctI ? "TSW_correct" : "TSW_wrong");
		});
		this.btns[selectedI].classList.add("TSW_selected");
		const correct = selectedI == this.wordSelect.correctI;
		if (correct)
			feedbackGood();
		else
			feedbackBad();
		this.showOverBtn(() => this.return(correct));
	}
}
