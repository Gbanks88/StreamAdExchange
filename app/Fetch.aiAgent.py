# Import required libraries
from cosmpy.aerial.client import LedgerClient, NetworkConfig  # For Fetch.ai integration
from cosmpy.aerial.wallet import LocalWallet  # For wallet management
from cosmpy.crypto.keypairs import PrivateKey  # For cryptographic operations
import json  # For JSON data handling
import os  # For file and directory operations
from bs4 import BeautifulSoup  # For HTML parsing
import requests  # For making HTTP requests
from typing import Dict, List  # For type hinting
import logging  # For logging operations

class WebPageOptimizer:
    """A class to optimize web pages using Fetch.ai integration"""
    
    def __init__(self):
        """Initialize the WebPageOptimizer with necessary configurations"""
        # Set up Fetch.ai client on testnet
        self.client = LedgerClient(NetworkConfig.fetchai_stable_testnet())
        # Initialize wallet
        self._init_wallet()
        # Set template directory path relative to current file
        self.template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        # Set up logging
        self.setup_logging()
        
    def setup_logging(self):
        """Configure logging settings for the optimizer"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def _init_wallet(self):
        """Initialize a test wallet for Fetch.ai operations"""
        private_key = PrivateKey()  # Generate new private key
        self.wallet = LocalWallet(private_key)  # Create wallet with private key

    def optimize_all_pages(self):
        """Process and optimize all HTML pages in the templates directory"""
        optimized_pages = {}
        
        # Iterate through all HTML files in template directory
        for filename in os.listdir(self.template_dir):
            if filename.endswith('.html'):
                file_path = os.path.join(self.template_dir, filename)
                optimized_pages[filename] = self.optimize_page(file_path)
                
        return optimized_pages

    def optimize_page(self, file_path):
        """Optimize a single web page"""
        # Read the HTML file
        with open(file_path, 'r') as file:
            content = file.read()
            
        # Parse HTML content
        soup = BeautifulSoup(content, 'html.parser')
        
        # Apply various optimizations
        optimized = {
            'layout': self.optimize_layout(soup),
            'styling': self.optimize_styling(soup),
            'content': self.optimize_content(soup),
            'performance': self.check_performance(soup)
        }
        
        return optimized

    def optimize_layout(self, soup):
        """Optimize the layout structure of the page"""
        layout_fixes = {
            'header_fixes': self.fix_headers(soup),
            'navigation_fixes': self.fix_navigation(soup),
            'content_structure': self.fix_content_structure(soup),
            'card_layout': self.optimize_cards(soup)
        }
        return layout_fixes

    def fix_headers(self, soup):
        """Apply consistent styling to header elements"""
        headers = soup.find_all(['h1', 'h2', 'h3'])
        fixes = []
        
        for header in headers:
            # Add section-title class to headers
            header['class'] = header.get('class', []) + ['section-title']
            fixes.append(f"Optimized header: {header.text}")
            
        return fixes

    def fix_navigation(self, soup):
        """Optimize navigation elements"""
        nav = soup.find('nav')
        if nav:
            # Add navigation background class
            nav['class'] = nav.get('class', []) + ['nav-with-bg']
            return "Navigation optimized with consistent styling"
        return "No navigation found"

    def optimize_cards(self, soup):
        """Optimize card components with consistent styling and hover effects"""
        cards = soup.find_all(['div'], class_=lambda x: x and 'card' in x)
        fixes = []
        
        for card in cards:
            # Add consistent card styling
            card['class'] = card.get('class', []) + ['hub-card']
            
            # Add card header if missing
            if not card.find('div', class_='card-header'):
                header = soup.new_tag('div', attrs={'class': 'card-header'})
                card.insert(0, header)
            
            # Add hover effects
            card['onmouseover'] = "this.style.transform='translateY(-5px)'"
            card['onmouseout'] = "this.style.transform='translateY(0)'"
            
            fixes.append(f"Optimized card: {card.get('id', 'unnamed-card')}")
        
        return fixes

    def save_optimizations(self, file_path, optimizations):
        """Save optimized changes with backup functionality"""
        # Create backup of original file
        backup_path = file_path + '.backup'
        with open(file_path, 'r') as source:
            with open(backup_path, 'w') as backup:
                backup.write(source.read())

        try:
            # Apply optimizations and save
            with open(file_path, 'r') as file:
                content = file.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            self.apply_layout_fixes(soup, optimizations['layout'])
            self.apply_styling_fixes(soup, optimizations['styling'])
            self.apply_content_fixes(soup, optimizations['content'])
            
            # Save optimized content
            with open(file_path, 'w') as file:
                file.write(str(soup.prettify()))
                
            self.logger.info(f"Successfully optimized {file_path}")
            
        except Exception as e:
            # Restore from backup if error occurs
            self.logger.error(f"Error optimizing {file_path}: {str(e)}")
            with open(backup_path, 'r') as backup:
                with open(file_path, 'w') as file:
                    file.write(backup.read())
            self.logger.info(f"Restored {file_path} from backup")

    def apply_optimizations(self):
        """Apply optimizations to all pages"""
        try:
            # Get optimizations for all pages
            optimized_pages = self.optimize_all_pages()
            
            # Save optimizations for each page
            for filename, optimizations in optimized_pages.items():
                file_path = os.path.join(self.template_dir, filename)
                self.save_optimizations(file_path, optimizations)
                
            self.logger.info("Successfully optimized all pages")
            return "All pages optimized successfully"
            
        except Exception as e:
            self.logger.error(f"Error during optimization: {str(e)}")
            return f"Error: {str(e)}"

    def apply_layout_fixes(self, soup, layout_fixes):
        """Apply layout optimizations"""
        # Fix headers
        for header in soup.find_all(['h1', 'h2', 'h3']):
            header['class'] = header.get('class', []) + ['section-title']
            
        # Fix navigation
        nav = soup.find('nav')
        if nav:
            nav['class'] = nav.get('class', []) + ['nav-with-bg']
            
        # Fix content structure
        main = soup.find('main') or soup.find('div', class_='content')
        if main:
            main['class'] = main.get('class', []) + ['main-content']

    def apply_styling_fixes(self, soup, styling_fixes):
        """Apply styling optimizations"""
        # Add consistent button styling
        for button in soup.find_all('button'):
            button['class'] = button.get('class', []) + ['hub-link']
            
        # Add consistent link styling
        for link in soup.find_all('a'):
            link['class'] = link.get('class', []) + ['nav-link']

    def apply_content_fixes(self, soup, content_fixes):
        """Apply content optimizations"""
        # Improve text readability
        for p in soup.find_all('p'):
            p['class'] = p.get('class', []) + ['readable-text']

    def optimize_styling(self, soup):
        """Apply consistent styling across pages"""
        elements = soup.find_all(['div', 'section'])
        style_fixes = []
        
        for element in elements:
            if 'card' in str(element.get('class', [])):
                element['class'] = element.get('class', []) + ['hub-card']
                style_fixes.append(f"Applied consistent card styling to {element.get('id', 'unnamed-card')}")
                
        return style_fixes

    def optimize_content(self, soup):
        """Optimize content presentation"""
        content_fixes = {
            'readability': self.improve_readability(soup),
            'consistency': self.ensure_consistency(soup)
        }
        return content_fixes

    def improve_readability(self, soup):
        """Improve content readability"""
        paragraphs = soup.find_all('p')
        fixes = []
        
        for p in paragraphs:
            p['class'] = p.get('class', []) + ['readable-text']
            fixes.append("Applied readable text styling")
            
        return fixes

    def ensure_consistency(self, soup):
        """Ensure consistent styling and formatting"""
        elements = soup.find_all(['button', 'a'])
        fixes = []
        
        for element in elements:
            if element.name == 'button':
                element['class'] = element.get('class', []) + ['hub-link']
            elif element.name == 'a':
                element['class'] = element.get('class', []) + ['nav-link']
            fixes.append(f"Applied consistent styling to {element.name}")
            
        return fixes

    def check_performance(self, soup):
        """Check page performance metrics"""
        metrics = {
            'element_count': len(soup.find_all()),
            'image_count': len(soup.find_all('img')),
            'script_count': len(soup.find_all('script')),
            'recommendations': self.get_performance_recommendations(soup)
        }
        return metrics

    def get_performance_recommendations(self, soup):
        """Generate performance recommendations"""
        recommendations = []
        
        # Check image optimization
        images = soup.find_all('img')
        if len(images) > 5:
            recommendations.append("Consider lazy loading for images")
            
        # Check script loading
        scripts = soup.find_all('script')
        if len(scripts) > 3:
            recommendations.append("Consider deferring non-critical scripts")
            
        return recommendations

    def fix_content_structure(self, soup):
        """Fix and optimize the content structure of the page"""
        try:
            # Find main content container
            main_content = soup.find('main') or soup.find('div', class_='content-container')
            if not main_content:
                # Create main content container if it doesn't exist
                main_content = soup.new_tag('main')
                main_content['class'] = ['main-content']
                
                # Move body content into main
                for element in soup.body.contents:
                    if element.name and element.name != 'nav' and element.name != 'footer':
                        main_content.append(element)
                
                soup.body.append(main_content)

            # Add proper section structure
            sections = soup.find_all('section') or soup.find_all('div', class_=lambda x: x and 'section' in str(x))
            for section in sections:
                if 'section' not in str(section.get('class', [])):
                    section['class'] = section.get('class', []) + ['content-section']

            # Fix content spacing
            content_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            for element in content_elements:
                if not element.get('class'):
                    element['class'] = []
                if element.name.startswith('h'):
                    element['class'].append('section-title')
                else:
                    element['class'].append('readable-text')

            return "Content structure optimized successfully"
            
        except Exception as e:
            self.logger.error(f"Error fixing content structure: {str(e)}")
            return f"Error in content structure: {str(e)}"

def main():
    """Main entry point for the optimizer"""
    optimizer = WebPageOptimizer()
    result = optimizer.apply_optimizations()
    print(result)

if __name__ == "__main__":
    main()
