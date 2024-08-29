document.addEventListener("DOMContentLoaded", function () {
  const textArray = ["Bienvenido..."];
  const typingSpeed = 100; // Velocidad de tipeo en milisegundos
  const erasingSpeed = 50; // Velocidad de borrado en milisegundos
  const delayBetweenTexts = 1500; // Tiempo entre textos en milisegundos
  let textIndex = 0;
  let charIndex = 0;

  const typewriterElement = document.getElementById("typewriter");

  function type() {
    if (charIndex < textArray[textIndex].length) {
      typewriterElement.textContent += textArray[textIndex].charAt(charIndex);
      charIndex++;
      setTimeout(type, typingSpeed);
    } else {
      setTimeout(erase, delayBetweenTexts);
    }
  }

  function erase() {
    if (charIndex > 0) {
      typewriterElement.textContent = textArray[textIndex].substring(0, charIndex - 1);
      charIndex--;
      setTimeout(erase, erasingSpeed);
    } else {
      textIndex++;
      if (textIndex >= textArray.length) textIndex = 0;
      setTimeout(type, typingSpeed + 1100);
    }
  }

  setTimeout(type, delayBetweenTexts + 250);
});