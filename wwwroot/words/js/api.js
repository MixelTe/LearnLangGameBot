import { FetchError, fetchJsonPost, wait } from "./littleLib.js";
const url = new URL(window.location.href);
const UID = url.searchParams.get("uid");
const TID = url.searchParams.get("tid");
export async function getData() {
    // return await getData_test();
    if (!UID || !TID)
        return {
            loadError: !UID ? "uid is undefined" : "tid is undefined",
            title: "",
            questions: [],
        };
    try {
        return await fetchJsonPost("/api/get_words", {
            uid: UID,
            tid: TID
        });
    }
    catch (e) {
        console.error(e);
        return {
            loadError: e instanceof FetchError ? e.message : true,
            title: "",
            questions: [],
        };
    }
}
async function getData_test() {
    await wait(400);
    return {
        title: "The best theme",
        loadError: false,
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
    };
}
export async function saveResult(results) {
    console.log(results);
    await fetchJsonPost("/api/save_result", {
        uid: UID,
        results,
    });
}
