# stateparks

## Description

On December 12th 2019, I started a journey to see every state park in the California State Park system. I have currently visited 51/282 parks! This website was created to document that journey and share with the people that joined me. At every park I visit, I take a picture at the park sign and take at least three landscape photos of that park. This website can be accessed at [johnprovazek.com/stateparks](https://www.johnprovazek.com/stateparks/).

This website is hosted for free here using GitHub Pages. It is written using vanilla JavaScript. The navbar was built on top of Bootstrap 5. The main body and pictures shown are built using a flexbox layout. I didn't want search engines or webcrawlers to have access to the images on this website. I am using [PageCrypt](https://www.maxlaumeister.com/pagecrypt/) as a solution to encrypt the main html file containing the image links. This keeps the website password protected while still taking advantage of GitHub Pages free hosting. I made a password-free guest option on my website to showcase the website to anyone that might want to setup something similar. 

## Installation

If you would like to access my website it can be found at [johnprovazek.com/stateparks](https://www.johnprovazek.com/stateparks/). If you would like to create a copy of this website follow the steps below. 

The repo is currently structured with [index.html](./index.html) as the default page. The page [index.html](./index.html) is utilizing [PageCrypt](https://www.maxlaumeister.com/pagecrypt/) so the main content is encrypted. The page [template.html](./template.html) would be a good place to start your development. You can rename [template.html](./template.html) to "index.html" and delete the old [index.html](./index.html) if you wish.

## Usage

### Adding Park Sign Photos

Start by modifying `<img>` elements with the class `parksigntext` updating the parks you've visited. Here's an example of an `<img>` element of a park that hasn't been visited:
```
<img class="parksign parksigntext SRA ALL" id="s424" data-visited="0" src="img/parks/424.svg" data-parksid="424" alt="Admiral William Standley State Recreation Area" onmouseover="handleLandscapeOnMouseOver(this)" onclick="handleLandscapeOnClick(this)">
```
`<img>` elements that look like the one above will show up as text with the park name. They are represented as svg images that can be found under the [img/parks](img/parks/) folder. Each park has a code associated with it. You can find the code that corresponds to a park in the html file. Here is an example of an `<img>` element for a park that has been visited:
```
<img class="parksign parksigntext SPK ALL" id="s523" data-visited="1" src="img/minporttr.png" data-photo-link="https://via.placeholder.com/324x432?text=parksign" data-parksid="523" alt="Año Nuevo State Park" onmouseover="handleLandscapeOnMouseOver(this)" onclick="handleLandscapeOnClick(this)">
```
For parks you've visited update the `data-visited` attribute to 1. This signifies the parks has been visited. Make sure the `src` attribute is set to "img/minporttr.png". This is a small image file displayed when rendering the page. Replace the link at the `data-photo-link` attribute with a link to your picture with the park sign. In my website I used links from Google Photos.

### Adding Landscape Park Photos

The next step is to add `<img>` elements for each landscape photo. Each park will have a `<div>` with the class `landscape_list`. Add `<img>` elements under that element. This website is structured to take three landscape photos for every park that has been visited. If a park hasn't been visited you can leave the `landscape_list <div>` empty. Here is an example of a `landscape_list <div>` with three landscape `<img>` elements:
```
<div id="l523_p" class="landscape_list" alt="Año Nuevo State Park">
    <img class="landscape" id="l523_1" src="img/minlandtr.png" data-photo-link="https://via.placeholder.com/1366x1024?text=l523_1">
    <img class="landscape" id="l523_2" src="img/minlandtr.png" data-photo-link="https://via.placeholder.com/1366x1024?text=l523_2">
    <img class="landscape" id="l523_3" src="img/minlandtr.png" data-photo-link="https://via.placeholder.com/1366x1024?text=l523_3">
</div>
```
First find the code associated with the park for which you would like to add landscape photos. In the example above this is for the park "Año Nuevo State Park" that has the code "523". Prepend the character "l" and append the strings "_1","_2", or "_3" like the example above. Make sure the `src` attribute is set to "img/minlandtr.png". Replace the links at the `data-photo-link` attribute with links to your landscape photos.

Lastly, this website has been setup and designed to fit the picture aspect ratios taken from my phone. The park sign pictures are taken in a portrait aspect ratio of 3x4. The landscape park pictures are in aspect ratio of 4x3. If you have pictures with different aspect ratios you may need to modify this projects code to work with your photos. The website navbar scaling was scaled according to the title "John Provazek's State Park Checklist". The website scaling might need to be altered for a longer or shorter title.

## Credits

[PageCrypt](https://www.maxlaumeister.com/pagecrypt/) was used for the encryption solution.

[Bootstrap 5](https://getbootstrap.com/docs/5.0/components/navbar/) was used for the navbar.

## Bugs & Improvements

- Possible race condition when opening landscape photos, specifically a problem on slow networks.
- Add missing parks SVGs.
- Blur new images and add them to the guest page 
