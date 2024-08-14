import { filterParks, hideLandscapes } from "./main.js";

let navbarActiveTitleTextElement = null;

// Handles navbar setup.
export function navbarOnLoad() {
  document.getElementById("navbar-desktop-filter-button").addEventListener("click", function () {
    hideLandscapes();
    navbarToggleDropdown();
  });
  document.getElementById("navbar-mobile-filter-button").addEventListener("click", function () {
    hideLandscapes();
    navbarToggleDropdown();
  });
  document.querySelectorAll(".navbar-parks-filter").forEach((filterElement) => {
    filterElement.addEventListener("click", (event) => {
      navbarFilterSelect(event);
    });
  });
  document.getElementById("navbar").addEventListener("mouseleave", () => {
    navbarToggleDropdown("close");
  });
  navbarScaleSVGText();
}

// Handles navbar resizing.
export function navbarOnResize() {
  navbarScaleSVGText();
  navbarToggleDropdown("close");
}

// Processes toggling the navbar filter dropdown.
export function navbarToggleDropdown(action) {
  let parkFiltersElement = document.getElementById("navbar-parks-filters");
  if (action === "close") {
    parkFiltersElement.classList.add("hidden");
  } else if (action === "open") {
    parkFiltersElement.classList.remove("hidden");
  } else {
    parkFiltersElement.classList.toggle("hidden");
  }
}

// Handles selecting a park filter option.
function navbarFilterSelect(event) {
  let filterElement = event.currentTarget;
  document.querySelector(".filter-active").classList.remove("filter-active");
  filterElement.classList.add("filter-active");
  navbarToggleDropdown("close");
  filterParks(filterElement.id.replace("-filter", ""));
  document.getElementById("navbar-desktop-filter-button").textContent = filterElement.textContent + " ▾";
}

// Handles scaling and selecting the navbar title text.
function navbarScaleSVGText() {
  let titleTextWidthDifference = Number.MAX_SAFE_INTEGER;
  let newTitleTextElement = null;
  let navbarTitleElement = document.getElementById("navbar-title");
  let titleWidth = navbarTitleElement.offsetWidth;
  let svgWidth = titleWidth * (100 / navbarTitleElement.offsetHeight);
  document.getElementById("navbar-title-svg").setAttribute("viewBox", "0 0 " + svgWidth + " " + 100);
  document.querySelectorAll(".navbar-title-svg-text").forEach((textElement) => {
    let textWidth = Math.ceil(textElement.getBoundingClientRect().width);
    if (textWidth < titleWidth && titleWidth - textWidth < titleTextWidthDifference) {
      newTitleTextElement = textElement;
      titleTextWidthDifference = titleWidth - textWidth;
    }
  });
  if (newTitleTextElement !== navbarActiveTitleTextElement) {
    if (navbarActiveTitleTextElement !== null) {
      navbarActiveTitleTextElement.classList.add("invisible");
    }
    if (newTitleTextElement !== null) {
      newTitleTextElement.classList.remove("invisible");
    }
    navbarActiveTitleTextElement = newTitleTextElement;
  }
}
