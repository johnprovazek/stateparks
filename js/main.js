import { createElement } from "./util.js";
import { navbarOnLoad, navbarOnResize, navbarToggleDropdown } from "./navbar.js";

var activeSignContainerId = null; // Active sign container ID. Used to show and hide park icons.
var maxSignWidth = 250; // Max park sign width for Google Photos.

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
  if (type === "all") {
    type = "sign-container";
  }
  document.querySelectorAll("." + type).forEach((sign) => {
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
  var signWidth = parseInt(window.screen.width * 0.2); // Park sign width.
  if (signWidth < 120) {
    signWidth = 120;
  } else if (signWidth > 120) {
    if (signWidth > 250) {
      signWidth = 250;
    }
    maxSignWidth = Math.floor(signWidth * 1.5);
  }
  document.querySelector(":root").style.setProperty("--sign-width", signWidth + "px");
  let signsContainerElement = document.querySelector("#signs-container");
  signsContainerElement.classList.remove("hidden");
  signsContainerElement.classList.add("grid");
}

// Loads park sign and landscape photos.
function photoLoadManager() {
  // Setting up loading bar for park sign photos.
  let loadingBar = document.getElementById("navbar-loading-fill");
  loadingBar.className = "green-background";
  loadingBar.style.width = "0%";
  // Load park sign photos. Once park sign photos are complete landscape photos are loaded next.
  let signContainers = document.querySelectorAll(".sign-container");
  let signCount = 0;
  signContainers.forEach((signContainer) => {
    const loadImage = new Image();
    loadImage.onload = () => {
      signImageElement.src = loadImage.src;
      let overlayImage = signContainer.querySelector(".park-sign-overlay");
      signCount = processImage(signCount, signContainers.length, loadingBar, overlayImage);
      if (signCount === signContainers.length) {
        landscapePhotosLoad(); // Load landscape photos after park sign photos are complete.
      }
    };
    loadImage.onerror = () => {
      let overlayImage = signContainer.querySelector(".park-sign-overlay");
      signCount = processImage(signCount, signContainers.length, loadingBar, overlayImage);
      signImageElement.src = "images/loading/broken-sign.svg";
      if (overlayImage === null) {
        let failOverlayImageSrc = "images/overlay/" + signContainer.id + ".svg";
        let failOverlayImageAlt = signImageElement.alt.replace("Photo", "Overlay");
        let failOverlayImage = createElement(`
          <img class="park-sign-overlay" src=${failOverlayImageSrc} alt="${failOverlayImageAlt}">
        `);
        signContainer.appendChild(failOverlayImage);
      }
      if (signCount === signContainers.length) {
        landscapePhotosLoad(); // Load landscape photos after park sign photos are complete.
      }
    };
    let signImageElement = signContainer.querySelector(".park-sign");
    let newImageSrc = signImageElement.getAttribute("data-src");
    if (newImageSrc.slice(-3) != "svg") {
      newImageSrc = newImageSrc + "=w" + maxSignWidth;
    }
    loadImage.src = newImageSrc;
  });
}

// Loads all landscape photos.
function landscapePhotosLoad() {
  // Setting up loading bar for landscape photos.
  let loadingBar = document.getElementById("navbar-loading-fill");
  loadingBar.className = "blue-background";
  loadingBar.style.width = "0%";
  // Load landscape photos.
  let landscapeImages = document.querySelectorAll(".landscape-latent");
  let landscapeCount = 0;
  landscapeImages.forEach((landscapeImage) => {
    const loadImage = new Image();
    loadImage.onload = () => {
      landscapeImage.src = loadImage.src;
      landscapeCount = processImage(landscapeCount, landscapeImages.length, loadingBar, null);
      landscapeImage.setAttribute("data-load", "true");
      if (landscapeImage.parentElement.querySelectorAll("[data-load='true']").length === 3) {
        let galleryIconContainer = landscapeImage.parentElement.parentElement.querySelector(".gallery-icon-container");
        galleryIconContainer.classList.remove("icon-loading");
        galleryIconContainer.querySelector(".sign-icon").src = "images/icon/landscape-button.svg";
      }
      if (landscapeCount === landscapeImages.length) {
        loadingBar.className = "brown-background";
      }
    };
    loadImage.onerror = () => {
      console.log("Error on landscape image: " + loadImage.src);
      landscapeCount = processImage(landscapeCount, landscapeImages.length, loadingBar, null);
      let galleryIconContainer = landscapeImage.parentElement.parentElement.querySelector(".gallery-icon-container");
      galleryIconContainer.querySelector(".sign-icon").src = "images/icon/landscape-button-broken.svg";
      if (landscapeCount === landscapeImages.length) {
        loadingBar.className = "brown-background";
      }
      landscapeImage.src = "images/loading/broken-landscape.svg";
    };
    let newImageSrc = landscapeImage.getAttribute("data-src") + "=w900";
    loadImage.src = newImageSrc;
  });
}

// Handles common processes when adding a new park sign photo or landscape photo.
function processImage(imageCount, totalImages, loadingBar, overlayElement) {
  if (overlayElement) {
    overlayElement.classList.remove("hidden");
  }
  imageCount = imageCount + 1;
  let percentLoaded = parseFloat(loadingBar.style.width);
  let percentLoadedNew = ((imageCount / totalImages) * 100).toFixed(2);
  if (percentLoadedNew > percentLoaded) {
    loadingBar.style.width = percentLoadedNew + "%";
  } else {
    console.log("lock issue - processImage");
  }
  return imageCount;
}

// Handles clicking on a sign container.
function handleSignClick(event) {
  let signContainerElement = event.target;
  if (signContainerElement.classList.contains("sign-container")) {
    let id = signContainerElement.id;
    let curActiveSignContainerId = activeSignContainerId;
    removeIcons();
    if (curActiveSignContainerId !== id) {
      let iconContainers = signContainerElement.querySelectorAll(".sign-icon-container");
      iconContainers.forEach((iconContainer) => {
        iconContainer.classList.remove("invisible");
      });
      activeSignContainerId = id;
    }
  }
}

// Hides all visible icons.
function removeIcons() {
  document.querySelectorAll(".sign-icon-container:not(.invisible)").forEach((visibleIconContainer) => {
    visibleIconContainer.classList.add("invisible");
  });
  activeSignContainerId = null;
}

// Handles mousing over signs container. Used to remove icons when mousing out of the active area.
function handleSignsContainerMouseMove(event) {
  if (activeSignContainerId) {
    let box = document.getElementById(activeSignContainerId).getBoundingClientRect();
    let offset = 0.25 * box.width;
    let right = box.right + offset;
    let left = box.left - offset;
    let top = box.top - offset;
    let bottom = box.bottom + offset;
    let x = event.clientX;
    let y = event.clientY;
    if (x < left || x > right || y < top || y > bottom) {
      removeIcons();
    }
  }
}

// Shows landscape photos.
function showLandscapes(event) {
  let iconContainerElement = event.target.parentElement;
  if (!iconContainerElement.classList.contains("icon-loading")) {
    let signContainerElement = iconContainerElement.parentElement;
    document.getElementById("landscape-1").src = signContainerElement.querySelector(".landscape-latent-1").src;
    document.getElementById("landscape-2").src = signContainerElement.querySelector(".landscape-latent-2").src;
    document.getElementById("landscape-3").src = signContainerElement.querySelector(".landscape-latent-3").src;
    document.body.classList.add("no-scroll");
    document.getElementById("landscape-container").classList.remove("hidden");
  }
}
