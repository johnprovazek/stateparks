import { createElement } from "./util.js";
import { navbarOnLoad, navbarOnResize, navbarToggleDropdown } from "./navbar.js";

const SIGN_WIDTH_PCT = 0.2; // Ideal sign width as a percentage of screen width.
const MIN_SIGN_WIDTH = 120; // Minimum sign width.
const MAX_SIGN_PCT = 1.5; // Percentage of sign width the sign is allowed to expand.
const SIGN_MOUSE_ALLOWANCE_PCT = 0.25; // Percentage of sign width mouse is allowed to travel.
const LANDSCAPE_IMAGE_COUNT = 3; // Total count of landscape images.

let activeSignContainerId = null; // Active sign container ID. Used to show and hide park icons.
let maxSignWidth = 250; // Max park sign width for Google Photos.

// Handles page setup.
window.onload = () => {
  navbarOnLoad(); // Handles navbar setup (js/navbar.js).
  displaySignsContainer(); // Calculates park sign widths then displays park signs.
  photoLoadManager(); // Loads park sign and landscape photos.
  document.querySelectorAll(".sign-container").forEach((signContainer) => {
    signContainer.addEventListener("click", (event) => {
      navbarToggleDropdown("close");
      handleSignClick(event);
    });
  });
  document.getElementById("signs-container").addEventListener("mousemove", (event) => {
    handleSignsContainerMouseMove(event);
  });
  document.getElementById("signs-container").addEventListener("mouseleave", () => {
    if (activeSignContainerId) {
      removeIcons();
    }
  });
  document.querySelectorAll(".gallery-icon-container").forEach((galleryIconContainer) => {
    galleryIconContainer.addEventListener("click", (event) => {
      showLandscapes(event);
    });
  });
  document.querySelectorAll(".landscape-exit-button").forEach((exitButton) => {
    exitButton.addEventListener("click", () => {
      hideLandscapes();
    });
  });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      hideLandscapes();
    }
  });
};

// Handles page resizing.
window.onresize = () => {
  navbarOnResize(); // Handles navbar resizing (js/navbar.js).
};

// Filters the type of park signs shown.
export function filterParks(type) {
  // Hide all visible park signs.
  document.querySelectorAll(".sign-container").forEach((sign) => {
    sign.classList.add("hidden");
  });
  // Show filtered park signs.
  const targetType = type === "all" ? "sign-container" : type;
  document.querySelectorAll(`.${targetType}`).forEach((sign) => {
    sign.classList.remove("hidden");
  });
}

// Hides landscape photos.
export function hideLandscapes() {
  document.body.classList.remove("no-scroll");
  document.getElementById("landscape-container").classList.add("hidden");
}

// Calculates park sign widths then displays park signs.
function displaySignsContainer() {
  let signWidth = parseInt(window.screen.width * SIGN_WIDTH_PCT); // Park sign width.
  signWidth = Math.max(MIN_SIGN_WIDTH, Math.min(signWidth, maxSignWidth));
  maxSignWidth = Math.floor(signWidth * MAX_SIGN_PCT);
  document.querySelector(":root").style.setProperty("--sign-width", `${signWidth}px`);
  const signsContainerElement = document.querySelector("#signs-container");
  signsContainerElement.classList.remove("hidden");
  signsContainerElement.classList.add("grid");
}

// Handles common processes when adding a new park sign photo or landscape photo.
function processImage(imageCount, totalImages, loadingBar) {
  const newImageCount = imageCount + 1;
  const percentLoaded = parseFloat(loadingBar.style.width);
  const percentLoadedNew = ((newImageCount / totalImages) * 100).toFixed(2);
  if (percentLoadedNew > percentLoaded) {
    loadingBar.style.width = `${percentLoadedNew}%`;
  } else {
    console.error("lock issue - processImage");
  }
  return newImageCount;
}

// Loads park sign and landscape photos.
function photoLoadManager() {
  // Setting up loading bar for park sign photos.
  const loadingBar = document.getElementById("navbar-loading-fill");
  loadingBar.className = "green-background";
  loadingBar.style.width = "0%";
  // Load park sign photos. Once park sign photos are complete landscape photos are loaded next.
  const signContainers = document.querySelectorAll(".sign-container");
  let signCount = 0;
  signContainers.forEach((signContainer) => {
    const loadImage = new Image();
    loadImage.onload = () => {
      signImageElement.src = loadImage.src;
      const overlayImage = signContainer.querySelector(".park-sign-overlay");
      if (overlayImage) {
        overlayImage.classList.remove("hidden");
      }
      signCount = processImage(signCount, signContainers.length, loadingBar);
      if (signCount === signContainers.length) {
        landscapePhotosLoad(); // Load landscape photos after park sign photos are complete.
      }
    };
    loadImage.onerror = () => {
      const overlayImage = signContainer.querySelector(".park-sign-overlay");
      if (overlayImage) {
        overlayImage.classList.remove("hidden");
      }
      signCount = processImage(signCount, signContainers.length, loadingBar);
      signImageElement.src = "images/loading/broken-sign.svg";
      if (overlayImage === null) {
        const failOverlayImageSrc = `images/overlay/${signContainer.id}.svg`;
        const failOverlayImageAlt = signImageElement.alt.replace("Photo", "Overlay");
        const failOverlayImage = createElement(`
          <img class="park-sign-overlay" src=${failOverlayImageSrc} alt="${failOverlayImageAlt}">
        `);
        signContainer.appendChild(failOverlayImage);
      }
      if (signCount === signContainers.length) {
        landscapePhotosLoad(); // Load landscape photos after park sign photos are complete.
      }
    };
    const signImageElement = signContainer.querySelector(".park-sign");
    let newImageSrc = signImageElement.getAttribute("data-src");
    if (!newImageSrc.toLowerCase().endsWith(".svg")) {
      newImageSrc += `=w${maxSignWidth}`;
    }
    loadImage.src = newImageSrc;
  });
}

// Loads all landscape photos.
function landscapePhotosLoad() {
  // Setting up loading bar for landscape photos.
  const loadingBar = document.getElementById("navbar-loading-fill");
  loadingBar.className = "blue-background";
  loadingBar.style.width = "0%";
  // Load landscape photos.
  const landscapeImages = document.querySelectorAll(".landscape-latent");
  let landscapeCount = 0;
  landscapeImages.forEach((landscapeImage) => {
    const loadImage = new Image();
    loadImage.onload = () => {
      landscapeImage.src = loadImage.src;
      landscapeCount = processImage(landscapeCount, landscapeImages.length, loadingBar);
      landscapeImage.setAttribute("data-load", "true");
      if (landscapeImage.parentElement.querySelectorAll("[data-load='true']").length === 3) {
        const galleryIconContainer =
          landscapeImage.parentElement.parentElement.querySelector(".gallery-icon-container");
        galleryIconContainer.classList.remove("icon-loading");
        galleryIconContainer.querySelector(".sign-icon").src = "images/icon/landscape-button.svg";
      }
      if (landscapeCount === landscapeImages.length) {
        loadingBar.className = "brown-background";
      }
    };
    loadImage.onerror = () => {
      console.error("Error on landscape image: ", loadImage.src);
      landscapeCount = processImage(landscapeCount, landscapeImages.length, loadingBar);
      const galleryIconContainer = landscapeImage.parentElement.parentElement.querySelector(".gallery-icon-container");
      galleryIconContainer.querySelector(".sign-icon").src = "images/icon/landscape-button-broken.svg";
      if (landscapeCount === landscapeImages.length) {
        loadingBar.className = "brown-background";
      }
      landscapeImage.src = "images/loading/broken-landscape.svg";
    };
    const newImageSrc = `${landscapeImage.getAttribute("data-src")}=w900`;
    loadImage.src = newImageSrc;
  });
}

// Handles clicking on a sign container.
function handleSignClick(event) {
  const signContainerElement = event.target;
  if (signContainerElement.classList.contains("sign-container")) {
    const id = signContainerElement.id;
    removeIcons();
    if (activeSignContainerId !== id) {
      const iconContainers = signContainerElement.querySelectorAll(".sign-icon-container");
      iconContainers.forEach((iconContainer) => {
        iconContainer.classList.remove("invisible");
      });
      activeSignContainerId = id;
    }
  }
}

// Hides all visible icons.
function removeIcons() {
  const visibleIcons = document.querySelectorAll(".sign-icon-container:not(.invisible)");
  visibleIcons.forEach((visibleIconContainer) => {
    visibleIconContainer.classList.add("invisible");
  });
  activeSignContainerId = null;
}

// Handles mousing over signs container. Used to remove icons when mousing out of the active area.
function handleSignsContainerMouseMove(event) {
  if (activeSignContainerId) {
    const box = document.getElementById(activeSignContainerId).getBoundingClientRect();
    const offset = box.width * SIGN_MOUSE_ALLOWANCE_PCT;
    const right = box.right + offset;
    const left = box.left - offset;
    const top = box.top - offset;
    const bottom = box.bottom + offset;
    const x = event.clientX;
    const y = event.clientY;
    if (x < left || x > right || y < top || y > bottom) {
      removeIcons();
    }
  }
}

// Shows landscape photos.
function showLandscapes(event) {
  const iconContainerElement = event.target.parentElement;
  if (!iconContainerElement.classList.contains("icon-loading")) {
    const signContainerElement = iconContainerElement.parentElement;
    for (let i = 0; i < LANDSCAPE_IMAGE_COUNT; i++) {
      document.getElementById(`landscape-${i + 1}`).src = signContainerElement.querySelector(
        `.landscape-latent-${i + 1}`
      ).src;
    }
    document.body.classList.add("no-scroll");
    document.getElementById("landscape-container").classList.remove("hidden");
  }
}
