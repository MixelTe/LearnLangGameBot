import { wait } from "./littleLib.js";
export async function getData() {
    await wait(400);
    return {
        title: "The best theme",
        questions: [
            {
                type: "WordInput",
                id: 10,
                question: "Яблоко",
                answers: ["the apple (object)", "the apple", "apple"],
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
    };
}
export async function saveResult(results) {
    await wait(400);
    console.log(results);
}
