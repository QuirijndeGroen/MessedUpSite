# Messed Up Website

## Description

The webiste uses Django apps for authentication, activities, registration lists and registration list responses. Furthermore it uses some Javascript to have a toggleable darkmode, carousels, open and closing of registration lists and registering/unregistering for activities.

For now, models can only be created from the admin page and thus the admin. A feature for an activity creator on a non-admin page will be implemented in the future.

### Features

Below are some of the key features of the site described.

#### Carousels

Carousels rotate through content automatically or to the selected item if the navigation is pressed. This content is dependant on where in the site the carousel is used.

Carousels are made with the carousel class in a container. In this container the items are added inside. From here a javascript script builds the carousel and its controls.

So far, carousels have been used on the following pages:

- Main page

  The carousel on the main page displays 3 items. A slide about Messed Up and the association, a slide about floorball and the first upcoming activity.

- Members page

  On the members  page there are two carousels used next to each other. One rotates through the upcoming activities and the other rotates through the upcoming tournaments.

- Creation page

  All important models can be created at:

  ```browser
  http://localhost:9000/acccounts/addcontent/
  ```

  This can only be done if the user is part of a committee with sufficient access to the site.

#### Activities

Activities are a model with a few fields that describe all important aspects of a activity. These field are:

- Type: This states the type of activity. So far the options are:
  - Activity
  - Tournament
- Image: Image that is displayed next to the activity
- Title: Title of the activity
- Description: Description of the activity
- Start time: Time that the activity begins
- End time: Time that the activity ends
- Location: Location of the activity
- Organizer: The committee (or other group) that organizes the activity. Note that only this group, next to admins and board, can see the registration list results.

#### Registration list

Registration list are models of forms where users (or non-users) can enter form responses.

Registration lists are linked to an active activity and have a deadline field. Registration lists also have an extra description field for when this is necessary.

Questions are a separate model added as an field of these models. The questions can be any combination of the following types:

- Short text: Text with a limit of ? characters
- Long text: Text with no limit
- Date and Time: a date and time combination
- True/False: either True or False
- Number: Positive integer
- Email: Text with check for e-mail format

All these questions can also have the Required field set to True or False, depending on wether the response for the question is mandatory.

## Getting Started

### Dependencies

The website is Django based. For the database postgresql is used.
The website is dockerized and thus imports the nessisary packages. However to run the dockerfile you will need the Docker software. Also to run the makefile (you could also copy the commands run by this file) you will need make.

Software to install:

- docker
- docker-compose
- make

### Hosting

To make the website:

Download the repo and open a teminal at the root of the project. If you havn't used the site before, build the project. Afterwards run compose start to run the docker image.

```bash
git clone https://github.com/QuirijndeGroen/MessedUpSite.git
cd MessedUpSite
```

```bash
make build #only for first time users
make make-migrations
```

```bash
make start
```

From here search

```browser
http://localhost:9000/
```

on your preferred browser.

If the setup doesn't work the first time, rerun make start. This should fix the sites' database initialization problems.
