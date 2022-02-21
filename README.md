# stateparks

## Description

On December 12th 2019 I started a journey to see every state park in the California State Park system. I have currently visited 45/282 parks! This website was created to document that journey and share with the people that joined me. At every park I visit, I take a picture at the park sign with the people that joined me and take at least three landscape photos of that park. This website can be accessed at [johnprovazek.com/stateparks](https://www.johnprovazek.com/stateparks/).

This website is hosted for free here using GitHub Pages. It is written using vanilla javascript without a database application. The navbar was built on top of Bootstrap 5. The main body and pictures shown are built using a flexbox layout. This was the first website I built using flexbox and scaled across mobile and desktop screens. I am using [PageCrypt](https://www.maxlaumeister.com/pagecrypt/) as a simple solution to encrypt the html file which contains the links to images. I didn't want search engines or webcrawlers to have access to the images on this website. This keeps the website password protected while still taking advantage of GitHub Pages free hosting. I made a password-free guest option on my website to showcase the website to prospective employers and anyone that might want to setup something similar. 

## Installation

If you would like to access my website it can be found at [johnprovazek.com/stateparks](https://www.johnprovazek.com/stateparks/). If you would like to create a copy of this website for yourself follow along below. 

Once development is complete and thoroughly tested (mobile is a little broken) I will create two branches *simplesite* and *pagecrypt*, where it would be best to start your own development. The *simplesite* branch will not include guest access or [PageCrypt](https://www.maxlaumeister.com/pagecrypt/) and therefore will not be password protected. The *pagecrypt* branch will not include guest access but will still be password protected. Fork off this repo to start creating your own website and start tracking the state parks you've visited! 

## Usage

If you are under the *main* or *pagecrypt* branch start by making changes to the file [main-public.html](common/main-public.html). If you are under the *simplesite* branch you can make changes directly to [index.html](index.html). Start by modifying `<img>` objects with the class `parksigntext` updating the parks you've visited. Here's an example of an `<img>` object of a park that hasn't been visited:
```
<img class="parksign parksigntext SRA ALL" id="s424" data-visited="0" src="img/parks/424.svg" data-parksid="424" alt="Admiral William Standley State Recreation Area" onmouseover="handleLandscapeOnMouseOver(this)" onclick="handleLandscapeOnClick(this)">
```
`<img>` objects that look like the one above will show up as text with the park name. They are represented as svg images that can be found under the [img/parks](img/parks/) folder. Each park has a code associated with it that is the same code used by the California State Parks system.  Here is an example of an `<img>` for a park that has been visited:
```
<img class="parksign parksigntext SPK ALL" id="s523" data-visited="1" src="img/minporttr.png" data-photo-link="https://via.placeholder.com/324x432?text=parksign" data-parksid="523" alt="Año Nuevo State Park" onmouseover="handleLandscapeOnMouseOver(this)" onclick="handleLandscapeOnClick(this)">
```
For parks you've visited update the `data-visited` attribute to 1. This signifies the parks has been visited. Make sure the `src` attribute is set to `img/minporttr.png`. This is a small image file displayed when rendering the page. Replace the link at `data-photo-link` attribute with a link to your own picture with the park sign. In my website I used links from Google Photos. If you don't have links to your photos you could try adding them under the [img](img/) folder and use the path to that image as the link. This option may be more difficult and is untested. There is also a GitHub file and repo size limit that should be looked into before going this route. 

The next step is to add `<div> landscape_list` objects under the `<div> landscape_container` for every park you've visited. These objects contain the landscape images of parks you've visited. Here is an example of a `<div> landscape_list` object:
```
<div id="l523_p" class="landscape_list">
   <img class="landscape" id="l523_1" src="img/minlandtr.png" data-photo-link="https://via.placeholder.com/1366x1024?text=landscape">
   <img class="landscape" id="l523_2" src="img/minlandtr.png" data-photo-link="https://via.placeholder.com/1366x1024?text=landscape">
   <img class="landscape" id="l523_3" src="img/minlandtr.png" data-photo-link="https://via.placeholder.com/1366x1024?text=landscape">
</div>
```
First find the code associated with the park for which you would like to add landscape photos. In the example above this is for the park "Año Nuevo State Park" that has the code "523". Prepend the character "l" and append the strings "_p","_1","_2", or "_3" like the example above. Make sure the `src` attribute is set to `img/minlandtr.png`. Replace the links at the `data-photo-link` attributes with links to your landscape photos.

If you are working under the *simplesite* branch and made your changes directly to [index.html](index.html). That is all you need to do and can skip ahead. If you are working under the *main* or *pagecrypt* and making changes to the file [main-public.html](common/main-public.html) you have a little more work to do. Upload the [main-public.html](common/main-public.html) file to [PageCrypt](https://www.maxlaumeister.com/pagecrypt/), choose a password and download. This downloaded file should look similar to [index.html](index.html). In the file you downloaded, you should find a variable `pl` that is equal to a long encrypted string that represents your html file. Copy that variable and replace the `pl` variable in [index.html](index.html).

Lastly, this website has been setup and designed to fit the picture aspect ratios taken from my phone. The park sign pictures are taken in a portrait aspect ratio of 3x4. The landscape park pictures are in aspect ratio of 4x3. The website navbar scaling was scaled according to the my title "John Provazek's State Park Checklist" and would likely need to be altered for a longer or shorter title.

## Credits

[PageCrypt](https://www.maxlaumeister.com/pagecrypt/) was used for the encryption solution.

[Bootstrap 5](https://getbootstrap.com/docs/5.0/components/navbar/) was used for the navbar.

## Bugs & Features

- Might be race condition when opening landscape, specifcally a problem on slow networks.
- Add password-free guest option.
- Add missing parks SVGs.
- Add simplesite and pagecrypt branch.

## License

No License for now until I have a better understanding of this. Would like this to be free for non commercial use.
