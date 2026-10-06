const API_BASE_URL = "http://localhost:8000";

const PROFESSIONAL_TOKEN_STORAGE_KEY =
  "guia_pro_professional_token";

let professionalId = null;
let professionalToken = null;


/*
============================================================
AUTENTICACIÓN
============================================================
*/

function getProfessionalToken() {
  return sessionStorage.getItem(
    PROFESSIONAL_TOKEN_STORAGE_KEY
  );
}


function getAuthHeaders() {
  return {
    Authorization: `Bearer ${professionalToken}`,
  };
}


async function loadAuthenticatedProfessional() {
  professionalToken =
    getProfessionalToken();

  if (!professionalToken) {
    throw new Error(
      "No hay una sesión de profesional activa."
    );
  }

  const response = await fetch(
    `${API_BASE_URL}/api/professional/auth/me`,
    {
      headers: getAuthHeaders(),
    }
  );

  let data = null;

  try {
    data = await response.json();
  } catch {}

  if (!response.ok) {
    sessionStorage.removeItem(
      PROFESSIONAL_TOKEN_STORAGE_KEY
    );

    throw new Error(
      data?.detail ||
      "La sesión del profesional no es válida."
    );
  }

  professionalId =
    data.professional_id;

  return professionalId;
}


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

const professionalContent =
  document.getElementById(
    "professional-content"
  );

const professionalName =
  document.getElementById(
    "professional-name"
  );

const professionalMeta =
  document.getElementById(
    "professional-meta"
  );

const professionalRating =
  document.getElementById(
    "professional-rating"
  );

const jobsList =
  document.getElementById(
    "jobs-list"
  );

const jobsEmpty =
  document.getElementById(
    "jobs-empty"
  );

const newJobButton =
  document.getElementById(
    "new-job-button"
  );

const newJobPanel =
  document.getElementById(
    "new-job-panel"
  );

const newJobForm =
  document.getElementById(
    "new-job-form"
  );

const cancelJobButton =
  document.getElementById(
    "cancel-job-button"
  );

const jobFormMessage =
  document.getElementById(
    "job-form-message"
  );

const logoutButton =
  document.getElementById(
    "logout-button"
  );

const publicProfileLink =
  document.getElementById(
    "public-profile-link"
  );


/*
============================================================
EDICIÓN DE PERFIL
============================================================
*/

const editProfileButton =
  document.getElementById(
    "edit-profile-button"
  );

const profileEditForm =
  document.getElementById(
    "profile-edit-form"
  );

const cancelProfileButton =
  document.getElementById(
    "cancel-profile-button"
  );

const profileFormMessage =
  document.getElementById(
    "profile-form-message"
  );

const profileDescription =
  document.getElementById(
    "profile-description"
  );

const profileYearsExperience =
  document.getElementById(
    "profile-years-experience"
  );

const profileWhatsapp =
  document.getElementById(
    "profile-whatsapp"
  );

const profileInstagram =
  document.getElementById(
    "profile-instagram"
  );

const profileCategories =
  document.getElementById(
    "profile-categories"
  );

const profileLocations =
  document.getElementById(
    "profile-locations"
  );


/*
============================================================
ESTADO DEL PERFIL
============================================================
*/

const profileIdentityStatus =
  document.getElementById(
    "profile-identity-status"
  );

const profileExperienceStatus =
  document.getElementById(
    "profile-experience-status"
  );

const profileReputationStatus =
  document.getElementById(
    "profile-reputation-status"
  );

const profileReputationDetail =
  document.getElementById(
    "profile-reputation-detail"
  );

const profileJobsStatus =
  document.getElementById(
    "profile-jobs-status"
  );

const profileJobsDetail =
  document.getElementById(
    "profile-jobs-detail"
  );

const professionalReviewsList =
  document.getElementById(
    "professional-reviews-list"
  );

const professionalReviewsEmpty =
  document.getElementById(
    "professional-reviews-empty"
  );


/*
============================================================
UTILIDADES
============================================================
*/

function show(element) {
  if (element) {
    element.classList.remove("hidden");
  }
}


function hide(element) {
  if (element) {
    element.classList.add("hidden");
  }
}


function escapeHtml(value) {
  if (
    value === null ||
    value === undefined
  ) {
    return "";
  }

  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}


function formatDate(value) {
  if (!value) {
    return "";
  }

  const date = new Date(value);

  if (
    Number.isNaN(
      date.getTime()
    )
  ) {
    return "";
  }

  return date.toLocaleDateString(
    "es-AR",
    {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    }
  );
}


/*
============================================================
CARGAR PROFESIONAL
============================================================
*/

async function loadProfessional() {
  const response = await fetch(
    `${API_BASE_URL}/api/public/professionals/${professionalId}/profile`
  );

  if (!response.ok) {
    throw new Error(
      `No se pudo cargar el profesional (${response.status})`
    );
  }

  return response.json();
}


/*
============================================================
CARGAR OPCIONES DEL PERFIL
============================================================
*/

async function loadProfileOptions() {
  const [
    categoriesResponse,
    locationsResponse,
  ] = await Promise.all([
    fetch(
      `${API_BASE_URL}/api/categories`
    ),
    fetch(
      `${API_BASE_URL}/api/locations`
    ),
  ]);

  if (!categoriesResponse.ok) {
    throw new Error(
      "No se pudieron cargar las categorías."
    );
  }

  if (!locationsResponse.ok) {
    throw new Error(
      "No se pudieron cargar las ubicaciones."
    );
  }

  const categories =
    await categoriesResponse.json();

  const locations =
    await locationsResponse.json();

  profileCategories.innerHTML = "";

  categories.forEach(
    category => {
      const option =
        document.createElement(
          "option"
        );

      option.value =
        category.id;

      option.textContent =
        category.name;

      profileCategories.appendChild(
        option
      );
    }
  );

  profileLocations.innerHTML = "";

  locations.forEach(
    location => {
      const option =
        document.createElement(
          "option"
        );

      option.value =
        location.id;

      option.textContent =
        `${location.name} · ${location.province}`;

      profileLocations.appendChild(
        option
      );
    }
  );
}


function fillProfileForm(
  professional
) {
  profileDescription.value =
    professional.description || "";

  profileYearsExperience.value =
    professional.years_experience ??
    "";

  profileWhatsapp.value =
    professional.whatsapp || "";

  profileInstagram.value =
    professional.instagram || "";

  const categoryIds =
    (professional.categories || [])
      .map(
        category =>
          String(category.id)
      );

  Array.from(
    profileCategories.options
  ).forEach(
    option => {
      option.selected =
        categoryIds.includes(
          option.value
        );
    }
  );

  const locationIds =
    (professional.locations || [])
      .map(
        location =>
          String(location.id)
      );

  Array.from(
    profileLocations.options
  ).forEach(
    option => {
      option.selected =
        locationIds.includes(
          option.value
        );
    }
  );
}


/*
============================================================
CARGAR TRABAJOS
============================================================
*/

async function loadJobs() {
  const response = await fetch(
    `${API_BASE_URL}/api/jobs/professional/${professionalId}`,
    {
      headers:
        getAuthHeaders(),
    }
  );

  if (!response.ok) {
    throw new Error(
      `No se pudieron cargar los trabajos (${response.status})`
    );
  }

  return response.json();
}


/*
============================================================
RENDER PROFESIONAL
============================================================
*/

function renderProfessional(
  professional
) {
  professionalName.textContent =
    `${professional.first_name} ${professional.last_name}`;

  const categories =
    professional.categories
      ?.map(
        category =>
          category.name
      )
      .join(" · ");

  const locations =
    professional.locations
      ?.map(
        location =>
          location.locality
      )
      .join(" · ");

  professionalMeta.textContent =
    [
      categories,
      locations,
    ]
      .filter(Boolean)
      .join(" · ");

  professionalRating.innerHTML = `
    <strong>
      ⭐ ${Number(
        professional.average_rating || 0
      ).toFixed(1)}
    </strong>

    <span>
      ${professional.total_reviews || 0}
      ${
        professional.total_reviews === 1
          ? "opinión"
          : "opiniones"
      }
    </span>
  `;


  /*
  ==========================================================
  ESTADO DEL PERFIL
  ==========================================================
  */

  if (profileIdentityStatus) {
    profileIdentityStatus.textContent =
      professional.identity_verified
        ? "✓ Verificada"
        : "Pendiente";
  }

  if (profileExperienceStatus) {
    profileExperienceStatus.textContent =
      professional.years_experience != null
        ? `${professional.years_experience} años`
        : "Sin informar";
  }

  const reputation =
    professional.reputation || {};

  const averageRating =
    Number(
      reputation.average_rating || 0
    );

  const totalReviews =
    Number(
      reputation.total_reviews || 0
    );

  const totalJobs =
    Number(
      reputation.total_jobs || 0
    );

  const ratedJobs =
    Number(
      reputation.rated_jobs || 0
    );

  if (profileReputationStatus) {
    profileReputationStatus.textContent =
      totalReviews > 0
        ? `⭐ ${averageRating.toFixed(1)}`
        : "Sin opiniones";
  }

  if (profileReputationDetail) {
    profileReputationDetail.textContent =
      totalReviews === 1
        ? "1 opinión"
        : `${totalReviews} opiniones`;
  }

  if (profileJobsStatus) {
    profileJobsStatus.textContent =
      String(totalJobs);
  }

  if (profileJobsDetail) {
    profileJobsDetail.textContent =
      ratedJobs === 1
        ? "1 trabajo valorado"
        : `${ratedJobs} trabajos valorados`;
  }
}


/*
============================================================
RENDER OPINIONES
============================================================
*/

function renderProfessionalReviews(
  reviews
) {
  professionalReviewsList.innerHTML =
    "";

  if (
    !reviews ||
    reviews.length === 0
  ) {
    show(
      professionalReviewsEmpty
    );
    return;
  }

  hide(
    professionalReviewsEmpty
  );

  reviews.forEach(
    review => {
      const article =
        document.createElement(
          "article"
        );

      article.className =
        "professional-review-item";

      const rating =
        Number(
          review.rating || 0
        );

      const stars =
        "★".repeat(rating) +
        "☆".repeat(
          Math.max(
            0,
            5 - rating
          )
        );

      article.innerHTML = `
        <div class="professional-review-top">

          <span class="professional-review-stars">
            ${stars}
          </span>

          <strong>
            ${rating}/5
          </strong>

        </div>

        ${
          review.comment
            ? `
              <p class="professional-review-comment">
                ${escapeHtml(
                  review.comment
                )}
              </p>
            `
            : ""
        }

        ${
          review.created_at
            ? `
              <span class="professional-review-date">
                ${formatDate(
                  review.created_at
                )}
              </span>
            `
            : ""
        }
      `;

      professionalReviewsList.appendChild(
        article
      );
    }
  );
}


/*
============================================================
RENDER TRABAJOS
============================================================
*/

function renderJobs(jobs) {
  jobsList.innerHTML = "";

  if (
    !jobs ||
    jobs.length === 0
  ) {
    show(jobsEmpty);
    return;
  }

  hide(jobsEmpty);

  jobs.forEach(
    job => {
      const article =
        document.createElement(
          "article"
        );

      article.className =
        "job-card";

      const status =
        job.status ||
        "completed";

      const statusLabel =
        status === "completed"
          ? "Completado"
          : status;

      article.innerHTML = `
        <div class="job-card-main">

          <span class="job-status">
            ${escapeHtml(
              statusLabel
            )}
          </span>

          <h3>
            ${escapeHtml(
              job.title
            )}
          </h3>

          ${
            job.description
              ? `
                <p>
                  ${escapeHtml(
                    job.description
                  )}
                </p>
              `
              : ""
          }

          ${
            job.completed_at
              ? `
                <small>
                  Finalizado el
                  ${formatDate(
                    job.completed_at
                  )}
                </small>
              `
              : ""
          }

        </div>

        <div class="job-card-actions">

          ${
            status === "completed"
              ? `
                <button
                  type="button"
                  class="button secondary-button review-token-button"
                  data-job-id="${job.id}"
                >
                  Generar valoración
                </button>

                <div
                  class="review-link-container hidden"
                  id="review-link-${job.id}"
                ></div>
              `
              : ""
          }

        </div>
      `;

      jobsList.appendChild(
        article
      );
    }
  );


  document
    .querySelectorAll(
      ".review-token-button"
    )
    .forEach(
      button => {
        button.addEventListener(
          "click",
          () =>
            generateReviewLink(
              button
            )
        );
      }
    );
}


/*
============================================================
GENERAR QR
============================================================

No dependemos de la variable global QRCode.

Esto evita que el panel falle si la librería
externa no se carga.

El QR se genera como imagen utilizando
la URL pública de valoración.
============================================================
*/

function createReviewQr(
  container,
  reviewUrl
) {
  const qrSection =
    document.createElement(
      "div"
    );

  qrSection.className =
    "review-qr-section";

  qrSection.innerHTML = `
    <span class="review-qr-label">
      También podés mostrar este QR a tu cliente
    </span>

    <img
      class="review-qr"
      alt="Código QR para valorar este trabajo"
    >

    <small class="review-qr-error hidden">
      No se pudo generar el código QR.
    </small>
  `;

  container
    .querySelector(
      ".review-link-box"
    )
    .appendChild(
      qrSection
    );

  const qrImage =
    qrSection.querySelector(
      ".review-qr"
    );

  const qrError =
    qrSection.querySelector(
      ".review-qr-error"
    );

  /*
  Generamos el QR a partir de la URL.
  */

  const qrUrl =
    `https://api.qrserver.com/v1/create-qr-code/?size=220x220&margin=10&data=${encodeURIComponent(reviewUrl)}`;

  qrImage.src = qrUrl;

  qrImage.addEventListener(
    "error",
    () => {
      qrImage.classList.add(
        "hidden"
      );

      qrError.classList.remove(
        "hidden"
      );
    }
  );
}


/*
============================================================
GENERAR ENLACE DE VALORACIÓN
============================================================
*/

async function generateReviewLink(
  button
) {
  const jobId =
    button.dataset.jobId;

  button.disabled = true;

  button.textContent =
    "Generando...";

  try {
    const response =
      await fetch(
        `${API_BASE_URL}/api/jobs/${jobId}/review-token`,
        {
          method: "POST",
          headers:
            getAuthHeaders(),
        }
      );

    const data =
      await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail ||
        "No se pudo generar el enlace de valoración."
      );
    }


    /*
    ========================================================
    TOKEN
    ========================================================
    */

    const token =
      data.review_token;

    if (!token) {
      throw new Error(
        "El backend no devolvió el token de valoración."
      );
    }


    /*
    ========================================================
    URL PÚBLICA
    ========================================================
    */

    const reviewUrl =
      new URL(
        `review.html?token=${encodeURIComponent(
          token
        )}`,
        window.location.href
      ).href;


    /*
    ========================================================
    CONTENEDOR
    ========================================================
    */

    const container =
      document.getElementById(
        `review-link-${jobId}`
      );

    if (!container) {
      throw new Error(
        "No se encontró el contenedor del enlace de valoración."
      );
    }


    /*
    ========================================================
    HTML DEL ENLACE
    ========================================================
    */

    container.innerHTML = `
      <div class="review-link-box">

        <strong>
          Enlace de valoración generado
        </strong>

        <p>
          Compartilo con tu cliente para que pueda valorar
          este trabajo.
        </p>

        <input
          type="text"
          value="${escapeHtml(
            reviewUrl
          )}"
          readonly
        >

        <button
          type="button"
          class="button primary-button copy-review-link"
          data-url="${escapeHtml(
            reviewUrl
          )}"
        >
          Copiar enlace
        </button>

        <a
          href="${escapeHtml(
            reviewUrl
          )}"
          target="_blank"
          rel="noopener noreferrer"
          class="review-preview-link"
        >
          Abrir valoración
        </a>

      </div>
    `;


    /*
    ========================================================
    MOSTRAR CONTENEDOR
    ========================================================
    */

    show(container);


    /*
    ========================================================
    QR
    ========================================================
    */

    createReviewQr(
      container,
      reviewUrl
    );


    /*
    ========================================================
    COPIAR ENLACE
    ========================================================
    */

    const copyButton =
      container.querySelector(
        ".copy-review-link"
      );

    copyButton.addEventListener(
      "click",
      async () => {
        try {
          await navigator.clipboard.writeText(
            reviewUrl
          );

          copyButton.textContent =
            "✓ Enlace copiado";

        } catch (error) {
          copyButton.textContent =
            "No se pudo copiar";

          console.error(
            error
          );
        }
      }
    );

  } catch (error) {
    console.error(error);

    alert(
      error.message
    );

  } finally {
    button.disabled = false;

    button.textContent =
      "Generar valoración";
  }
}


/*
============================================================
MOSTRAR FORMULARIO DE TRABAJO
============================================================
*/

function openNewJobForm() {
  show(newJobPanel);

  document
    .getElementById(
      "job-title"
    )
    .focus();
}


function closeNewJobForm() {
  hide(newJobPanel);

  newJobForm.reset();

  hide(jobFormMessage);
}


/*
============================================================
REGISTRAR TRABAJO
============================================================
*/

async function createJob(
  event
) {
  event.preventDefault();

  const formData =
    new FormData(
      newJobForm
    );

  const title =
    formData
      .get("title")
      ?.trim();

  const description =
    formData
      .get("description")
      ?.trim();

  if (!title) {
    return;
  }

  const submitButton =
    newJobForm.querySelector(
      'button[type="submit"]'
    );

  submitButton.disabled = true;

  submitButton.textContent =
    "Registrando...";

  hide(
    jobFormMessage
  );

  try {
    const response =
      await fetch(
        `${API_BASE_URL}/api/jobs`,
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",

            ...getAuthHeaders(),
          },

          body: JSON.stringify({
            title,

            description:
              description ||
              null,

            status:
              "completed",
          }),
        }
      );

    const data =
      await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail ||
        "No se pudo registrar el trabajo."
      );
    }

    show(
      jobFormMessage
    );

    jobFormMessage.className =
      "form-message success-message";

    jobFormMessage.textContent =
      "Trabajo registrado correctamente.";

    newJobForm.reset();

    await refreshJobs();

  } catch (error) {
    console.error(error);

    show(
      jobFormMessage
    );

    jobFormMessage.className =
      "form-message error-message";

    jobFormMessage.textContent =
      error.message;

  } finally {
    submitButton.disabled =
      false;

    submitButton.textContent =
      "Registrar trabajo";
  }
}


/*
============================================================
REFRESCAR TRABAJOS
============================================================
*/

async function refreshJobs() {
  const jobs =
    await loadJobs();

  renderJobs(
    jobs
  );
}


/*
============================================================
GUARDAR PERFIL
============================================================
*/

async function saveProfessionalProfile() {
  profileFormMessage.classList.add(
    "hidden"
  );

  profileFormMessage.textContent =
    "";

  const categoryIds =
    Array.from(
      profileCategories
        .selectedOptions
    )
      .map(
        option =>
          Number(option.value)
      );

  const locationIds =
    Array.from(
      profileLocations
        .selectedOptions
    )
      .map(
        option =>
          Number(option.value)
      );

  const payload = {
    description:
      profileDescription.value
        .trim() ||
      null,

    years_experience:
      profileYearsExperience.value === ""
        ? null
        : Number(
            profileYearsExperience.value
          ),

    whatsapp:
      profileWhatsapp.value
        .trim() ||
      null,

    instagram:
      profileInstagram.value
        .trim() ||
      null,

    category_ids:
      categoryIds,

    location_ids:
      locationIds,
  };


  try {
    const response =
      await fetch(
        `${API_BASE_URL}/api/professional/profile`,
        {
          method: "PATCH",

          headers: {
            ...getAuthHeaders(),

            "Content-Type":
              "application/json",
          },

          body:
            JSON.stringify(
              payload
            ),
        }
      );

    let data = null;

    try {
      data =
        await response.json();
    } catch {}


    if (!response.ok) {
      throw new Error(
        data?.detail ||
        `No se pudo guardar el perfil (${response.status})`
      );
    }


    renderProfessional(
      data
    );

    profileFormMessage.textContent =
      "Los cambios se guardaron correctamente.";

    profileFormMessage.classList.remove(
      "hidden"
    );

    profileEditForm.classList.add(
      "hidden"
    );

    editProfileButton.classList.remove(
      "hidden"
    );

  } catch (error) {
    console.error(error);

    profileFormMessage.textContent =
      error.message ||
      "No se pudieron guardar los cambios.";

    profileFormMessage.classList.remove(
      "hidden"
    );
  }
}


/*
============================================================
ABRIR EDICIÓN DE PERFIL
============================================================
*/

editProfileButton.addEventListener(
  "click",
  async () => {
    try {
      await loadProfileOptions();

      const professional =
        await loadProfessional();

      fillProfileForm(
        professional
      );

      profileEditForm.classList.remove(
        "hidden"
      );

      editProfileButton.classList.add(
        "hidden"
      );

      profileFormMessage.classList.add(
        "hidden"
      );

      profileFormMessage.textContent =
        "";

    } catch (error) {
      console.error(error);

      profileFormMessage.textContent =
        error.message ||
        "No se pudo abrir la edición del perfil.";

      profileFormMessage.classList.remove(
        "hidden"
      );
    }
  }
);


/*
============================================================
CANCELAR EDICIÓN
============================================================
*/

cancelProfileButton.addEventListener(
  "click",
  () => {
    profileEditForm.classList.add(
      "hidden"
    );

    editProfileButton.classList.remove(
      "hidden"
    );

    profileFormMessage.classList.add(
      "hidden"
    );

    profileFormMessage.textContent =
      "";
  }
);


/*
============================================================
SUBMIT PERFIL
============================================================
*/

profileEditForm.addEventListener(
  "submit",
  async event => {
    event.preventDefault();

    await saveProfessionalProfile();
  }
);


/*
============================================================
LOGOUT
============================================================
*/

logoutButton.addEventListener(
  "click",
  () => {
    sessionStorage.removeItem(
      PROFESSIONAL_TOKEN_STORAGE_KEY
    );

    window.location.replace(
      "professional-login.html"
    );
  }
);


/*
============================================================
INICIALIZACIÓN
============================================================
*/

async function init() {
  try {
    await loadAuthenticatedProfessional();


    /*
    ========================================================
    PERFIL PÚBLICO
    ========================================================
    */

    if (
      publicProfileLink &&
      professionalId
    ) {
      publicProfileLink.href =
        `./profile.html?id=${encodeURIComponent(
          professionalId
        )}`;
    }


    const professional =
      await loadProfessional();

    const jobs =
      await loadJobs();


    renderProfessional(
      professional
    );

    renderProfessionalReviews(
      professional.reviews
    );

    renderJobs(
      jobs
    );


    hide(
      loadingState
    );

    hide(
      errorState
    );

    show(
      professionalContent
    );

  } catch (error) {
    console.error(error);

    const hasToken =
      getProfessionalToken();

    if (!hasToken) {
      window.location.replace(
        "professional-login.html"
      );

      return;
    }

    hide(
      loadingState
    );

    show(
      errorState
    );

    errorMessage.textContent =
      error.message;
  }
}


/*
============================================================
EVENTOS
============================================================
*/

newJobButton.addEventListener(
  "click",
  openNewJobForm
);


cancelJobButton.addEventListener(
  "click",
  closeNewJobForm
);


newJobForm.addEventListener(
  "submit",
  createJob
);


/*
============================================================
START
============================================================
*/

init();