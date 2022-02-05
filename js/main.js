/*  Global Variables  */
var totalParks = 0
var true_var = true
var false_var = false
var currentActiveDropdown = "ALL"
var numParkSignPerRow = 0
var intervalID = null
var mobileOpen = false
var numParkPerCategory = {  /*  TODO: could reduce to tuples probably  */
    ALL: 1,
    SPK: 1,
    HPK: 1,
    SBH: 1,
    SRA: 1,
    SNR: 1,
    VRA: 1,
    OTH: 1,
};
var numVisitedPerCategory = {  /*  TODO: could reduce to tuples probably  */
    ALL: 1,
    SPK: 1,
    HPK: 1,
    SBH: 1,
    SRA: 1,
    SNR: 1,
    VRA: 1,
    OTH: 1,
};

window.onload = function() {
    setParkData()  /*  Calculates and sets data for parks  */
    photoLoadManager()  /*  Handles loading in park images  */
    navbarOnLoad()  /*  js/navbar.js: Handles navbar variables and setup on mobile  */
};

window.onresize = function() {
    manageParkSigns(0)  /*  Manages adding transparent parksigns to bottom of parksignflexbox  */
    removeLandscape("xxx")  /*  Removes any landscape photos that do not match the input code  */
    navbarOnResize()  /*  js/navbar.js: Handles navbar toggle and dropdown issues when switching between mobile (small window < 1025px) and desktop screens  */
}

/*  Calculates and sets data for parks  */
function setParkData(){
    /*  Calculates the total amount of parks and stores in variable  */
    totalParks = document.getElementsByClassName("parksigntext").length
    /*  Calculates the number of parks per category and parks visited per category  */
    var parktypes = [ "SPK","HPK","SBH","SRA","SNR", "VRA", "OTH", "ALL"]
    for (const parktype of parktypes) {
        numParkPerCategory[parktype] = document.getElementsByClassName(parktype).length 
        var list_parks = document.getElementsByClassName(parktype)
        var counter = 0;
        for(const park of list_parks) {
            if(park.getAttribute("data-visited") == "1"){
                counter = counter + 1
            }
        }
        numVisitedPerCategory[parktype] = counter
    }
}

/*  Handles loading in park images  */
function photoLoadManager(){
    var parksigns = document.getElementsByClassName("parksigntext")
    var counter = 0
    var dumpFirstLandscapesComplete = 0
    var landscapeIDArray = []
    for(const park of parksigns) {
        counter++
        if(park.getAttribute("data-visited") == "1"){
            if(counter < numParkSignPerRow * 5){  /*  Load portrait photos for the first visible portrait images */
                park.src = park.getAttribute("data-photo-link");
                landscapeIDArray.push(park.id.substring(1, 4));
            }
            else{
                if(!dumpFirstLandscapesComplete){  /*  Load landscape photos for the first visible portrait images */
                    for(const code of landscapeIDArray){
                        for (let i = 1; i < 4; i++){
                            var landscapeElement = document.getElementById("l" + code + "_" + i)
                            landscapeElement.src = landscapeElement.getAttribute("data-photo-link")
                        }
                    }
                    landscapeIDArray = []
                    dumpFirstLandscapesComplete = 1
                    var list_parks = document.getElementsByClassName("parksign")
                    for(const park of list_parks) {
                        park.style.opacity =  0;
                        park.style.display = "block";
                    }
                    intervalID = setInterval(opacityFade, 10);
                    manageParkSigns(1)
                }
                park.src = park.getAttribute("data-photo-link"); /*  Load rest of portrait photos  */
                landscapeIDArray.push(park.id.substring(1, 4));
            }
        }
    }
    for(const code of landscapeIDArray){  /*  Load rest of landscape photos  */
        for (let i = 1; i < 4; i++){
            var landscapeElement = document.getElementById("l" + code + "_" + i)
            landscapeElement.src = landscapeElement.getAttribute("data-photo-link")
        }
    }
}

/*  Helper function to increase opacity of parksign elements  */
function opacityFade(){
    var list_parks = document.getElementsByClassName("parksign")
    for(const park of list_parks) {
        var opacity = Number(park.style.opacity)
        if(opacity < 1){
            opacity = opacity + 0.01
            park.style.opacity = opacity
        }
        else{
            clearInterval(intervalID); 
        }
    }
}

/*  Manages adding transparent parksigns to bottom of parksignflexbox  */
function manageParkSigns(force) {
    var parkSignElement = document.getElementsByClassName(currentActiveDropdown)[0]
    const numPerRow = Math.round(window.innerWidth / parkSignElement.width)
    if (force || numPerRow != numParkSignPerRow) {
        var extras = (numPerRow - (numParkPerCategory[currentActiveDropdown] % numPerRow)) % numPerRow
        var elements = document.getElementsByClassName("transparentend");
        while(elements.length > 0){
            elements[0].parentNode.removeChild(elements[0]);
        }
        var flexbox = document.getElementById("parksignflexbox")
        for (let i = 0; i < extras; i++) {
            var x = document.createElement("IMG");
            x.setAttribute("src", "img/transparent612x817.png");
            x.setAttribute("class", "parksign transparentend");
            flexbox.appendChild(x);
        }
    }
    numParkSignPerRow = numPerRow;
}

/*  Removes any landscape photos that do not match the input code  */
function removeLandscape(code){
    var parent = document.getElementById("parksignflexbox");
    var openLandscapes = document.querySelectorAll('[id$=_temp]');
    for(const landscape of openLandscapes) {
        if(landscape.id.substring(1, 4) != code){
            parent.removeChild(landscape);
        }
    }
    return document.querySelectorAll('[id$=_temp]').length;
}

/*  Filter the type of parks shown  */
function filterParks(elem){
    var code = elem.id

    /*  Set Display to none and display to block to filter  */
    var list_parks = document.getElementsByClassName("ALL")
    for(const park of list_parks) {
        park.style.display = "none";
    }
    var list_parks = document.getElementsByClassName(code)
    for(const park of list_parks) {
        park.style.display = "block";
    }

    /*  Update the dropdown text  */
    var visited = numVisitedPerCategory[code]
    var parkspercategory = numParkPerCategory[code]
    var dropdown = document.getElementById("navbarDropdownMenuLink");
    dropdown.text = elem.getAttribute("data-text") + " " + visited + "/" + parkspercategory
    dropdown.setAttribute("data-current-id",code)

    currentActiveDropdown = code
    removeLandscape("xxx")
    manageParkSigns(1)
    navbarCloseDropdown(elem)
    navbarStyleSelectedDropdown()
}

/*  Handle adding and removing landscape photos triggered onMouseOver - specific to desktop */
function handleLandscapeOnMouseOver(elem){
    if(!isMobileDevice()){
        var code = elem.id.substring(1, 4)
        var itemsActive = removeLandscape(code)
        if(itemsActive == "0" && elem.getAttribute("data-visited") == "1"){
            var counter = 0
            var list_parks = document.getElementsByClassName(currentActiveDropdown)
            while(list_parks[counter] != elem){
                counter++
            }
            counter++
            var restInRow = (numParkSignPerRow - (counter % numParkSignPerRow)) % numParkSignPerRow
            var endsibling = elem
            for (let i = 0; i < restInRow; i++) {
                do{
                    endsibling = endsibling.nextElementSibling
                }while(endsibling.style.display == "none")
            }
            for(let i = 1; i < 4; i++) {
                var landscape_clone = document.getElementById("l" + code + "_" + i).cloneNode(true);
                landscape_clone.id = landscape_clone.id + "_temp"
                endsibling.parentNode.insertBefore(landscape_clone,endsibling.nextElementSibling);
            }
        }
    }
}

/*  Handle adding and removing landscape photos triggered onClick - specific to mobile */
/*  TODO: this can be condensed  */
function handleLandscapeOnClick(elem){
    if(isMobileDevice()){
        var code = elem.id.substring(1, 4)
        var itemsActive = removeLandscape(code) 

        /*  if clicked an empty tile or clicked a different picture tile than the one active set mobileOpen to false  */
        if(elem.getAttribute("data-visited") == "0" || itemsActive == 0){
            mobileOpen = false
        }

        /*  if a picture tile is open and has been clicked again close the landscape  */
        if(mobileOpen && elem.getAttribute("data-visited") == "1"){
            removeLandscape("xxx")
            itemsActive = 1  /* don't run if statement below  */
            mobileOpen = false
        }

        /* if clicked on picture tile add */
        if(itemsActive == "0" && elem.getAttribute("data-visited") == "1"){
            var counter = 0
            var list_parks = document.getElementsByClassName(currentActiveDropdown)
            while(list_parks[counter] != elem){ /* TODO: is this always in order? */
                counter++
            }
            counter++
            var restInRow = (numParkSignPerRow - (counter % numParkSignPerRow)) % numParkSignPerRow 
            var endsibling = elem
            for (let i = 0; i < restInRow; i++) {
                do{
                    endsibling = endsibling.nextElementSibling
                }while(endsibling.style.display == "none")
            }
            for(let i = 1; i < 4; i++) {
                var landscape_clone = document.getElementById("l" + code + "_" + i).cloneNode(true);
                landscape_clone.id = landscape_clone.id + "_temp"
                endsibling.parentNode.insertBefore(landscape_clone,endsibling.nextElementSibling);
            }
            mobileOpen = true
        }
    }
}

/*  Determine if on a mobile device - taken from internet */
function isMobileDevice() {
    var check = false;
    (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);
    return check;
}