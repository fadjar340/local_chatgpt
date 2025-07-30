(() => {
    console.log("🔥 MathJax + TikZ live rendering enabled");

    // Load MathJax
    const mathjaxScript = document.createElement("script");
    mathjaxScript.src = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js";
    mathjaxScript.onload = () => {
        console.log("✅ MathJax loaded for LaTeX/TikZ rendering");

        // Observe new chat messages
        const observer = new MutationObserver(() => {
            document.querySelectorAll("pre code.language-latex, pre code.language-tex").forEach((block) => {
                if (!block.dataset.rendered) {
                    const container = document.createElement("div");
                    container.innerHTML = `$$${block.innerText}$$`;
                    block.parentElement.replaceWith(container);
                    MathJax.typesetPromise([container]);
                    block.dataset.rendered = "true";
                }
            });
        });

        observer.observe(document.body, { childList: true, subtree: true });
    };

    document.head.appendChild(mathjaxScript);
})();
