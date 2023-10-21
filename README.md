# stateparks

## Description

On December 12th 2019, I started a journey to see every state park in the California State Park system. This project was created to document this journey and share it with the people that joined me. At every park I visit I take a picture with the park sign and at least three landscape photos. This website can be accessed at [johnprovazek.com/stateparks](https://www.johnprovazek.com/stateparks/).

This website is hosted for free using GitHub Pages. It is written using vanilla JavaScript. The navbar was built on top of Bootstrap 5. To avoid search engines and webcrawlers from having access to the image links on this website, I am using [PageCrypt](https://github.com/MaxLaumeister/pagecrypt) as a solution to encrypt the main html file containing the image links. This keeps the website password protected while still taking advantage of GitHub Pages free hosting. This project is setup to use image links from Google Photos. There is also a password free [guest option](https://www.johnprovazek.com/stateparks/guest.html) to showcase the website to anyone that might be interested in setting up something similar.

## Installation

### Structure

The way this project is setup is with the [index.html](./index.html) file as the login page. The *main.html* file is where the main content of this project is located. The *main.html* file is included in the [.gitignore](./.gitignore) file and has been left out of this repository. This is because the file contains the Google Photos image links that need to be encrypted. The content of *main.html* is encrypted and stored in the [index.html](./index.html) file using [PageCrypt](https://github.com/MaxLaumeister/pagecrypt). There is also a [guest.html](./guest.html) file that acts as a password free demo page for this project. The [guest.html](./guest.html) file is structered identically to the *main.html* file just with different image links. If you are not interested in utilizing [PageCrypt](https://github.com/MaxLaumeister/pagecrypt) in your project you will have to make some adjustments to alter this structure.

### Updates

This project contains many helpful python scripts to assist with setting up and maintaining the website as new parks are visited. These scripts can be found in the [update](./update/) directory. There is a *parks.json* that is included in the [.gitignore](./.gitignore) file and has been left out of this repository. This is because the file contains the Google Photos image links that need to be encrypted. The *parks.json* file is where all the important park information is stored and updated. This file will be used when generating the html files for the website.

When first building this project the first script to run is [scrape.py](./update/scrape.py). This script is used to gather the latest California State Parks data from the official California State Parks website. This script will then generate/update the *parks.json* file and the [parks](./img/parks/) and [overlay](./img/overlay/) image directories with SVG images of the park names.

The next step would be to go through the *parks.json* file and update the park fields as needed.

Some of the park names pulled from the official California State Parks website were too long and needed to be abriviated or altered. You may do this as you see fit. When changing a park name in the *parks.json* file you will also need to generate new SVG images for that park. You can do this by running the script [sign.py](./update/sign.py).

Parks that have been visited will need to be updated in the *parks.json* file. To mark a park as visited set the visited field to true.

This project is currently setup to use Google Photos image links for all park photos. There is a script [photos.py](./update/photos.py) included to help with automating the process of gathering the direct image links from Google Photos shared album links.

Occasionally photos with the park sign may be difficult to read so there is an overlay option included to place an SVG image overlay of the park name on top of the park sign photo. To utilize this set the overlay option to true in the *parks.json* file.

The last step is to run the script [build.py](./update/build.py) to generate the html files. You will need to add a *passphrase.txt* file with a passphrase in the first line to the [assets](./update/assets/) directory in order to encrypt the site.

### Adjustments

This website has been setup and designed to fit the picture aspect ratio of 3:4 for park sign photos and 4:3 for landscape park photos. If you have photos with different aspect ratios you may need to modify this projects code to get it to work with your photos.

This project also utilizes Google Photos image links. If you would like to use a different method, you will need to make adjustments.

The website navbar title is setup as a SVG and will likely need to be adjusted when adding your own name.

## Usage

Use the dropdown to filter the type of parks shown.

Click on the landscape icon under a park to view the landscape photos for that park.

## Credits

[PageCrypt](https://github.com/MaxLaumeister/pagecrypt) was used for the encryption solution.

[Bootstrap 5](https://getbootstrap.com/docs/5.0/components/navbar/) was used for the navbar.

## Bugs & Improvements

- Test directly embedding SVGs using the `<text>` element instead of using SVG image files. 
- Add retry logic for when Google Photos images fail to load.
- Add lines to seperate the landscape loading images.
- Needs further testing on a slow network.
- Add a map feature to show all the parks on a map.
- Use a linter and a style guide.