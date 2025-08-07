const targetButtons = document.getElementsByClassName("custom-loading-overlay");

Array.from(targetButtons).forEach(button => {
    button.addEventListener("click", function () {
        // オーバーレイを表示
        document.getElementById("custom-loading-overlay").style.display = "block";
    });
});


