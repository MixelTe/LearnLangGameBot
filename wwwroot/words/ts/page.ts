import { Button } from "./littleLib.js";

export abstract class Page
{
	protected overBtn: HTMLButtonElement = Button(["overBtn", "overBtn_hidden"], [], () => this.onOverBtn());
	private onOverBtn = () => { };
	private onKeydown = (e: KeyboardEvent) => { if (e.key == "Enter") this.onOverBtn(); };
	protected return = (res: boolean) => { };

	public abstract generate(): HTMLDivElement;


	public run()
	{
		return new Promise<boolean>(res => { this.return = res });
	}

	protected showOverBtn(onClc: () => void)
	{
		window.removeEventListener("keydown", this.onKeydown);
		this.onOverBtn = () =>
		{
			window.removeEventListener("keydown", this.onKeydown);
			onClc();
			this.overBtn.classList.add("overBtn_hidden");
		};
		window.addEventListener("keydown", this.onKeydown);
		this.overBtn.classList.remove("overBtn_hidden");
	}
}
