/*  Global Variables  */
var last_width = 0

/*  Handles navbar variables and setup on mobile  */
function navbarOnLoad(){
    last_width = window.innerWidth;  /*  Sets intial window width  */
    navbarSetParkNumbersDropdown()  /*  Sets the parks filter dropdown onload for mobile to show the numbers visted per category  */
    navbarStyleSelectedDropdown()  /*  Sets the parks dropdown background and color to the one selected  */
};

/*  Handles navbar toggle and dropdown issues when switching between mobile (small window < 1025px) and desktop screens  */
function navbarOnResize(){
    var window_width = window.innerWidth;
    if((window_width < 1025 && last_width > 1024) || (window_width > 1024 && last_width < 1025)){  /*  Resets dropdowns to be closed when screen is switched between mobile and desktop  */
        var top_dropdown = document.getElementById("navbarNavDropdown")
        var dropdown = document.getElementById("navbarDropdownMenuLink")
        var dropdown_list = document.getElementById("dropdown-parks")
        top_dropdown.className = "collapse navbar-collapse"
        top_dropdown.style.height = "auto"
        top_dropdown.style.paddingTop = "12px"
        dropdown.className = "nav-link dropdown-toggle unselectable"
        dropdown.ariaExpanded = "false"
        dropdown.style.display = "block"
        dropdown_list.className = "dropdown-menu dropdown-menu-end"
        dropdown_list.removeAttribute('data-bs-popper')
    }
    if(window_width < 1025 && last_width > 1024){  /*  Mobile  - Adds Number Visited to text in dropdown and resets color  */
        var parktypes = [ "SPK","HPK","SBH","SRA","SNR", "VRA", "OTH", "ALL"]
        for (const parktype of parktypes) {
            document.getElementById(parktype).innerHTML = document.getElementById(parktype).getAttribute("data-text") + " - " + numVisitedPerCategory[parktype] + "/" + numParkPerCategory[parktype]
        }
        navbarStyleSelectedDropdown()
    }
    if(window_width > 1024 && last_width < 1025){  /*  Desktop  - Removes Number Visited to text in dropdown and resets color  */
        var parktypes = [ "SPK","HPK","SBH","SRA","SNR", "VRA", "OTH", "ALL"]
        for (const parktype of parktypes) {
            document.getElementById(parktype).innerHTML = document.getElementById(parktype).getAttribute("data-text")
            document.getElementById(parktype).style.color = "#FCC917";
            document.getElementById(parktype).style.backgroundColor = "#592626";
        }
    }
    last_width = window_width
}

/*  Sets the parks filter dropdown onload for mobile to show the numbers visted per category  */
function navbarSetParkNumbersDropdown(){
    var window_width = window.innerWidth
    if(window_width < 1025){
        var parktypes = [ "SPK","HPK","SBH","SRA","SNR", "VRA", "OTH", "ALL"]
        for (const parktype of parktypes) {
            document.getElementById(parktype).innerHTML = document.getElementById(parktype).getAttribute("data-text") + " - " + numVisitedPerCategory[parktype] + "/" + numParkPerCategory[parktype]
        }
    }
}

/*  Sets the parks dropdown background and color to the one selected */
function navbarStyleSelectedDropdown(){
    var window_width = window.innerWidth
    if(window_width < 1025){
        /*  Reset all dropdowns backgrounds and colors  */
        var parktypes = [ "SPK","HPK","SBH","SRA","SNR", "VRA", "OTH", "ALL"]
        for (const parktype of parktypes) {
            document.getElementById(parktype).style.color = "#FCC917";
            document.getElementById(parktype).style.backgroundColor = "#592626";
        }
        /*  Set selected dropdown backgrounds and colors  */
        var current_selected_id = document.getElementById("navbarDropdownMenuLink").getAttribute("data-current-id")
        document.getElementById(current_selected_id).style.color = "#337321";
        document.getElementById(current_selected_id).style.backgroundColor = "#002469";
    }
}


/*  Handles opening and closing dropdown on mobile menu button press  */
function navbarOpenDropdown(elem){
    var top_dropdown = document.getElementById("navbarNavDropdown")
    var dropdown = document.getElementById("navbarDropdownMenuLink")
    var dropdown_list = document.getElementById("dropdown-parks")
    if(dropdown.ariaExpanded == "true"){  /*  Open  */
        top_dropdown.className = "collapse navbar-collapse"
        top_dropdown.style.height = "auto"
        top_dropdown.style.paddingTop = "12px"
        dropdown.className = "nav-link dropdown-toggle unselectable"
        dropdown.ariaExpanded = "false"
        dropdown.style.display = "block"
        dropdown_list.className = "dropdown-menu dropdown-menu-end"
        dropdown_list.removeAttribute('data-bs-popper')
    }
    else{  /*  Closed  */
        top_dropdown.className = "navbar-collapse collapse show"
        top_dropdown.style.height = "auto"
        top_dropdown.style.paddingTop = "12px"
        dropdown.className = "nav-link dropdown-toggle unselectable"
        dropdown.ariaExpanded = "true"
        dropdown.style.display = "none"
        dropdown_list.className = "dropdown-menu dropdown-menu-end show"
        dropdown_list.setAttribute("data-bs-popper", "none")
    }
}

/*  Handles closing dropdown when a selection is made from the dropdown on mobile  */
function navbarCloseDropdown(elem){
    var window_width = window.innerWidth;
    if(window_width < 1025){
        var top_dropdown = document.getElementById("navbarNavDropdown")
        var dropdown = document.getElementById("navbarDropdownMenuLink")
        var dropdown_list = document.getElementById("dropdown-parks")
        top_dropdown.className = "collapse navbar-collapse"
        top_dropdown.style.height = "auto"
        top_dropdown.style.paddingTop = "12px"
        dropdown.className = "nav-link dropdown-toggle unselectable"
        dropdown.ariaExpanded = "false"
        dropdown.style.display = "block"
        dropdown_list.className = "dropdown-menu dropdown-menu-end"
        dropdown_list.removeAttribute('data-bs-popper')
    }
}

/*  Handles resizing navbar to look better on mobile  - TODO: this is handled in js/speedy.js now but might need later  */
function navbarMobileResize(){
    if(isMobileDevice()){
        var element = document.getElementsByClassName("container-fluid")[0];
        var computedStyle = getComputedStyle(element);
        elementHeight = element.clientHeight;  // height with padding
        elementWidth = element.clientWidth;   // width with padding
        elementHeight -= parseFloat(computedStyle.paddingTop) + parseFloat(computedStyle.paddingBottom);
        elementWidth = elementWidth - parseFloat(computedStyle.paddingLeft) - parseFloat(computedStyle.paddingRight);
    
        var logo = document.getElementById("logo")
        var menu = document.getElementById("menu-symbol")
        var text = document.getElementById("navbar-main-text")
        var index = 0;
        logo.setAttribute("style","width:2px;height:2px;");
        menu.setAttribute("style","width:2px;height:2px;");
        text.setAttribute("style","width:2px;height:4px;");
    
        while (logo.clientWidth + menu.clientWidth + text.clientWidth + 16 + 16 < elementWidth) {
            index = index + 1
            logo.setAttribute("style","width:" + index*2 + "px;height:" + index*2 + "px;");
            menu.setAttribute("style","width:" + index*2 + "px;height:" + index*2 + "px;");
            text.setAttribute("style","font-size:" + index + "px;");
        }
        index = index - 1
        logo.setAttribute("style","width:" + index*2 + "px;height:" + index*2 + "px;");
        menu.setAttribute("style","width:" + index*2 + "px;height:" + index*2 + "px;");
        text.setAttribute("style","font-size:" + index + "px;");
    }
}

//  Mobile  - Standard - Open
//  <button id="menu-button" class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="true" aria-label="Toggle navigation" onclick="navbarOpenDropdown(this)">
//  <div class="navbar-collapse collapse show" id="navbarNavDropdown" style="">
//  <a class="nav-link dropdown-toggle unselectable show" href="#" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="true">All State Parks 43/282</a>
//  <ul id="dropdown-parks" class="dropdown-menu dropdown-menu-end show" aria-labelledby="navbarDropdownMenuLink" data-bs-popper="none">


//  Mobile  - Standard - Half Open
//  <button id="menu-button" class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="true" aria-label="Toggle navigation" onclick="navbarOpenDropdown(this)">
//  <div class="navbar-collapse collapse show" id="navbarNavDropdown" style="">
//  <a class="nav-link dropdown-toggle unselectable" href="#" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">All State Parks 43/282</a>
//  <ul id="dropdown-parks" class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdownMenuLink">


//  Mobile  - Standard - Closed
//  <button id="menu-button" class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation" onclick="navbarOpenDropdown(this)">
//  <div class="collapse navbar-collapse" id="navbarNavDropdown">
//  <a class="nav-link dropdown-toggle unselectable" href="#" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">All State Parks 43/282</a>
//  <ul id="dropdown-parks" class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdownMenuLink">


//  Desktop - Standard - Open
//  <button id="menu-button" class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation" onclick="navbarOpenDropdown(this)">
//  <div class="collapse navbar-collapse" id="navbarNavDropdown">
//  <a class="nav-link dropdown-toggle unselectable show" href="#" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="true">All State Parks 43/282</a>
//  <ul id="dropdown-parks" class="dropdown-menu dropdown-menu-end show" aria-labelledby="navbarDropdownMenuLink" data-bs-popper="none">


//  Desktop - Standard - Closed
//  <button id="menu-button" class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation" onclick="navbarOpenDropdown(this)">
//  <div class="collapse navbar-collapse" id="navbarNavDropdown">
//  <a class="nav-link dropdown-toggle unselectable" href="#" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">All State Parks 43/282</a>
//  <ul id="dropdown-parks" class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdownMenuLink">
