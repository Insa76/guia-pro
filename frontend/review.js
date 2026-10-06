const API_BASE_URL = "http://localhost:8000";


/*
============================================================
ELEMENTOS
============================================================
*/

const loadingState =
  document.getElementById("loading-state");

const errorState =
  document.getElementById("error-state");

const errorMessage =
  document.getElementById("error-message");

const reviewContent =
  document.getElementById("review-content");

const successState =
  document.getElementById("success-state");

const professionalName =
  document.getElementById("professional-name");

const jobTitle =
  document.getElementById("job-title");

const reviewForm =
  document.getElementById("review-form");

const ratingButtons =
  document.querySelectorAll(
    "#rating-buttons button"
  );

const ratingLabel =
  document.getElementById("rating-label");

const commentInput =
  document.getElementById("comment");

const submitButton =
  document.getElementById(
    "submit-review-button"
  );

const formMessage =
  document.getElementById("form-message");


/*
============================================================
ESTADO
============================================================
*/

let selectedRating = 0;
let reviewToken = null;


/*
============================================================
UTILIDADES
============================================================
*/

function show(element) {
  element.classList.remove("hidden");
}


function hide(element) {
  element.classList.add("hidden");
}


/*
============================================================
OBTENER TOKEN
============================================================
*/

function getReviewToken() {

  const params =
    new URLSearchParams(
      window.location.search
    );

  return params.get("token");
}


/*
============================================================
OBTENER CONTEXTO DE LA VALORACIÓN
============================================================

El backend devuelve:

- profesional
- trabajo realizado
- estado de la valoración

============================================================
*/

async function loadReviewContext() {

  if (!reviewToken) {
    throw new Error(
      "El enlace de valoración no contiene un token válido."
    );
  }

  const response = await fetch(
    `${API_BASE_URL}/api/reviews/public/${encodeURIComponent(reviewToken)}`
  );

  let data = null;

  try {
    data = await response.json();
  } catch {
    // Si el backend no devuelve JSON,
    // utilizamos el mensaje genérico.
  }

  if (!response.ok) {

    throw new Error(
      data?.detail ||
      "No se pudo validar el enlace de valoración."
    );
  }

  return data;
}


/*
============================================================
RENDER CONTEXTO
============================================================
*/

function renderReviewContext(data) {

  professionalName.textContent =
    `${data.first_name || ""} ${data.last_name || ""}`.trim();

  jobTitle.textContent =
    data.title || "Trabajo realizado";
}


/*
============================================================
RATING
============================================================
*/

function updateRating(rating) {

  selectedRating = rating;

  ratingButtons.forEach(button => {

    const buttonRating =
      Number(button.dataset.rating);

    button.classList.toggle(
      "selected",
      buttonRating <= rating
    );

  });

  const labels = {
    1: "Muy mala",
    2: "Mala",
    3: "Regular",
    4: "Buena",
    5: "Excelente",
  };

  ratingLabel.textContent =
    labels[rating] ||
    "Seleccioná una valoración";

  submitButton.disabled =
    selectedRating === 0;
}


/*
============================================================
MOSTRAR ERROR DEL FORMULARIO
============================================================
*/

function showFormError(message) {

  show(formMessage);

  formMessage.className =
    "form-message error-message";

  formMessage.textContent =
    message;
}


/*
============================================================
ENVIAR VALORACIÓN
============================================================
*/

async function submitReview(event) {

  event.preventDefault();

  if (!selectedRating) {

    showFormError(
      "Seleccioná una valoración."
    );

    return;
  }

  submitButton.disabled = true;

  submitButton.textContent =
    "Publicando...";

  hide(formMessage);

  try {

    const response = await fetch(
      `${API_BASE_URL}/api/reviews/public/${encodeURIComponent(reviewToken)}`,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          rating: selectedRating,
          comment:
            commentInput.value.trim() || null,
        }),
      }
    );

    let data = null;

    try {
      data = await response.json();
    } catch {
      // El backend podría responder sin JSON.
    }

    if (!response.ok) {

      throw new Error(
        data?.detail ||
        "No se pudo publicar la valoración."
      );
    }

    /*
    --------------------------------------------------------
    ÉXITO
    --------------------------------------------------------
    */

    hide(reviewContent);
    hide(loadingState);
    hide(errorState);

    show(successState);

  } catch (error) {

    console.error(
      "[Review] Error:",
      error
    );

    showFormError(
      error.message ||
      "Ocurrió un error al publicar la valoración."
    );

    submitButton.disabled = false;

    submitButton.textContent =
      "Publicar valoración";
  }
}


/*
============================================================
EVENTOS DE RATING
============================================================
*/

ratingButtons.forEach(button => {

  button.addEventListener(
    "click",
    () => {

      updateRating(
        Number(button.dataset.rating)
      );

    }
  );

});


/*
============================================================
EVENTO FORMULARIO
============================================================
*/

reviewForm.addEventListener(
  "submit",
  submitReview
);


/*
============================================================
INICIALIZACIÓN
============================================================
*/

async function init() {

  reviewToken =
    getReviewToken();

  try {

    const data =
      await loadReviewContext();

    /*
    --------------------------------------------------------
    TOKEN YA UTILIZADO
    --------------------------------------------------------
    */

    if (data.already_reviewed) {

      hide(loadingState);
      hide(reviewContent);

      show(errorState);

      errorMessage.textContent =
        "Esta valoración ya fue registrada. El enlace ya no puede volver a utilizarse.";

      return;
    }

    /*
    --------------------------------------------------------
    TOKEN VÁLIDO
    --------------------------------------------------------
    */

    renderReviewContext(data);

    hide(loadingState);
    hide(errorState);

    show(reviewContent);

  } catch (error) {

    console.error(
      "[Review] Error al cargar:",
      error
    );

    hide(loadingState);
    hide(reviewContent);

    show(errorState);

    errorMessage.textContent =
      error.message ||
      "No pudimos validar este enlace de valoración.";
  }
}


init();