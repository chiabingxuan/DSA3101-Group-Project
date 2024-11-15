export function initPage() {
    // Handle toggling of menu
    const menuButton = document.querySelector("#menu-button");
    const menuIcon = document.querySelector("#menu-icon");
    const nav = document.querySelector("#nav-bar");
    const main = document.querySelector("#main");
    let navIsHidden = true;

    function toggleMenu(event) {
        menuIcon.classList.toggle("spin");
        nav.classList.toggle("hide");
        navIsHidden = !navIsHidden;   // toggle the navIsHidden boolean variable
    }
    
    function hideMenuByClickingMain(event) {
        if (!navIsHidden) {
            toggleMenu(event);   // if nav is currently opened and main is clicked, nav will be hidden
        }
    }
    
    if (menuButton) {
        menuButton.addEventListener("click", toggleMenu);
        main.addEventListener("click", hideMenuByClickingMain);
    }
}