from HTMLParser import HTMLParser
import urllib
import urlparse
import pprint

class MyHTMLParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        # HTMLParser is an old style class
        HTMLParser.__init__(self)
        
        self.links = []
        self.images = []
        self.css = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self.links.append(attr[1])

        elif tag == 'img':
            for attr in attrs:
                if attr[0] == 'src':
                    self.images.append(attr[1])

        elif tag == 'link':
            is_stylesheet = False
            src = ''
            for attr in attrs:
                if attr[0] == 'rel':
                    is_stylesheet = 'stylesheet' in attr[1]
                elif attr[0] == 'href':
                    src = attr[1]

            if src and is_stylesheet:
                self.css.append(src)
            elif src:
                self.links.append(src)


        # elif tag == 'link':
        #     for attr in attrs:
        #         if attr[0] == 'src':
        #             self.images.append(attr[1])


class SiteMapGenerator(object):
    def __init__(self, begin_url):
        self.begin_url = begin_url
        self.parsed_url = urlparse.urlparse(begin_url)
        self.urls = {self.begin_url}
        self.processed_links = []

        self.internal_pages = set()
        self.static_content = set()
        self.external_pages = set()
        self.emails = set()

    def Process(self):
        while len(self.processed_links) < len(self.urls):
            next_url = [url for url in self.urls if url not in self.processed_links][0]
            self.processed_links.append(next_url)

            # are we dealing with an external url?
            if not self.SameSite(next_url):
                self.external_pages.update([next_url])
                continue

            self.__ParseUrl(next_url)

    def __ParseUrl(self, url):
        reqResponse = urllib.urlopen(url)

        print 'scraping: %s' % url

        if (reqResponse.getcode() >= 400):
            return

        encoding = reqResponse.headers.getparam('charset')
        if encoding:
            parsed_data = reqResponse.read().decode(encoding)
        else:
            parsed_data = reqResponse.read()

        parser = MyHTMLParser()
        parser.feed(parsed_data)

        self.emails.update([url for url in parser.links if url.startswith('mailto:')])

        # don't parse any mailto links, as they'll throw the MakeUrlAbsolute method
        mail_free_links = [url for url in parser.links if not url.startswith('mailto:')]

        # add found links, turning relative URLs into absolute URLs
        self.urls.update([self.ProcessUrl(link) for link in mail_free_links])

        self.static_content.update(parser.images)
        self.static_content.update(parser.css)
        
        # Add the url we ended up being redirected to
        self.internal_pages.update([reqResponse.geturl()])

    def SameSite(self, url):
        original_net_loc_split = self.parsed_url.netloc.split('.')
        checking_net_loc_split = urlparse.urlparse(url).netloc.split('.')
        
        # check that the site is in the same, handling the case where we may
        # have abc.com and www.abc.com urls
        if self.parsed_url.netloc == urlparse.urlparse(url).netloc:
            return True

        if (
            len(original_net_loc_split) > 1 and
            len(checking_net_loc_split) > 1 and
            original_net_loc_split[-1] == checking_net_loc_split[-1] and
            original_net_loc_split[-2] == checking_net_loc_split[-2]
        ):
            if original_net_loc_split[0] == 'www' or checking_net_loc_split[0] == 'www':
                return True

        return False

    def ProcessUrl(self, url):
        # Remove the single fragment identifier
        # (we only have to worry about everything before the identifier, as
        # indicated in https://tools.ietf.org/html/rfc3986)
        url = url.split('#')[0]

        return self.MakeUrlAbsolute(url)

    def MakeUrlAbsolute(self, url):
        parsed_link = urlparse.urlparse(url)
        if not parsed_link.netloc:
            if url.startswith('/'):
                url = url[1:]
            return '%s://%s/%s' % (self.parsed_url.scheme, self.parsed_url.netloc, url)
        else:
            return url

if __name__ == '__main__':
    begin_url = 'http://www.wiprodigital.com'
    generator = SiteMapGenerator(begin_url)

    generator.Process()

    print 'Internal pages: %s' % generator.internal_pages
    print 'Static content URLs: %s' % generator.static_content
    print 'External pages: %s' % generator.external_pages
    print 'Email links: %s' % generator.emails
