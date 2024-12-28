import { feedbackBad } from "./functions.js";
import { Div } from "./littleLib.js";
import { Page } from "./page.js";

export class ErrorPage extends Page
{
	private error: string
	constructor(error: string | boolean)
	{
		super();
		this.error = typeof error == "string" ? error : "";
	}

	public generate(): HTMLDivElement
	{
		return Div(["page", "EP"], Div("EP_page", [
			Div("gradientText", "Произошла ошибка"),
			Div("gradientText", this.error),
			this.overBtn,
		]));
	}

	public run(): Promise<boolean>
	{
		feedbackBad();
		this.showOverBtn(() => this.return(true));
		return super.run();
	}
}