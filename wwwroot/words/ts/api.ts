import { wait } from "./littleLib.js";

export interface TesterData
{
	title: string,
	questions: TesterQuestion[],
}
export type TesterQuestion = WordSelect | WordInput;
export interface WordSelect
{
	type: "WordSelect",
	id: number,
	word: string;
	options: string[];
	correctI: number;
}
export interface WordInput
{
	type: "WordInput",
	id: number,
	question: string;
	answers: string[];
}
export interface TestResult
{
	id: number,
	result: boolean,
}

export async function getData(): Promise<TesterData>
{
	await wait(400);
	return {
		title: "The best theme",
		questions: [
			{
				type: "WordInput",
				id: 10,
				question: "Яблоко",
				answers: ["the apple (noun)", "the apple", "apple"],
			},
			{
				type: "WordSelect",
				id: 1,
				word: "Яблоко",
				options: ["Peach", "Apple", "Pear", "Pineapple"],
				correctI: 1,
			},
			{
				type: "WordSelect",
				id: 2,
				word: "Стул",
				options: ["Armchair", "Table", "Chair", "Sofa"],
				correctI: 2,
			},
			{
				type: "WordSelect",
				id: 3,
				word: "Star",
				options: ["Солнце", "Планета", "Марс", "Звезда"],
				correctI: 3,
			},
		]
	}
}
export async function saveResult(results: TestResult[])
{
	await wait(400);
	console.log(results);
}