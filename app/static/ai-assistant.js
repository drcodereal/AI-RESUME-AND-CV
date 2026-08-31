/* =========================================================
   AI RESUME ASSISTANT
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    const button = document.getElementById("aiAssistantButton");
    const chat = document.getElementById("aiAssistantChat");
    const closeButton = document.getElementById("aiAssistantClose");

    const messages = document.getElementById("aiAssistantMessages");
    const input = document.getElementById("aiAssistantInput");
    const sendButton = document.getElementById("aiAssistantSend");

    if (!button || !chat) return;


    /* Open */

    button.addEventListener("click", () => {
        chat.classList.add("open");

        setTimeout(() => {
            input?.focus();
        }, 300);
    });


    /* Close */

    closeButton?.addEventListener("click", () => {
        chat.classList.remove("open");
    });


    /* Escape */

    document.addEventListener("keydown", (event) => {

        if (event.key === "Escape") {
            chat.classList.remove("open");
        }

    });


    /* Send */

    async function sendMessage(customMessage = null) {

        const message =
            customMessage ||
            input.value.trim();

        if (!message) return;


        addMessage(message, "user");

        input.value = "";

        const typing = addTyping();


        try {

            const response = await fetch("/ai-assistant", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: message
                })

            });


            const data = await response.json();

            typing.remove();


            if (!response.ok) {

                addMessage(
                    data.error ||
                    "Sorry, something went wrong.",
                    "assistant"
                );

                return;
            }


            addMessage(
                data.reply ||
                "I couldn't generate a response.",
                "assistant"
            );


        } catch (error) {

            typing.remove();

            addMessage(
                "AI Assistant is currently unavailable. Please try again.",
                "assistant"
            );

            console.error(error);
        }

    }


    /* Send button */

    sendButton?.addEventListener("click", () => {
        sendMessage();
    });


    /* Enter */

    input?.addEventListener("keydown", (event) => {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();
        }

    });


    /* Quick questions */

    document.querySelectorAll(
        ".ai-quick-question"
    ).forEach((question) => {

        question.addEventListener("click", () => {

            const text =
                question.dataset.question ||
                question.textContent.trim();

            sendMessage(text);
        });

    });


    /* Add message */

    function addMessage(text, type) {

        const wrapper =
            document.createElement("div");

        wrapper.className =
            `ai-message ${type}`;


        const bubble =
            document.createElement("div");

        bubble.className =
            "ai-message-bubble";


        bubble.textContent = text;


        wrapper.appendChild(bubble);

        messages.appendChild(wrapper);

        scrollToBottom();
    }


    /* Typing */

    function addTyping() {

        const wrapper =
            document.createElement("div");

        wrapper.className =
            "ai-message assistant";


        wrapper.innerHTML = `
            <div class="ai-message-bubble">
                <div class="ai-typing">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;


        messages.appendChild(wrapper);

        scrollToBottom();

        return wrapper;
    }


    /* Scroll */

    function scrollToBottom() {

        messages.scrollTop =
            messages.scrollHeight;
    }

});