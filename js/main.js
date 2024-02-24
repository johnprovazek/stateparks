var activeSignContainerId = null; // Active sign-container Id. Used to show/hide the park icons.

window.onload = function() {
  navbarOnLoad(); // Handles navbar variables and setup on mobile (js/navbar.js).
  photoLoadManager(); // Loads park sign and landscape images.
  let signContainers = document.querySelectorAll('.sign-container');
  for(let i = 0; i < signContainers.length; i++) {
    signContainers[i].onclick = function(event) {
      handleSignClick(event);
    };
  }
  document.getElementById('signs-container').onmousemove = function(event) {
    handleSignsContainerMouseMove(event)
  };
  document.getElementById('signs-container').onmouseleave = function() {
    removeIcons();
  }
  // Setting onclick function for all landscape buttons.
  let galleryIcons = document.querySelectorAll('.gallery-icon-visited');
  for(let i = 0; i < galleryIcons.length; i++) {
    galleryIcons[i].onclick = function() {
      showLandscapes(galleryIcons[i].parentElement.parentElement);
    };
  }
};

window.onresize = function() {
  navbarOnResize();
}

// Loads park sign images.
function photoLoadManager(){
  // Setting up loading bar.
  let loadingBar = document.getElementById('photos-loading-bar-fill');
  loadingBar.className = 'green-background';
  loadingBar.style.width = '0%';
  let signContainers = document.querySelectorAll('.sign-container');
  let signCount = 0;
  for (let i = 0; i < signContainers.length; i++) {
    const loadImage = new Image();
    loadImage.onload = function(){
      signContainers[i].querySelector('.park-sign').src = loadImage.src;
      let overlayElement = signContainers[i].querySelector('.hidden-overlay');
      if(overlayElement){
        overlayElement.classList.remove('hidden-overlay');
      }
      signCount = signCount + 1;
      let percentLoaded = parseFloat(loadingBar.style.width);
      let percentLoadedNew = ((signCount/signContainers.length) * 100).toFixed(2);
      if (percentLoadedNew > percentLoaded) {
        loadingBar.style.width = percentLoadedNew + '%';
      }
      if(signCount === signContainers.length){
        landscapePhotosLoad();
      }
    }
    loadImage.onerror = function(){
      console.log('Error on sign image: ' + newSrc);
      signCount = signCount + 1;
      let percentLoaded = parseFloat(loadingBar.style.width);
      let percentLoadedNew = ((signCount/signContainers.length) * 100).toFixed(2);
      if (percentLoadedNew > percentLoaded) {
        loadingBar.style.width = percentLoadedNew + '%';
      }
      if(signCount === signContainers.length){
        landscapePhotosLoad();
      }
      let overlayElement = signContainers[i].querySelector('.hidden-overlay');
      if(overlayElement){
        overlayElement.classList.remove('hidden-overlay');
        overlayElement.classList.add('image-load-fail-overlay');
      }
      else{
        let failOverlayImg = document.createElement('img');
        failOverlayImg.src = 'img/overlay/' + signContainers[i].id + '.svg';
        failOverlayImg.alt = signContainers[i].querySelector('.park-sign').alt.replace('Photo', 'Overlay');
        failOverlayImg.classList.add('park-sign-overlay', 'image-load-fail-overlay');
        signContainers[i].appendChild(failOverlayImg);
      }
      signContainers[i].querySelector('.park-sign').classList.add('image-load-fail-park-sign');
      signContainers[i].querySelector('.park-sign').src = 'img/loading/broken-sign.svg'
    }
    let newSrc = signContainers[i].querySelector('.park-sign').getAttribute('data-src');
    if(newSrc.slice(-3) != 'svg'){
      newSrc = newSrc + '=w256';
    }
    loadImage.src = newSrc;
  }

  // Load in all the landscape photos.
  function landscapePhotosLoad() {
    let landscapeImages = document.querySelectorAll('.landscape-hidden');
    let landscapeCount = 0;
    // loadingBarContainer.className = 'green-background';
    loadingBar.className = 'blue-background';
    loadingBar.style.width = '0%';
    for (let i = 0; i < landscapeImages.length; i++) {
      const loadImage = new Image();
      loadImage.onload = function(){
        landscapeImages[i].src = loadImage.src;
        landscapeCount = landscapeCount + 1;
        let percentLoaded = parseFloat(loadingBar.style.width);
        let percentLoadedNew = ((landscapeCount/landscapeImages.length) * 100).toFixed(2);
        if (percentLoadedNew > percentLoaded) {
          loadingBar.style.width = percentLoadedNew + '%';
        }
        if(landscapeCount === landscapeImages.length){
          loadingBar.className = 'brown-background';
        }
      }
      loadImage.onerror = function(){
        console.log('Error on landscape image: ' + newSrc);
        landscapeCount = landscapeCount + 1;
        let percentLoaded = parseFloat(loadingBar.style.width);
        let percentLoadedNew = ((landscapeCount/landscapeImages.length) * 100).toFixed(2);
        if (percentLoadedNew > percentLoaded) {
          loadingBar.style.width = percentLoadedNew + '%';
        }
        if(landscapeCount === landscapeImages.length){
          loadingBar.className = 'brown-background';
        }
        landscapeImages[i].src = 'img/loading/broken-landscape.svg'
      }
      let newSrc = landscapeImages[i].getAttribute('data-src') + '=w900';
      loadImage.src = newSrc;
    }
  }
}

// Handles clicking on a sign container.
function handleSignClick(event){
  let signContainerElement = event.target;
  let id = signContainerElement.id;
  let curActiveSignContainerId = activeSignContainerId;
  removeIcons();
  if(curActiveSignContainerId !== id){
    let iconContainers = signContainerElement.getElementsByClassName('icon-container');
    for(let i = 0; i < iconContainers.length; i++) {
      iconContainers[i].classList.add('icon-visible');
    }
    activeSignContainerId = id;
  }
}

// Hide's all visible icons.
function removeIcons(){
  let visibleIconContainers = document.querySelectorAll('.icon-visible');
  visibleIconContainers.forEach((container) => {
    container.classList.remove('icon-visible');
  });
  activeSignContainerId = null;
}

// Handles mousing over signs container. Used to remove icons when out of the active area.
function handleSignsContainerMouseMove(event){
  if(activeSignContainerId){
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

// Filters the type of park signs shown.
function filterParks(elem){
  // Hide all visible park signs.
  let shownSigns = document.querySelectorAll('.sign-shown');
  shownSigns.forEach((sign) => {
    sign.classList.remove('sign-shown');
  });
  // Show filtered park signs.
  let type = elem.id.replace('-filter','');
  if(type === 'all'){
    type = 'sign-container';
  }
  let filteredSigns = document.querySelectorAll('.' + type);
  filteredSigns.forEach((sign) => {
    sign.classList.add('sign-shown');
  });
}

// Shows landscape photos.
function showLandscapes(signContainerElement){
  let landscapeContainer = document.getElementById('landscape-container');
  let galleryContainer = createElement(`
    <div id='landscape-gallery-container'>
      <div id='landscape-images-container'>
        <div class='landscape-grid' id='landscape-grid-container' onclick='event.stopPropagation()'>
          <img class='landscape landscape-1' src=${signContainerElement.querySelector('.landscape-hidden-1').src} ></img>
          <img class='landscape landscape-2' src=${signContainerElement.querySelector('.landscape-hidden-2').src} ></img>
          <img class='landscape landscape-3' src=${signContainerElement.querySelector('.landscape-hidden-3').src} ></img>
        </div>
      </div>
      <div class='landscape-grid' id='exit-grid-container' onclick='event.stopPropagation()'>
        <svg class='exit-landscape-button' onclick='hideLandscapes()' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' viewBox='0 0 2500 2500' shape-rendering='geometricPrecision' text-rendering='geometricPrecision'>
          <ellipse rx='1175' ry='1175' transform='translate(1250 1250)' fill='#592626' stroke='#fcc917' stroke-width='150'/>
          <path d='M1988.19,1407.99l.02-316.25-1035.834,15.99-440-16.07-.018,311.67l467.5-13.72Z' transform='matrix(-.707107 0.707107-.707107-.707107 3018.119405 1249.49909)' fill='#fcc917'/>
          <path d='M1988.19,1407.99l.02-316.25-1035.834,15.99-440-16.07-.018,311.67l467.5-13.72Z' transform='matrix(.707107 0.707107-.707107 0.707107 1249.956518-518.016897)' fill='#fcc917'/>
        </svg>
      </div>
    </div>
  `);
  landscapeContainer.appendChild(galleryContainer);
  landscapeContainer.classList.add('shown');
  landscapeContainer.onclick = function() { hideLandscapes() };
  document.body.classList.add('no-scroll');
}

// Hides landscape photos.
function hideLandscapes(){
  let landscapesContainer = document.getElementById('landscape-container');
  document.body.classList.remove('no-scroll');
  landscapesContainer.classList.remove('shown');
  landscapesContainer.textContent = '';
}

// Creates a HTML element from an HTML string.
function createElement(htmlString){
  let wrapper = document.createElement('div');
  wrapper.innerHTML= htmlString.trim();
  return wrapper.firstChild;
}