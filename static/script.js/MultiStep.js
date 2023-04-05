function NextTab(){
    let tab_1 = document.getElementById("tab-1");
    let tab_2 = document.getElementById("tab-2");
    tab_1.style.animation = "Smooth 0.2s 1";
    setTimeout(() => {
        tab_1.style.display = 'none';
        tab_2.style.display = "block";
    }, 100);
}
function PreviousTab(){
    let tab_1 = document.getElementById("tab-1");
    let tab_2 = document.getElementById("tab-2");
    tab_2.style.animation = "test 0.2s 1";
    setTimeout(() => {
        tab_2.style.display = 'none';
        tab_1.style.display = "block";
    }, 100);
}