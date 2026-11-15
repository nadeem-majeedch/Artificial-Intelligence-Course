/* global mermaid, document$ */

mermaid.initialize({
  startOnLoad: false,
  securityLevel: "loose",
  theme: "base",
  themeVariables: {
    primaryColor: "#e8f1f7",
    primaryTextColor: "#102a43",
    primaryBorderColor: "#0b4f78",
    lineColor: "#526b80",
    secondaryColor: "#f7f4ed",
    tertiaryColor: "#ffffff",
    fontFamily: "Inter, system-ui, sans-serif"
  }
});

document$.subscribe(async () => {
  const diagrams = document.querySelectorAll(".mermaid");
  if (diagrams.length) {
    await mermaid.run({ querySelector: ".mermaid" });
  }
});
