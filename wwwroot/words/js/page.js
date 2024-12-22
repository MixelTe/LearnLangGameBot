import { Button } from "./littleLib.js";
export class Page {
    overBtn = Button(["overBtn", "overBtn_hidden"], [], () => this.onOverBtn());
    onOverBtn = () => { };
    onKeydown = (e) => { if (e.key == "Enter")
        this.onOverBtn(); };
    return = (res) => { };
    run() {
        return new Promise(res => { this.return = res; });
    }
    showOverBtn(onClc) {
        window.removeEventListener("keydown", this.onKeydown);
        this.onOverBtn = () => {
            window.removeEventListener("keydown", this.onKeydown);
            onClc();
            this.overBtn.classList.add("overBtn_hidden");
        };
        window.addEventListener("keydown", this.onKeydown);
        this.overBtn.classList.remove("overBtn_hidden");
    }
}
