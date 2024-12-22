export function feedbackGood()
{
	document.body.classList.remove("gradient_good")
	setTimeout(() => document.body.classList.add("gradient_good"), 50);
	setTimeout(() => document.body.classList.remove("gradient_good"), 1100);
}
export function feedbackBad()
{
	document.body.classList.remove("gradient_bad")
	setTimeout(() => document.body.classList.add("gradient_bad"), 50);
	setTimeout(() => document.body.classList.remove("gradient_bad"), 1100);
}
let feedbackLoadingRun = false;
export function feedbackLoadingStart()
{
	feedbackLoadingRun = true;
	document.body.classList.add("gradient_loading");
	setTimeout(() =>
	{
		document.body.classList.remove("gradient_loading");
		if (feedbackLoadingRun)
			setTimeout(feedbackLoadingStart, 50);
	}, 1100);
}
export function feedbackLoadingEnd()
{
	feedbackLoadingRun = false;
}
export async function wait(t: number)
{
	return new Promise<void>(r => setTimeout(r, t));
}
export function toCapitalCase(str: string)
{
	if (str.length == 0) return "";
	return str[0].toUpperCase() + str.slice(1);
}