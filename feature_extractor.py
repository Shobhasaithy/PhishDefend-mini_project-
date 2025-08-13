import re
import urllib.parse
import requests
import whois
import tldextract
from bs4 import BeautifulSoup
from datetime import datetime
import numpy as np
import logging
from urllib.parse import urlparse

class FeatureExtractor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.features = []
        self.feature_names = [
            'has_ip', 'url_length', 'shortened_url', 'has_at_symbol',
            'double_slash_redirect', 'prefix_suffix', 'sub_domains',
            'ssl_final_state', 'domain_registration_length', 'favicon',
            'port', 'https_token', 'request_url', 'url_of_anchor',
            'links_in_tags', 'sfh', 'email_submit', 'abnormal_url',
            'redirect', 'mouseover', 'right_click', 'popup',
            'iframe', 'domain_age', 'dns_record', 'web_traffic',
            'page_rank', 'google_index', 'links_pointing',
            'statistical_report'
        ]

    def extract_features(self, url):
        """Extract features from the given URL."""
        try:
            self.features = []
            self.url = url
            
            # Basic URL features
            self.features.append(self._has_ip())
            self.features.append(self._url_length())
            self.features.append(self._shortened_url())
            self.features.append(self._has_at_symbol())
            self.features.append(self._has_double_slash_redirect())
            self.features.append(self._has_prefix_suffix())
            self.features.append(self._count_subdomains())
            
            # SSL/HTTPS features
            self.features.append(self._check_ssl())
            
            # Domain-based features
            domain_features = self._get_domain_features()
            self.features.extend(domain_features)
            
            # HTML and JavaScript based Features
            html_features = self._get_html_features()
            self.features.extend(html_features)
            
            # Fill remaining features with -1 (unknown/error)
            while len(self.features) < len(self.feature_names):
                self.features.append(-1)
                
            return np.array(self.features).reshape(1, -1)
            
        except Exception as e:
            self.logger.error(f"Error extracting features: {str(e)}")
            return np.array([-1] * len(self.feature_names)).reshape(1, -1)

    def _has_ip(self):
        """Check if URL contains IP address."""
        ip_pattern = r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
        return 1 if re.search(ip_pattern, self.url) else 0

    def _url_length(self):
        """Check URL length."""
        return 1 if len(self.url) > 75 else 0

    def _shortened_url(self):
        """Check if URL is shortened."""
        shortening_services = ['bit.ly', 'goo.gl', 't.co', 'tinyurl.com']
        return 1 if any(service in self.url for service in shortening_services) else 0

    def _has_at_symbol(self):
        """Check for @ symbol in URL."""
        return 1 if '@' in self.url else 0

    def _has_double_slash_redirect(self):
        """Check for // redirect."""
        return 1 if '//' in self.url[7:] else 0

    def _has_prefix_suffix(self):
        """Check for prefix or suffix separator."""
        return 1 if '-' in urlparse(self.url).netloc else 0

    def _count_subdomains(self):
        """Count number of subdomains."""
        ext = tldextract.extract(self.url)
        subdomains = ext.subdomain.split('.')
        return 1 if len(subdomains) > 2 else 0

    def _check_ssl(self):
        """Check SSL certificate."""
        return 1 if self.url.startswith('https') else 0

    def _get_domain_features(self):
        """Extract domain-based features."""
        try:
            domain = urlparse(self.url).netloc
            w = whois.whois(domain)
            
            # Domain age
            if isinstance(w.creation_date, list):
                creation_date = w.creation_date[0]
            else:
                creation_date = w.creation_date
                
            if creation_date:
                age = (datetime.now() - creation_date).days
                domain_age = 1 if age > 365 else 0
            else:
                domain_age = -1
                
            # DNS record
            dns_record = 1 if w.domain_name else 0
            
            return [domain_age, dns_record]
            
        except Exception as e:
            self.logger.error(f"Error getting domain features: {str(e)}")
            return [-1, -1]

    def _get_html_features(self):
        """Extract HTML and JavaScript based features."""
        try:
            response = requests.get(self.url, timeout=5, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check for iframes
            iframe = 1 if len(soup.find_all('iframe')) > 0 else 0
            
            # Check for right click disabled
            right_click = 1 if 'oncontextmenu="return false"' in response.text.lower() else 0
            
            # Check for popup windows
            popup = 1 if 'window.open' in response.text.lower() else 0
            
            # Check for form handler
            sfh = 1 if len(soup.find_all('form', action=True)) > 0 else 0
            
            return [iframe, right_click, popup, sfh]
            
        except Exception as e:
            self.logger.error(f"Error getting HTML features: {str(e)}")
            return [-1, -1, -1, -1]
