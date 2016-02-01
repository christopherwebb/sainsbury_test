## Very simple web scraper

### To run
```
> python scraper.py
```

### Shortcomings of this program
* Will not attempt to parse URLs shortened by a URL service (which in theory can point back to the original site)
* Only parses the raw html it finds. ie the program will not find any links or images inserted by javascript
* No cookie state is kept; in theory this could mean the discovered links differ to those shown to what the host site considers a repeat visitor
* No 'logging in' capabilities; therefore the scraper can't access any areas of the site that are given over to known users (for instance, account pages)
* Doesn't handle a few cases, like id linking and mailtos
