(() => {
    console.log("🔥 Mermaid.js live rendering enabled");
    const script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js";
    script.onload = () => {
        mermaid.initialize({ startOnLoad: true, theme: "default" });
        setInterval(() => {
            document.querySelectorAll("pre code.language-mermaid").forEach((block) => {
                if (!block.dataset.rendered) {
                    const container = document.createElement("div");
                    container.classList.add("mermaid");
                    container.innerText = block.innerText;
                    block.parentElement.replaceWith(container);
                    mermaid.init(undefined, container);
                    block.dataset.rendered = "true";
                }
            });
        }, 1000);
    };
    document.head.appendChild(script);
})();
