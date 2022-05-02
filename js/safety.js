// Optimized photo loading function
function altphotoLoadManager(){
    var list_parks = document.getElementsByClassName("parksigntext")
    var items_populated_check = false // Boolean to indicate that all item arrays have been populated.
    var landing_page_src_counter = 0 // Counter to count the first 15 "pictures with the park sign". On most screens this should be all the pictures initially shown.
    var landing_page_onload_counter = 0 // Counter to count once the first 15 "pictures with the park sign" have been loaded.
    var landing_page_landscape_onload_counter = 0 // Counter to count once the landscape photo elements associated with the first 15 "pictures with the park sign" elements have been loaded.
    var landing_page_landscape_items = [] // Landscape photo elements associated with the first 15 "pictures with the park sign" elements.
    var deeper_page_src_items = [] // The rest of the "pictures with the park sign" elements.
    var deeper_page_landscape_items = [] // Landscape photo elements associated with the rest of the "pictures with the park sign" elements.
    var all_page_text_items = [] // All the elements that are in the form of park sign text SVGs.

    // Ran when one of the landscape photo elements associated with the first 15 "pictures with the park sign" elements is loaded
    var landscapeOnloadCallback = function(){
        landing_page_landscape_onload_counter++;
        if(landing_page_landscape_onload_counter < 45){
            return;
        }
        landscapeAllLoadedCallback();
    }

    // Ran once all of the landscape photo elements associated with the first 15 "pictures with the park sign" elements are loaded
    var landscapeAllLoadedCallback = function(){
        // Load the rest of the "pictures with the park sign" elements.
        for(const park of deeper_page_src_items){
            park.src = park.getAttribute("data-photo-link");
            park.style.opacity =  1;
            park.style.display = "block";
        }
        // Load all the Landscape photo elements associated with the rest of the "pictures with the park sign" elements.
        for(const landscape of deeper_page_landscape_items){
            landscape.src = landscape.getAttribute("data-photo-link");
        }
        // manageParkSigns(1)
    };

    // Ran when one of the first 15 "pictures with the park sign" elements is loaded
    var onloadCallback = function(){
        landing_page_onload_counter++;
        if(landing_page_onload_counter < 15 && items_populated_check){
            return;
        }
        allLoadedCallback();
    };

    // Ran once all of the first 15 "pictures with the park sign" elements are loaded
    var allLoadedCallback = function(){
        // Displaying all the park sign text SVGs.
        for(const text_item of all_page_text_items){
            text_item.style.opacity =  1;
            text_item.style.display = "block";
        }
        manageParkSigns(1)
        // Load all the landscape photo elements associated with the first 15 "pictures with the park sign" elements
        for(const landscape of landing_page_landscape_items){
            landscape.onload = landscapeOnloadCallback
            landscape.src = landscape.getAttribute("data-photo-link");
        }
    };

    for(const park of list_parks) {
        // Looks for the first 15 "pictures with the park sign" elements and loads the google photos source
        if(landing_page_src_counter < 15 && park.getAttribute("data-visited") == "1"){
            park.onload = onloadCallback
            park.style.opacity =  1;
            park.style.display = "block";
            park.src = park.getAttribute("data-photo-link");
            var code = park.id.substring(1, 4)
            // Adding the landscape photos associated with the first 15 "pictures with the park sign" elements to an array
            for (let i = 1; i < 4; i++){
                var landscapeElement = document.getElementById("l" + code + "_" + i)
                landing_page_landscape_items.push(landscapeElement)
            }
            landing_page_src_counter++;
        }
        else{
            // Adds the rest of the "pictures with the park sign" elements to an array
            if(park.getAttribute("data-visited") == "1"){
                deeper_page_src_items.push(park)
                var code = park.id.substring(1, 4)
                // Adding the landscape photos associated with the rest of the "pictures with the park sign" elements to an array
                for (let i = 1; i < 4; i++){
                    var landscapeElement = document.getElementById("l" + code + "_" + i)
                    deeper_page_landscape_items.push(landscapeElement)
                }
            }
            // Adds all the park sign text svg elements to an array
            else{
                all_page_text_items.push(park)
                park.style.opacity =  1;
                park.style.display = "block";
            }
        }
    }
    items_populated_check = true
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
            // alert(numParkSignPerRow)
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
                    // manageParkSigns(1)
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
    manageParkSigns(1)
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