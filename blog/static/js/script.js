    function toggleCommentSection() {
        console.log("Test")
        var commentSection = document.getElementById("comment-section");
        var toggleButton = document.getElementById("toggle-comment-section");
        if (commentSection.style.display === "none") {
            commentSection.style.display = "block";
            toggleButton.textContent = "Masquer la section des commentaires";
        } else {
            commentSection.style.display = "none";
            toggleButton.textContent = "Commentez cet article";
        }
    }