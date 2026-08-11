document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("pawfolio-ai-form");
    const input = document.getElementById("pawfolio-ai-input");
    const chat = document.getElementById("pawfolio-ai-chat");
    const suggestions = document.querySelectorAll(".pawfolio-ai-suggestion");

    if (!form || !input || !chat) {
        return;
    }

    function scrollChatToBottom() {
        chat.scrollTo({
            top: chat.scrollHeight,
            behavior: "smooth"
        });
    }

    function addMessage(message, type) {
        const wrapper = document.createElement("div");
        wrapper.className = `pawfolio-ai-message pawfolio-ai-message-${type}`;

        const content = document.createElement("div");
        content.className = "pawfolio-ai-message-content";
        content.textContent = message;

        wrapper.appendChild(content);
        chat.appendChild(wrapper);

        scrollChatToBottom();

        return wrapper;
    }

    function setLoadingState(isLoading) {
        input.disabled = isLoading;

        suggestions.forEach(button => {
            button.disabled = isLoading;
        });

        const submitButton = form.querySelector(".pawfolio-ai-submit");

        if (submitButton) {
            submitButton.disabled = isLoading;
            submitButton.setAttribute("aria-busy", isLoading ? "true" : "false");
        }
    }

    async function askAI(question) {
        const trimmedQuestion = question.trim();

        if (!trimmedQuestion) {
            return;
        }

        setLoadingState(true);

        addMessage(trimmedQuestion, "user");

        const loadingMessage = addMessage(
            "Pawfolio AI is thinking...",
            "assistant"
        );

        try {
            const response = await fetch("/api/ai/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    message: trimmedQuestion
                })
            });

            let data = {};

            try {
                data = await response.json();
            } catch {
                data = {};
            }

            loadingMessage.remove();

            if (!response.ok) {
                throw new Error(
                    data.error || "Pawfolio AI is temporarily unavailable."
                );
            }

            addMessage(
                data.answer || "I couldn't generate an answer.",
                "assistant"
            );

        } catch (error) {
            loadingMessage.remove();

            addMessage(
                error.message || "Something went wrong. Please try again.",
                "error"
            );

        } finally {
            setLoadingState(false);
            input.focus();
        }
    }

    form.addEventListener("submit", event => {
        event.preventDefault();

        const question = input.value.trim();

        if (!question) {
            return;
        }

        input.value = "";

        askAI(question);
    });

    input.addEventListener("keydown", event => {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            form.requestSubmit();
        }
    });

    suggestions.forEach(button => {
        button.addEventListener("click", () => {
            const question = button.dataset.aiQuestion;

            if (!question || input.disabled) {
                return;
            }

            input.value = "";
            askAI(question);
        });
    });
});
