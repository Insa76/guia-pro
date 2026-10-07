const API_BASE_URL = "https://guia-pro.onrender.com";

const searchForm = document.getElementById("search-form");

const queryInput = document.getElementById("query");
const locationInput = document.getElementById("location");

const resultsHeader = document.getElementById("results-header");
const resultsTitle = document.getElementById("results-title");
const resultsCount = document.getElementById("results-count");

const resultsContainer = document.getElementById("results");

const loadingState = document.getElementById("loading");
const errorState = document.getElementById("error");
const emptyState = document.getElementById("empty");


function setState({
    loading = false,
    error = false,
    empty = false,
} = {}) {
    loadingState.classList.toggle(
        "hidden",
        !loading
    );

    errorState.classList.toggle(
        "hidden",
        !error
    );

    emptyState.classList.toggle(
        "hidden",
        !empty
    );
}

async function loadSearchOptions() {

    const [
        categoriesResponse,
        locationsResponse
    ] = await Promise.all([
        fetch(`${API_BASE_URL}/api/categories`),
        fetch(`${API_BASE_URL}/api/locations`)
    ]);


    const categories =
        await categoriesResponse.json();

    const locations =
        await locationsResponse.json();


    queryInput.innerHTML = `
        <option value="">
            Seleccioná un oficio
        </option>
    `;


    categories.forEach(category => {

        const option =
            document.createElement("option");

        option.value =
            category.slug;

        option.textContent =
            category.name;

        queryInput.appendChild(option);

    });



    locationInput.innerHTML = `
        <option value="">
            Seleccioná una zona
        </option>
    `;


    locations.forEach(location => {

        const option =
            document.createElement("option");

        option.value =
            location.name;

        option.textContent =
            `${location.name}, ${location.province}`;

        locationInput.appendChild(option);

    });


    locationInput.value =
        "Resistencia";
}


function getInitials(firstName, lastName) {
    const first =
        firstName?.trim()?.charAt(0) || "";

    const last =
        lastName?.trim()?.charAt(0) || "";

    return `${first}${last}`.toUpperCase();
}


function createProfessionalCard(professional) {
    const card =
        document.createElement("article");

    card.className =
        "professional-card";

    const verifiedMarkup =
        professional.identity_verified
            ? `
                <span class="verified">
                    ✓ Identidad verificada
                </span>
            `
            : "";

    const ratingMarkup =
        professional.total_reviews > 0
            ? `
                <div class="rating">
                    <span class="rating-star">★</span>

                    <span>
                        ${professional.average_rating.toFixed(1)}
                    </span>

                    <span class="rating-meta">
                        (${professional.total_reviews})
                    </span>
                </div>
            `
            : `
                <div class="rating">
                    <span class="rating-meta">
                        Sin reseñas todavía
                    </span>
                </div>
            `;

    const experienceMarkup =
        professional.years_experience !== null
            ? `
                <span class="experience">
                    ${professional.years_experience}
                    años de experiencia
                </span>
            `
            : "";

    card.innerHTML = `
        <div class="card-top">

            <div class="avatar">
                ${getInitials(
                    professional.first_name,
                    professional.last_name
                )}
            </div>

            ${verifiedMarkup}

        </div>


        <h3>
            ${professional.first_name}
            ${professional.last_name}
        </h3>


        <p class="profession">
            ${professional.category_name}
        </p>


        <p class="location">
            ${professional.location_name}
        </p>


        ${
            professional.description
                ? `
                    <p class="description">
                        ${professional.description}
                    </p>
                `
                : ""
        }


        <div class="card-footer">

    <div>
        ${ratingMarkup}

        ${experienceMarkup}
    </div>

    <a
        class="profile-link"
        href="./profile.html?id=${professional.id}"
    >
        Ver perfil →
    </a>

</div>
    `;

    return card;
}


async function searchProfessionals({
    query,
    location,
}) {
    const params =
        new URLSearchParams();

    if (query) {
    params.set("category", query.toLowerCase());
}

    if (location) {
        params.set("location", location);
    }

    const url =
    `${API_BASE_URL}/api/search/professionals?${params.toString()}`;

    const response =
        await fetch(url);

    if (!response.ok) {
        throw new Error(
            "No se pudo realizar la búsqueda."
        );
    }

    return response.json();
}


function renderResults(
    professionals,
    query,
    location
) {
    resultsContainer.innerHTML = "";

    resultsHeader.classList.remove(
        "hidden"
    );

    resultsCount.textContent =
        `${professionals.length} ${
            professionals.length === 1
                ? "profesional"
                : "profesionales"
        }`;

    if (query) {
        resultsTitle.textContent =
            `Resultados para "${query}"`;
    } else {
        resultsTitle.textContent =
            `Profesionales en ${location || "tu zona"}`;
    }

    if (professionals.length === 0) {
        setState({
            empty: true,
        });

        return;
    }

    setState();

    const fragment =
        document.createDocumentFragment();

    professionals.forEach(
        (professional) => {
            fragment.appendChild(
                createProfessionalCard(
                    professional
                )
            );
        }
    );

    resultsContainer.appendChild(
        fragment
    );
}


searchForm.addEventListener(
    "submit",
    async (event) => {
        event.preventDefault();

        const query =
            queryInput.value.trim();

        const location =
            locationInput.value.trim();

        resultsContainer.innerHTML = "";

        resultsHeader.classList.add(
            "hidden"
        );

        errorState.textContent = "";

        setState({
            loading: true,
        });

        try {
            const professionals =
                await searchProfessionals({
                    query,
                    location,
                });

            renderResults(
                professionals,
                query,
                location
            );

        } catch (error) {
            console.error(error);

            setState({
                error: true,
            });

            errorState.textContent =
                error.message ||
                "Ocurrió un error al buscar profesionales.";

        } finally {
            loadingState.classList.add(
                "hidden"
            );
        }
    }
);

loadSearchOptions();