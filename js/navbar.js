import { filterParks, hideLandscapes } from "./main.js";

// HTML Elements.
const filterButtons = document.querySelectorAll("#navbar-desktop-filter-button, #navbar-mobile-filter-button");
const parkFilters = document.querySelectorAll(".navbar-parks-filter");
const navbar = document.getElementById("navbar");
const parkFiltersElement = document.getElementById("navbar-parks-filters");
const desktopFilterButton = document.getElementById("navbar-desktop-filter-button");
const navbarTitleElement = document.getElementById("navbar-title");
const navbarTitleSVG = document.getElementById("navbar-title-svg");
const navbarTitleTextSVG = document.querySelectorAll(".navbar-title-svg-text");

let navbarActiveTitleTextElement = null;

// Handles navbar setup.
export const navbarOnLoad = () => {
  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      hideLandscapes();
      navbarToggleDropdown();
    });
  });

  parkFilters.forEach((filter) => {
    filter.addEventListener("click", navbarFilterSelect);
  });

  navbar.addEventListener("mouseleave", () => {
    navbarToggleDropdown("close");
  });
  navbarScaleSVGText();
};

// Handles navbar resizing.
export const navbarOnResize = () => {
  navbarScaleSVGText();
  navbarToggleDropdown("close");
};

// Processes toggling the navbar filter dropdown.
export const navbarToggleDropdown = (action) => {
  if (action === "close") {
    parkFiltersElement.classList.add("hidden");
  } else if (action === "open") {
    parkFiltersElement.classList.remove("hidden");
  } else {
    parkFiltersElement.classList.toggle("hidden");
  }
};

// Handles selecting a park filter option.
const navbarFilterSelect = (event) => {
  const filterElement = event.currentTarget;
  document.querySelector(".filter-active").classList.remove("filter-active");
  filterElement.classList.add("filter-active");
  navbarToggleDropdown("close");
  filterParks(filterElement.id.replace("-filter", ""));
  desktopFilterButton.textContent = `${filterElement.textContent} ▾`;
};

// Handles scaling and selecting the navbar title text.
const navbarScaleSVGText = () => {
  let titleTextWidthDifference = Number.MAX_SAFE_INTEGER;
  let newTitleTextElement = null;
  const titleWidth = navbarTitleElement.offsetWidth;
  const svgWidth = titleWidth * (100 / navbarTitleElement.offsetHeight);
  navbarTitleSVG.setAttribute("viewBox", `0 0 ${svgWidth} 100`);
  navbarTitleTextSVG.forEach((textElement) => {
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
};
