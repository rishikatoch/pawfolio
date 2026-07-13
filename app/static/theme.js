const toggle = document.getElementById("themeToggle");

function setTheme(theme) {
    if (theme === "dark") {
        document.body.classList.add("dark-mode");
        toggle.textContent = "☀️";
    } else {
        document.body.classList.remove("dark-mode");
        toggle.textContent = "🌙";
    }

    localStorage.setItem("theme", theme);
}

const savedTheme = localStorage.getItem("theme") || "light";
setTheme(savedTheme);

toggle.addEventListener("click", () => {
    const newTheme = document.body.classList.contains("dark-mode")
        ? "light"
        : "dark";

    setTheme(newTheme);
});