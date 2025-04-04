# stateparks

## Description

In late 2019, I started a journey to see every state park in the California State Park system.
At every park I visit I take a picture with the park sign and at least three landscape photos.
This website was created to serve as a checklist for the parks I've visited and to showcase the photos I took at each park.
This website can be accessed at [johnprovazek.com/stateparks](https://www.johnprovazek.com/stateparks/).

This project was built with the intention to be hosted using GitHub Pages.
[PageCrypt](https://github.com/MaxLaumeister/pagecrypt) is used as a solution to keep the main content and images of this website encrypted while still taking advantage of GitHub Pages free hosting.
There is also a password-free [guest page](https://www.johnprovazek.com/stateparks/guest.html) to showcase this website to anyone that might be interested in setting up something similar.

Built using vanilla JavaScript.

<div align="center">
  <picture>
    <img src="https://repository-images.githubusercontent.com/842290182/2ea32130-5e3b-458e-95cd-348fc21821df" width="830px">
  </picture>
</div>

## Installation

### Structure

The way this project is structured is with the [index.html](./index.html) file setup as the login page.
The _main.html_ file is where the main content of this project is located.
The _main.html_ file is included in the [.gitignore](./.gitignore) file and has been left out of this repository.
This is because the file contains the [Google Photos](https://photos.google.com/) image links that need to be encrypted.
The content of _main.html_ is encrypted and stored in the [index.html](./index.html) file using [PageCrypt](https://github.com/MaxLaumeister/pagecrypt).
There is also a [guest.html](./guest.html) file that acts as a password-free [demo page](https://www.johnprovazek.com/stateparks/guest.html) for this project.
The [guest.html](./guest.html) file is structured identically to the _main.html_ file just with different image links.
If you are not interested in utilizing [PageCrypt](https://github.com/MaxLaumeister/pagecrypt) in your project you will have to make some adjustments to alter this structure.

### Updates

This project contains many helpful python scripts to assist with setting up and maintaining the website as new parks are visited.
These scripts can be found in the [update](./update/) directory.
There is a _parks.json_ file located in the [assets](./update/assets/) directory that is included in the [.gitignore](./.gitignore) file and has been left out of this repository.
This is because the _parks.json_ file contains the [Google Photos](https://photos.google.com/) image links that need to be encrypted.
The _parks.json_ file is where all the important park information is stored and updated.
This file will be used when generating the html files for the website.

When building this project for the first time, the first script to run is [scrape.py](./update/scrape.py).
This script is used to gather the latest California State Parks data from the official California State Parks website.
This script will then generate/update the _parks.json_ file and the [parks](./images/parks/) and [overlay](./images/overlay/) image directories with SVG images that will be used to display the park names on the website.

When running the [scrape.py](./update/scrape.py) script, the script will override some park names and park types pulled from the official California State Parks website with values outlined in [overrides.json](./update/assets/overrides.json).
There are a few park names that were too long when creating their SVG images resulting in the need for abbreviated park names.
There were also some incorrect names for parks on the official California State Parks website at the time this was last updated.
The [overrides.json](./update/assets/overrides.json) file is setup to override the results in the official California State Parks website with any desired changes you have.

When running the [scrape.py](./update/scrape.py) script it will also add GPS coordinates to parks based on the coordinates found in the [coords.json](./update/assets/coords.json) file with corresponding park codes.
[scrape.py](./update/scrape.py) is currently not setup to pull the GPS coordinates from the official California State Parks website.
If you are adding a new park with coordinates that are not listed in [coords.json](./update/assets/coords.json), you will need to manually enter the coordinates for these parks.

The [scrape.py](./update/scrape.py) script should take care of setting up the [parks](./images/parks/) and [overlay](./images/overlay/) image directories with SVG images.
However, if you have a need to recreate the SVG images or create a park or overlay SVG image for a single park you can run the script [sign.py](./update/sign.py) to do so.

The next step is to update the _parks.json_ file by adding your first and last name to the appropriate fields.
This will handle setting up your name in the navigation bar.

The next step is to update the _parks.json_ file by marking all the parks that you have visited.
To mark a park as visited, find the park in the _parks.json_ file and set the visited field to true.

The next step is to update the _parks.json_ file with image links for each park.
This project is currently setup to use [Google Photos](https://photos.google.com/) image links for all park photos.
The [photos.py](./update/photos.py) script is included to help with automating the process of gathering the direct image links from [Google Photos](https://photos.google.com/) shared album links.
To utilize this script you first need to add [Google Photos](https://photos.google.com/) shared album links in the _parks.json_ file under the appropriate park photo "share" property.
The [Google Photos](https://photos.google.com/) shared album links can be created by going to [Google Photos](https://photos.google.com/), finding your image, and clicking Share > Create Link > Copy.
Next add these share links to to the _parks.json_ file under the appropriate park photo "share" property.
Once that is complete you are ready to run the [photos.py](./update/photos.py) script.
This will pull the direct image link from the [Google Photos](https://photos.google.com/) shared album link's html and add it to the _parks.json_ file under the appropriate park photo "photo" property.

Occasionally photos with the park sign may be difficult to read.
There is an overlay option included to place a SVG image overlay of the park name on top of the park sign photo.
To utilize this feature for a park, find the park in the _parks.json_ file and set the overlay option to true.

The last step is to run the script [build.py](./update/build.py) to generate the html files.
You will need to add a _passphrase.txt_ file with a passphrase in the first line to the [assets](./update/assets/) directory in order to encrypt the site.

### Adjustments

This website has been setup and designed for 3:4 aspect ratio park sign photos and 4:3 aspect ratio landscape photos.
If you have photos with different aspect ratios you will either need to crop them or alter this projects code to get them to display properly.

This project currently utilizes [Google Photos](https://photos.google.com/) image links.
If you would like to use a different method, you will need to alter this projects code.

## Usage

Use the park dropdown in the navbar to filter the type of parks shown.

Clicking on the landscape icon under a park will display the landscape photos for that park.

## Credits

[PageCrypt](https://github.com/MaxLaumeister/pagecrypt) was used for the encryption solution in this project.

## Bugs & Improvements

- Add the ability to filter by searching park names.
- Add logic to reload higher-quality images after lower-quality images have been loaded.
- Implement logic to skip loading images that are taking longer than the average image load time.
- Add retry logic for when images fail to load.
- Needs further testing on a slow network.
- Add a map feature to show all the parks on a map.
