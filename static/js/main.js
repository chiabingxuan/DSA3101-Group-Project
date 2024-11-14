import { initPage } from "./init.js";

function init(event) {
    if (event.target.readyState === "complete") {
        initPage();
    }
}

// Driver code
document.addEventListener("readystatechange", init);