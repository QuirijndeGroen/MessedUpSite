# Messed Up Website

Simple overview of use/purpose.

## Description

An in-depth paragraph about your project and overview of use.

## Getting Started

### Dependencies

The website is Django based. For the database postgresql is used and for hosting kerbernetes is used.
The website is dockerized and thus imports the nessisary packages. The website can atleast be made with Docker 29.3.1.

### Hosting

To make the website:

Download the repo and open a teminal at the root of the project. If you havn't used the site before, build the project. Afterwards run compose start to run the docker image.

```bash
git clone https://github.com/QuirijndeGroen/Messed-Up.git
cd MessedUpSite
```

```bash
make build #only for first time users
```

```bash
make compose-start
```

From here search

```browser
http://localhost:9000/
```

on your preferred browser.

## Authors

Quirijn de Groen

## Version History

* 0.1.1
  * Refectored carousels and styles
  * Added automatic carousel rotation
  * Added some new example images
* 0.1.0
  * Initial Release
