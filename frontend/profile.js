const API_BASE_URL = "https://guia-pro.onrender.com";

const loadingElement = document.getElementById("loading");
const errorElement = document.getElementById("error");
const profileElement = document.getElementById("profile");

const profileAvatar = document.getElementById("profile-avatar");
const profileName = document.getElementById("profile-name");
const profileProfession = document.getElementById("profile-profession");
const profileLocation = document.getElementById("profile-location");
const profileVerified = document.getElementById("profile-verified");

const profileDescription = document.getElementById("profile-description");
const profileExperience = document.getElementById("profile-experience");

const profileRating = document.getElementById("profile-rating");
const profileReviewCount = document.getElementById("profile-review-count");
const profileJobs = document.getElementById("profile-jobs");
const profileRatedJobs = document.getElementById("profile-rated-jobs");

const profileCategories = document.getElementById("profile-categories");
const profileLocations = document.getElementById("profile-locations");

const reviewsSection = document.getElementById("reviews-section");
const reviewsList = document.getElementById("reviews-list");

const contactActions = document.getElementById(
    "profile-contact-actions"
);


function showLoading() {
    loadingElement.classList.remove("hidden");
    errorElement.classList.add("hidden");
    profileElement.classList.add("hidden");
}


function showError(message) {
    loadingElement.classList.add("hidden");
    profileElement.classList.add("hidden");

    errorElement.textContent = message;
    errorElement.classList.remove("hidden");
}


function showProfile() {
    loadingElement.classList.add("hidden");
    errorElement.classList.add("hidden");
    profileElement.classList.remove("hidden");
}


function getProfessionalId() {
    const params = new URLSearchParams(window.location.search);

    return params.get("id");
}


function getInitials(firstName, lastName) {
    const first = firstName?.trim()?.charAt(0) || "";
    const last = lastName?.trim()?.charAt(0) || "";

    return `${first}${last}`.toUpperCase();
}


function formatRating(rating) {
    return Number(rating || 0).toFixed(1);
}


function renderStars(rating) {
    const value = Math.round(Number(rating || 0));

    return "★".repeat(value) + "☆".repeat(5 - value);
}


function formatDate(dateString) {
    if (!dateString) {
        return "";
    }

    const date = new Date(dateString);

    if (Number.isNaN(date.getTime())) {
        return "";
    }

    return new Intl.DateTimeFormat("es-AR", {
        day: "2-digit",
        month: "long",
        year: "numeric",
    }).format(date);
}


function renderCategories(categories) {
    profileCategories.innerHTML = "";

    if (!categories || categories.length === 0) {
        return;
    }

    categories.forEach((category) => {
        const tag = document.createElement("span");

        tag.className = "profile-tag";
        tag.textContent = category.name;

        profileCategories.appendChild(tag);
    });
}


function renderLocations(locations) {
    profileLocations.innerHTML = "";

    if (!locations || locations.length === 0) {
        return;
    }

    locations.forEach((location) => {
        const tag = document.createElement("span");

        tag.className = "profile-tag profile-tag-location";
        tag.textContent =
            `${location.locality}, ${location.province}`;

        profileLocations.appendChild(tag);
    });
}


function renderReviews(reviews) {
    reviewsList.innerHTML = "";

    if (!reviews || reviews.length === 0) {
        reviewsList.innerHTML = `
            <div class="reviews-empty">
                Todavía no hay opiniones de clientes.
            </div>
        `;

        return;
    }

    reviews.forEach((review) => {

        const reviewElement = document.createElement("article");

        reviewElement.className = "review-item";

        const comment = review.comment
            ? escapeHtml(review.comment)
            : "El cliente no dejó un comentario.";

        const date = formatDate(review.created_at);

        reviewElement.innerHTML = `
            <div class="review-top">
                <span class="review-stars">
                    ${renderStars(review.rating)}
                </span>

                <span class="review-rating">
                    ${review.rating}/5
                </span>
            </div>

            <p class="review-comment">
                ${comment}
            </p>

            ${
                date
                    ? `<span class="review-date">${date}</span>`
                    : ""
            }
        `;

        reviewsList.appendChild(reviewElement);
    });
}


function renderContactActions(profile) {

    contactActions.innerHTML = "";

    if (profile.whatsapp) {

        const whatsappNumber = profile.whatsapp
            .replace(/\D/g, "");

        const whatsappUrl =
            `https://wa.me/${whatsappNumber}`;

        const whatsappButton =
            document.createElement("a");

        whatsappButton.href = whatsappUrl;
        whatsappButton.target = "_blank";
        whatsappButton.rel = "noopener noreferrer";
        whatsappButton.className = "contact-button primary";
        whatsappButton.textContent = "Contactar por WhatsApp";

        contactActions.appendChild(whatsappButton);
    }


    if (profile.instagram) {

        const instagramHandle =
            profile.instagram
                .replace(/^@/, "")
                .trim();

        const instagramUrl =
            `https://instagram.com/${instagramHandle}`;

        const instagramButton =
            document.createElement("a");

        instagramButton.href = instagramUrl;
        instagramButton.target = "_blank";
        instagramButton.rel = "noopener noreferrer";
        instagramButton.className = "contact-button secondary";

        instagramButton.textContent =
            `Instagram ${profile.instagram}`;

        contactActions.appendChild(instagramButton);
    }


    if (contactActions.children.length === 0) {

        contactActions.innerHTML = `
            <span class="contact-unavailable">
                El profesional todavía no publicó
                un medio de contacto.
            </span>
        `;
    }
}


function renderProfile(profile) {

    const fullName =
        `${profile.first_name} ${profile.last_name}`;

    profileName.textContent = fullName;

    profileAvatar.textContent =
        getInitials(
            profile.first_name,
            profile.last_name
        );

    const primaryCategory =
        profile.categories?.[0];

    profileProfession.textContent =
        primaryCategory?.name || "Profesional";

    const primaryLocation =
        profile.locations?.[0];

    if (primaryLocation) {

        profileLocation.textContent =
            `${primaryLocation.locality}, ${primaryLocation.province}`;

    } else {

        profileLocation.textContent = "";
    }


    if (profile.identity_verified) {

        profileVerified.classList.remove("hidden");

    } else {

        profileVerified.classList.add("hidden");
    }


    profileDescription.textContent =
        profile.description ||
        "Este profesional todavía no agregó una descripción.";


    if (profile.years_experience !== null &&
        profile.years_experience !== undefined) {

        profileExperience.textContent =
            `${profile.years_experience} años de experiencia`;

    } else {

        profileExperience.textContent = "";
    }


    profileRating.textContent =
        formatRating(profile.average_rating);

    profileReviewCount.textContent =
        profile.total_reviews === 1
            ? "1 opinión de cliente"
            : `${profile.total_reviews} opiniones de clientes`;


    profileJobs.textContent =
        profile.total_jobs;

    profileRatedJobs.textContent =
        profile.rated_jobs;


    renderCategories(profile.categories);

    renderLocations(profile.locations);

    renderReviews(profile.reviews);

    renderContactActions(profile);


    document.title =
        `${fullName} — Guia Pro`;
}


function escapeHtml(value) {

    return value
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


async function loadProfile() {

    const professionalId =
        getProfessionalId();

    if (!professionalId) {

        showError(
            "No se indicó qué perfil profesional mostrar."
        );

        return;
    }


    showLoading();

    try {

        const response = await fetch(
            `${API_BASE_URL}/api/public/professionals/${professionalId}/profile`
        );


        if (!response.ok) {

            if (response.status === 404) {

                throw new Error(
                    "No encontramos este perfil profesional."
                );
            }

            throw new Error(
                "No se pudo cargar el perfil profesional."
            );
        }


        const profile =
            await response.json();

        renderProfile(profile);

        showProfile();

    } catch (error) {

        console.error(
            "[Guia Pro] Error cargando perfil:",
            error
        );

        showError(
            error.message ||
            "Ocurrió un error al cargar el perfil."
        );
    }
}


loadProfile();