document.addEventListener("DOMContentLoaded", () => {
  console.log("La página se cargó correctamente.");
  
  const loginButton = document.querySelector(".login-button");
  if (loginButton) {
    loginButton.addEventListener("click", () => {
      console.log("Iniciando sesión con Spotify...");
    });
  }
});
