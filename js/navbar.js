// Handles navbar setup.
function navbarOnLoad(){
  navbarSetDropdownText(); // Sets the dropdown text. Handles mobile screens showing the number of parks visited per category.
  let dropdownItems = document.getElementsByClassName('dropdown-item');
  for (let i = 0; i < dropdownItems.length; i++) {
    dropdownItems[i].addEventListener('click', navbarHandleSelectedDropdown);
  }
};

// Handles navbar resizing.
function navbarOnResize(){
  navbarMobileDropdownClose();
  navbarSetDropdownText();
}

// Handles adding dropdown text. On mobile screens the dropdown text will include the number of parks visited per category.
function navbarSetDropdownText(){
  let parkCategories = ['all','state-park','state-historic-park','state-beach','state-recreation-area','state-natural-reserve','state-vehicular-recreation-area','other'];
  for (let parkCategory of parkCategories) {
    let navElement = document.getElementById(parkCategory + '-filter');
    let navElementText = navElement.textContent.split(' - ')[0];
    if(window.innerWidth < 1025){
      navElementText = navElementText + ' - ' + stats[parkCategory]['visited'] + '/' + stats[parkCategory]['count'];
    }
    navElement.innerHTML = navElementText;
  }
}

// Handles when a navbar dropdown item has been selected.
function navbarHandleSelectedDropdown(event){
  // Adding and removing 'selected-item' class.
  document.querySelector('.selected-item').classList.remove('selected-item');
  let selectedDropdown = event.target;
  selectedDropdown.classList.add('selected-item');
  // Setting dropdown text.
  let dropdown = document.getElementById('navbar-dropdown-menu-link');
  let code = selectedDropdown.id.replace('-filter','');
  dropdown.text = selectedDropdown.textContent.split(' - ')[0] + ' ' + stats[code]['visited'] + '/' + stats[code]['count'];
  // Handle closing dropdown on mobile screens.
  if(window.innerWidth < 1025){
    navbarMobileDropdownClose();
  }
}

// Handles opening and closing dropdown on a mobile screen when the menu button is pressed.
function navbarMenuToggle(){
  if(document.getElementById('navbar-dropdown-menu-link').ariaExpanded == 'true'){
    navbarMobileDropdownClose();
  }
  else{
    navbarMobileDropdownOpen();
  }
}

// Handles opening navbar in a mobile friendly view by overriding Bootstrap.
function navbarMobileDropdownOpen(){
  let topDropdown = document.getElementById('navbar-nav-dropdown');
  topDropdown.className = 'collapse navbar-collapse show show-mobile-collapse';
  let dropdown = document.getElementById('navbar-dropdown-menu-link');
  dropdown.className = 'nav-link dropdown-toggle unselectable hide-mobile-dropdown';
  dropdown.ariaExpanded = 'true';
  let dropdownList = document.getElementById('dropdown-parks');
  dropdownList.className = 'dropdown-menu dropdown-menu-end show';
  dropdownList.setAttribute('data-bs-popper', 'none');
}

// Handles closing navbar in a mobile friendly view by overriding Bootstrap.
function navbarMobileDropdownClose(){
  let topDropdown = document.getElementById('navbar-nav-dropdown');
  topDropdown.className = 'collapse navbar-collapse';
  let dropdown = document.getElementById('navbar-dropdown-menu-link');
  dropdown.className = 'nav-link dropdown-toggle unselectable show-mobile-dropdown';
  dropdown.ariaExpanded = 'false';
  let dropdownList = document.getElementById('dropdown-parks');
  dropdownList.className = 'dropdown-menu dropdown-menu-end';
  dropdownList.removeAttribute('data-bs-popper');
}