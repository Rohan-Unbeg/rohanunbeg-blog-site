#!/usr/bin/env python3
import os
import re
import sys
import argparse
import shutil
import glob
import traceback
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

class BlogAutomator:
    def __init__(self, base_dir="."):
        self.base_dir = Path(base_dir)
        self.blog_dir = self.base_dir / "blog"
        self.images_dir = self.base_dir / "images"
        
        self.blog_dir.mkdir(exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)
        
        self.categories = {
            "AI Tools": "ai",
            "Dev Tools": "dev",
            "Tech News": "tech",
            "Tutorials": "tutorials"
        }
    
    def create_post(self, title, category, content=None, image=None):
        try:
            print("Starting create_post...")
            category_slug = self.categories.get(category, self._generate_slug(category))
            if category not in self.categories:
                self.categories[category] = category_slug
                print(f"Added new category: {category} with slug: {category_slug}")
            
            slug = self._generate_slug(title)
            post_filename = f"{slug}.html"
            post_path = self.blog_dir / post_filename
            
            if post_path.exists():
                count = 1
                while post_path.exists():
                    post_filename = f"{slug}-{count}.html"
                    post_path = self.blog_dir / post_filename
                    count += 1
            
            final_slug = post_filename[:-5] if post_filename.endswith('.html') else post_filename
            
            # Get placeholder image if none provided
            if not image:
                # Use images directly from the images folder
                images = [img for img in os.listdir(str(self.images_dir)) if img.endswith(('.jpg', '.png', '.jpeg')) and img != 'profile.jpg']
                if images:
                    image = f"../images/{images[0]}"
                else:
                    image = "../images/default-post.jpg"
            
            # --- FIX: Support direct markdown content or file path ---
            md_content = None
            if content:
                if os.path.isfile(content):
                    with open(content, 'r', encoding='utf-8') as f:
                        md_content = f.read()
                else:
                    # Replace literal '\n' with actual newlines for CLI input
                    md_content = content.replace('\\n', '\n')
            
            soup = BeautifulSoup('<!DOCTYPE html><html lang="en"><head></head><body></body></html>', 'html.parser')
            head = soup.head
            body = soup.body
            
            # Add meta tags
            meta_charset = soup.new_tag('meta', charset='UTF-8')
            meta_viewport = soup.new_tag('meta', attrs={'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'})
            head.append(meta_charset)
            head.append(meta_viewport)
            
            # Add title
            title_tag = soup.new_tag('title')
            title_tag.string = f"{title} | Rohan Unbeg"
            head.append(title_tag)
            
            # Add minified CSS
            link_css = soup.new_tag('link', rel='stylesheet', href='../css/styles.min.css')
            head.append(link_css)
            
            # Add Font Awesome
            link_fa = soup.new_tag('link', rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css')
            head.append(link_fa)
            
            # Add Google Fonts
            link_fonts = soup.new_tag('link', rel='stylesheet', href='https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap')
            head.append(link_fonts)
            
            # --- DYNAMIC SEO GENERATION START ---
            # Generate meta description from content (first 150 chars, no markdown)
            import re
            def strip_markdown(md):
                # Remove markdown links/images/code/formatting
                text = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', md)
                text = re.sub(r'\[[^\]]*\]\([^)]*\)', '', text)
                text = re.sub(r'`[^`]+`', '', text)
                text = re.sub(r'[\*_#>`~\-]', '', text)
                text = re.sub(r'\s+', ' ', text)
                return text.strip()
            
            meta_description = None
            meta_keywords = None
            if md_content:
                stripped_text = strip_markdown(md_content)
                meta_description = f"Discover the latest insights on {title} within the {category} category. Enhance your skills with Rohan Unbeg's expert analysis."
                # Generate keywords (prioritize words > 3 chars)
                words = re.findall(r'\w+', stripped_text.lower())
                keywords_list = [w for w in words if len(w) > 3][:10]
                keywords_str = ', '.join(keywords_list)
                # Add category-specific niche keywords for AI & Developer Productivity Tools
                niche_keywords = {
                    'AI Tools': 'AI tools, artificial intelligence, machine learning, developer AI, coding automation',
                    'Dev Tools': 'developer tools, programming software, coding tools, software development, productivity apps',
                    'Tech News': 'tech news, technology updates, AI trends, developer news, software industry',
                    'Tutorials': 'coding tutorials, developer guides, AI tutorials, programming tips, tech learning'
                }
                category_keywords = niche_keywords.get(category, 'developer tools, AI productivity, coding efficiency, tech tools')
                keywords_str = f'{keywords_str}, {category_keywords}' if keywords_str else category_keywords
                meta_keywords = keywords_str
            else:
                meta_description = f"Discover the latest insights on {title} within the {category} category. Enhance your skills with Rohan Unbeg's expert analysis."
                # Use category-specific niche keywords even for fallback
                niche_keywords = {
                    'AI Tools': 'AI tools, artificial intelligence, machine learning, developer AI, coding automation',
                    'Dev Tools': 'developer tools, programming software, coding tools, software development, productivity apps',
                    'Tech News': 'tech news, technology updates, AI trends, developer news, software industry',
                    'Tutorials': 'coding tutorials, developer guides, AI tutorials, programming tips, tech learning'
                }
                category_keywords = niche_keywords.get(category, 'developer tools, AI productivity, coding efficiency, tech tools')
                meta_keywords = f"{title}, {category}, Rohan Unbeg, blog, article, {category_keywords}"
            # Canonical URL
            canonical_url = f"https://rohanunbeg.com/blog/{final_slug}.html"
            # OpenGraph/Twitter image fallback
            og_image = image.replace('..','https://rohanunbeg.com') if image.startswith('..') else image
            # --- DYNAMIC SEO TAGS ---
            meta_desc_tag = soup.new_tag('meta', attrs={'name':'description','content':meta_description})
            meta_keywords_tag = soup.new_tag('meta', attrs={'name':'keywords','content':meta_keywords})
            meta_robots_tag = soup.new_tag('meta', attrs={'name':'robots','content':'index, follow'})
            link_canonical = soup.new_tag('link', rel='canonical', href=canonical_url)
            og_type = soup.new_tag('meta', property='og:type', content='article')
            og_title = soup.new_tag('meta', property='og:title', content=f"{title} | Rohan Unbeg")
            og_desc = soup.new_tag('meta', property='og:description', content=meta_description)
            og_url = soup.new_tag('meta', property='og:url', content=canonical_url)
            og_img = soup.new_tag('meta', property='og:image', content=og_image)
            tw_card = soup.new_tag('meta', attrs={'name':'twitter:card', 'content':'summary_large_image'})
            tw_title = soup.new_tag('meta', attrs={'name':'twitter:title', 'content':f"{title} | Rohan Unbeg"})
            tw_desc = soup.new_tag('meta', attrs={'name':'twitter:description', 'content':meta_description})
            tw_img = soup.new_tag('meta', attrs={'name':'twitter:image', 'content':og_image})
            # JSON-LD Article schema
            import json
            article_ld = {
                "@context": "https://schema.org",
                "@type": "BlogPosting",
                "headline": title,
                "description": meta_description,
                "image": og_image,
                "author": {"@type": "Person", "name": "Rohan Unbeg"},
                "publisher": {"@type": "Person", "name": "Rohan Unbeg"},
                "datePublished": datetime.now().strftime('%Y-%m-%dT%H:%M:%S+05:30'),
                "mainEntityOfPage": canonical_url,
                "keywords": meta_keywords,
                "inLanguage": "en"
            }
            script_ld = soup.new_tag('script', type='application/ld+json')
            script_ld.string = json.dumps(article_ld, indent=2)
            # Insert SEO tags
            head.append(meta_desc_tag)
            head.append(meta_keywords_tag)
            head.append(meta_robots_tag)
            head.append(link_canonical)
            head.append(og_type)
            head.append(og_title)
            head.append(og_desc)
            head.append(og_url)
            head.append(og_img)
            head.append(tw_card)
            head.append(tw_title)
            head.append(tw_desc)
            head.append(tw_img)
            head.append(script_ld)
            # --- DYNAMIC SEO GENERATION END ---
            
            # Add header (navbar) using BeautifulSoup (parsed HTML)
            header_html = self._get_navbar_html()
            header_soup = BeautifulSoup(header_html, "html.parser")
            body.insert(0, header_soup)
            # Main content
            main = soup.new_tag('main')
            article = soup.new_tag('article')
            post_layout = soup.new_tag('div', attrs={'class': 'post-layout'})
            main_col = soup.new_tag('div', attrs={'class': 'post-main'})
            # Heading right at the top
            h1 = soup.new_tag('h1')
            h1.string = title
            main_col.append(h1)
            # Meta row directly after heading
            meta_row = soup.new_tag('div', attrs={'class': 'post-meta-row'})
            date_span = soup.new_tag('span', attrs={'class': 'meta-item'})
            date_icon = soup.new_tag('i', attrs={'class': 'far fa-calendar'})
            date_span.append(date_icon)
            date_span.append(f" {datetime.now().strftime('%B %d, %Y')}")
            read_span = soup.new_tag('span', attrs={'class': 'meta-item'})
            read_icon = soup.new_tag('i', attrs={'class': 'far fa-clock'})
            read_span.append(read_icon)
            read_span.append(" 5 min read")
            cat_span = soup.new_tag('span', attrs={'class': 'meta-item'})
            cat_icon = soup.new_tag('i', attrs={'class': 'far fa-folder'})
            cat_span.append(cat_icon)
            cat_span.append(f" {category}")
            meta_row.append(date_span)
            meta_row.append(read_span)
            meta_row.append(cat_span)
            main_col.append(meta_row)
            # Featured image and post content as before
            featured_image_div = soup.new_tag('div', attrs={'class': 'post-featured-image'})
            featured_img = soup.new_tag('img', src=image or '../images/hero-bg.jpg', alt=title)
            featured_image_div.append(featured_img)
            main_col.append(featured_image_div)
            post_content_div = soup.new_tag("div", attrs={"class": "post-content"})
            if md_content:
                try:
                    import markdown
                    html_content = markdown.markdown(md_content, extensions=["fenced_code", "tables", "codehilite", "nl2br", "sane_lists", "toc"])
                    post_content_div.append(BeautifulSoup(html_content, "html.parser"))
                except Exception as e:
                    error_p = soup.new_tag("p")
                    error_p.string = f"Error processing markdown: {e}"
                    post_content_div.append(error_p)
            else:
                no_content_p = soup.new_tag("p")
                no_content_p.string = "No content provided."
                post_content_div.append(no_content_p)
            main_col.append(post_content_div)
            sidebar = soup.new_tag('aside', attrs={'class': 'sidebar'})
            sidebar.append(self._get_recent_posts_sidebar(soup, exclude_slug=final_slug))
            sidebar.append(self._get_featured_posts_sidebar(soup, exclude_slug=final_slug))
            post_layout.append(main_col)
            post_layout.append(sidebar)
            article.append(post_layout)
            main.append(article)
            body.append(main)
            
            # CTA section
            cta = soup.new_tag('section', attrs={'class': 'cta'})
            cta_container = soup.new_tag('div', attrs={'class': 'container'})
            cta_content = soup.new_tag('div', attrs={'class': 'cta-content'})
            cta_h2 = soup.new_tag('h2')
            cta_h2.string = 'Stay Updated'
            cta_p = soup.new_tag('p')
            cta_p.string = 'Join our newsletter for the latest AI and dev tool insights.'
            newsletter_form = soup.new_tag('div', attrs={'class': 'newsletter-form'})
            email_input = soup.new_tag('input', type='email', attrs={'placeholder': 'Enter your email'})
            subscribe_button = soup.new_tag('button', attrs={'class': 'btn'})
            subscribe_button.string = 'Subscribe'
            newsletter_form.append(email_input)
            newsletter_form.append(subscribe_button)
            cta_content.append(cta_h2)
            cta_content.append(cta_p)
            cta_content.append(newsletter_form)
            cta_container.append(cta_content)
            cta.append(cta_container)
            body.append(cta)
            
            # Add footer
            footer = self._create_footer(soup)
            body.append(footer)
            
            # Add main.min.js script for future posts
            script_main = soup.new_tag('script', src='../js/main.min.js')
            body.append(script_main)
            
            # Write to file
            with open(post_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
                print(f"Successfully wrote to {post_path.relative_to(self.base_dir)}")
            
            # Update site pages (blog.html, index.html, etc.)
            self._update_blog_page(final_slug, title, category, category_slug)
            self._update_index_page(final_slug, title, category, category_slug, content)
            
            print(f"Created new blog post: {post_path}")
            
            # After creating post, update all sidebars
            self.update_all_sidebars()
            
            return True
        except Exception as e:
            print(f"Error in create_post: {str(e)}")
            traceback.print_exc()
            return False

    def _parse_inline_markdown(self, text, soup):
        """
        Parse inline markdown for bold, italic, code, and images within a line of text.
        Returns a list of BeautifulSoup elements and strings.
        """
        import re
        elements = []
        # Regex for inline code, images, bold, italic
        # The previous regex was broken due to linebreaks and incomplete groups. Fix:
        pattern = re.compile(r'(`[^`]+`|!\[[^\]]*\]\([^\)]+\)|\*\*.+?\*\*|__.+?__|\*.+?\*|_.+?_)')
        pos = 0
        for match in pattern.finditer(text):
            start, end = match.span()
            if start > pos:
                elements.append(text[pos:start])
            token = match.group(0)
            if token.startswith('`'):
                code = soup.new_tag('code', **{'class': 'markdown-inline-code'})
                code.string = token[1:-1]
                elements.append(code)
            elif token.startswith('!['):
                # ![alt](src)
                img_match = re.match(r'!\[([^\]]*)\]\(([^\)]+)\)', token)
                if img_match:
                    alt, src = img_match.groups()
                    img = soup.new_tag('img', src=src, alt=alt)
                    elements.append(img)
                else:
                    elements.append(token)
            elif token.startswith('**') or token.startswith('__'):
                strong = soup.new_tag('strong')
                strong.string = token[2:-2]
                elements.append(strong)
            elif token.startswith('*') or token.startswith('_'):
                em = soup.new_tag('em')
                em.string = token[1:-1]
                elements.append(em)
            else:
                elements.append(token)
            pos = end
        if pos < len(text):
            elements.append(text[pos:])
        return elements

    def _create_header(self, soup):
        header = soup.new_tag('header')
        container = soup.new_tag('div', attrs={'class': 'container'})
        
        # Logo
        logo = soup.new_tag('div', attrs={'class': 'logo'})
        logo_link = soup.new_tag('a', href='../index.html')
        logo_link.string = 'Rohan Unbeg'
        logo.append(logo_link)
        
        # Navigation
        nav = soup.new_tag('nav')
        nav_list = soup.new_tag('ul', attrs={'class': 'nav-links'})
        nav_items = [
            ('Home', '../index.html'),
            ('Blog', '../blog.html', 'active'),
            ('About', '../about.html'),
            ('Contact', '../contact.html')
        ]
        for text, href, *cls in nav_items:
            li = soup.new_tag('li')
            a = soup.new_tag('a', href=href)
            if cls:
                a['class'] = cls[0]
            a.string = text
            li.append(a)
            nav_list.append(li)
        
        nav.append(nav_list)
        container.append(logo)
        container.append(nav)
        header.append(container)
        return header

    def _create_blog_header(self, soup, title, description):
        section = soup.new_tag('section', attrs={'class': 'blog-header'})
        container = soup.new_tag('div', attrs={'class': 'container'})
        h1 = soup.new_tag('h1')
        h1.string = title
        p = soup.new_tag('p')
        p.string = description
        container.append(h1)
        container.append(p)
        section.append(container)
        return section

    def _get_recent_posts_sidebar(self, soup, exclude_slug=None, max_posts=3):
        sidebar_section = soup.new_tag('section')
        h3 = soup.new_tag('h3')
        h3.string = 'Recent Posts'
        sidebar_section.append(h3)
        posts_list = soup.new_tag('ul', attrs={'class': 'sidebar-posts-list'})
        recent_posts = self._get_recent_posts(exclude_slug=exclude_slug, max_posts=max_posts)
        for post in recent_posts:
            li = soup.new_tag('li')
            a = soup.new_tag('a', href=f'/blog/{post["slug"]}.html')
            a.string = post['title']
            li.append(a)
            posts_list.append(li)
        sidebar_section.append(posts_list)
        return sidebar_section

    def _get_featured_posts_sidebar(self, soup, exclude_slug=None, max_posts=2):
        sidebar_section = soup.new_tag('section')
        h3 = soup.new_tag('h3')
        h3.string = 'Featured Posts'
        sidebar_section.append(h3)
        posts_list = soup.new_tag('ul', attrs={'class': 'sidebar-posts-list'})
        featured_posts = self._get_featured_posts(exclude_slug=exclude_slug, max_posts=max_posts)
        for post in featured_posts:
            li = soup.new_tag('li')
            a = soup.new_tag('a', href=f'/blog/{post["slug"]}.html')
            a.string = post['title']
            li.append(a)
            posts_list.append(li)
        sidebar_section.append(posts_list)
        return sidebar_section

    def _get_featured_posts(self, exclude_slug=None, max_posts=2):
        # For now, just return the most recent posts as 'featured'
        return self._get_recent_posts(exclude_slug=exclude_slug, max_posts=max_posts)

    def _get_recent_posts(self, exclude_slug=None, max_posts=3):
        # Get recent posts for related posts section
        posts = []
        for html_file in sorted(self.blog_dir.glob('*.html'), reverse=True):
            slug = html_file.stem
            if slug == exclude_slug:
                continue
            with open(html_file, encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                title_tag = soup.find('h1')
                title = title_tag.text.strip() if title_tag else slug
                posts.append({'slug': slug, 'title': title})
            if len(posts) >= max_posts:
                break
        return posts

    def _create_footer(self, soup):
        footer = soup.new_tag('footer')
        container = soup.new_tag('div', attrs={'class': 'container'})
        footer_content = soup.new_tag('div', attrs={'class': 'footer-content'})
        
        footer_logo = soup.new_tag('div', attrs={'class': 'footer-logo'})
        logo_link = soup.new_tag('a', href='../index.html')
        logo_link.string = 'Rohan Unbeg'
        footer_logo.append(logo_link)
        
        tagline = soup.new_tag('p')
        tagline.string = 'Exploring the future of AI & Dev Tools'
        footer_logo.append(tagline)
        footer_content.append(footer_logo)
        
        footer_links = soup.new_tag('div', attrs={'class': 'footer-links'})
        for section_title, links in [
            ('Navigation', [
                ('Home', '../index.html'),
                ('Blog', '../blog.html'),
                ('About', '../about.html'),
                ('Contact', '../contact.html')
            ]),
            ('Categories', [
                ('AI Tools', '../blog.html?category=ai'),
                ('Dev Tools', '../blog.html?category=dev'),
                ('Tech News', '../blog.html?category=tech'),
                ('Tutorials', '../blog.html?category=tutorials')
            ]),
            ('Connect', [
                ('Twitter', 'https://twitter.com/rohanunbeg', True),
                ('GitHub', 'https://github.com/rohanunbeg', True),
                ('LinkedIn', 'https://linkedin.com/in/rohanunbeg', True)
            ])
        ]:
            group = soup.new_tag('div', attrs={'class': 'links-group'})
            h3 = soup.new_tag('h3')
            h3.string = section_title
            group.append(h3)
            
            ul = soup.new_tag('ul')
            for link_text, href, *is_external in links:
                li = soup.new_tag('li')
                a = soup.new_tag('a', href=href)
                if is_external and is_external[0]:
                    a['target'] = '_blank'
                a.string = link_text
                li.append(a)
                ul.append(li)
            group.append(ul)
            footer_links.append(group)
        
        footer_content.append(footer_links)
        container.append(footer_content)
        
        footer_bottom = soup.new_tag('div', attrs={'class': 'footer-bottom'})
        copyright = soup.new_tag('p')
        copyright.string = f'  {datetime.now().year} Rohan Unbeg. All rights reserved.'
        footer_bottom.append(copyright)
        container.append(footer_bottom)
        
        footer.append(container)
        return footer

    def _icon_text(self, soup, icon, text):
        span = soup.new_tag('span')
        i = soup.new_tag('i', attrs={'class': icon})
        span.append(i)
        span.append(f' {text}')
        return span

    def _generate_slug(self, title):
        return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    
    def _get_placeholder_image(self, idx=None):
        # Return a placeholder image path from the images folder, excluding profile.jpg
        images = [img for img in os.listdir(str(self.images_dir)) if img.endswith('.jpg') and img != 'profile.jpg']
        images.sort()
        if not images:
            return 'images/default-post.jpg'
        if idx is not None:
            return f'images/{images[idx % len(images)]}'
        import random
        return f'images/{random.choice(images)}'
    
    def update_site(self, slug, title, category, category_slug, content=None):
        """
        Update blog page, index page, and related posts sections after creating a post.
        """
        # Add new post to blog.html
        self._update_blog_page(slug, title, category, category_slug)
        # Add new post to index.html
        self._update_index_page(slug, title, category, category_slug, content)
        # Update related posts in other posts
        self._update_related_posts(slug, title, category)

    def _update_index_page(self, slug, title, category, category_slug, content=None):
        index_path = self.base_dir / "index.html"
        if not index_path.exists():
            print("Warning: index.html not found.")
            return False

        with open(index_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        articles_grid = soup.find("div", class_="articles-grid")
        if not articles_grid:
            print("Warning: Could not find articles-grid in index.html")
            return False

        # Remove duplicate cards with the same title
        article_cards = articles_grid.find_all("article", class_="article-card")
        for card in article_cards:
            h3 = card.find("h3", class_="article-title")
            if h3 and h3.a and h3.a.string and h3.a.string.strip().lower() == title.strip().lower():
                card.decompose()

        # Create new article card (existing logic)
        article = self._create_article_card(soup, slug, title, category, category_slug)
        articles_grid.insert(0, article)

        # Limit number of cards (e.g., 6)
        max_cards = 6
        article_cards = articles_grid.find_all("article", class_="article-card")
        for card in article_cards[max_cards:]:
            card.decompose()

        with open(index_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Updated index.html successfully")
        return True

    def _update_blog_page(self, slug, title, category, category_slug):
        blog_path = self.base_dir / "blog.html"
        if not blog_path.exists():
            print("Warning: blog.html not found.")
            return False

        with open(blog_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        posts_grid = soup.find("div", class_="posts-grid")
        if not posts_grid:
            print("Warning: Could not find posts-grid in blog.html")
            return False

        # Remove duplicate cards with the same title
        article_cards = posts_grid.find_all("article", class_="article-card")
        for card in article_cards:
            h3 = card.find("h3", class_="article-title")
            if h3 and h3.a and h3.a.string and h3.a.string.strip().lower() == title.strip().lower():
                card.decompose()

        # Create new article card (existing logic)
        article = self._create_article_card(soup, slug, title, category, category_slug)
        posts_grid.insert(0, article)

        # Limit number of cards (e.g., 9)
        max_cards = 9
        article_cards = posts_grid.find_all("article", class_="article-card")
        for card in article_cards[max_cards:]:
            card.decompose()

        with open(blog_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Updated blog.html with new post")
        return True

    def _update_related_posts(self, slug, title, category):
        # This updates the recent/featured posts sidebar in all blog posts
        N = 5
        blog_files = sorted(self.blog_dir.glob("*.html"), key=lambda x: x.stat().st_mtime, reverse=True)
        recent_posts = []
        for post_file in blog_files:
            if post_file.stem == slug:
                continue
            post_title = self._extract_title_from_post(post_file)
            if post_title:
                recent_posts.append((post_title, post_file.name))
            if len(recent_posts) >= N:
                break
        # For featured, just use the same as recent for now (or pick other logic)
        featured_posts = recent_posts[:N]
        for post_file in blog_files:
            self._update_sidebar_in_post(post_file, recent_posts, featured_posts)
        print(f"Updated sidebars in blog posts with recent and featured posts.")

    def _update_sidebar_in_post(self, post_file, recent_posts, featured_posts):
        # Helper to update sidebar in a single blog post file
        with open(post_file, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        # Update Recent Posts (sidebar)
        recent_section = None
        for section in soup.find_all("section"):
            h3 = section.find("h3")
            if h3 and h3.text.strip().lower() == "recent posts":
                recent_section = section
                break
        if recent_section:
            ul = recent_section.find("ul", class_="sidebar-posts-list")
            if ul:
                ul.clear()
                for title, fname in recent_posts:
                    li = soup.new_tag("li")
                    a = soup.new_tag("a", href=f'/blog/{fname}')
                    a.string = title
                    li.append(a)
                    ul.append(li)
        # Update Featured Posts (sidebar)
        featured_section = None
        for section in soup.find_all("section"):
            h3 = section.find("h3")
            if h3 and h3.text.strip().lower() == "featured posts":
                featured_section = section
                break
        if featured_section:
            ul = featured_section.find("ul", class_="sidebar-posts-list")
            if ul:
                ul.clear()
                for title, fname in featured_posts:
                    li = soup.new_tag("li")
                    a = soup.new_tag("a", href=f'/blog/{fname}')
                    a.string = title
                    li.append(a)
                    ul.append(li)
        with open(post_file, "w", encoding="utf-8") as f:
            f.write(str(soup))

    def _extract_title_from_post(self, post_file):
        # Helper to extract title from a blog post file
        try:
            with open(post_file, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
            h1 = soup.find("h1")
            if h1:
                return h1.text.strip()
            h2 = soup.find("h2")
            if h2:
                return h2.text.strip()
        except Exception:
            return None
        return None

    def _extract_category_from_post(self, post_file):
        # Helper to extract category from a blog post file
        try:
            with open(post_file, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
            cat_span = soup.find("span", class_="article-category")
            if cat_span:
                return cat_span.text.strip()
        except Exception:
            return None
        return None

    def _create_article_card(self, soup, slug, title, category, category_slug):
        # Helper to create a new article card for blog/index pages
        article = soup.new_tag("article", **{"class": "article-card", "data-category": category_slug})
        image_div = soup.new_tag("div", **{"class": "article-image"})
        img = soup.new_tag("img", src="../images/hero-bg.jpg", alt=title)
        image_div.append(img)
        cat_span = soup.new_tag("span", **{"class": "article-category"})
        cat_span.string = category
        image_div.append(cat_span)
        article.append(image_div)
        content_div = soup.new_tag("div", **{"class": "article-content"})
        meta_div = soup.new_tag("div", **{"class": "article-meta"})
        date_span = soup.new_tag("span")
        date_icon = soup.new_tag("i", **{"class": "far fa-calendar"})
        date_span.append(date_icon)
        date_span.append(f" {self._get_today_date()}")
        meta_div.append(date_span)
        read_span = soup.new_tag("span")
        read_icon = soup.new_tag("i", **{"class": "far fa-clock"})
        read_span.append(read_icon)
        read_span.append(" 5 min read")
        meta_div.append(read_span)
        content_div.append(meta_div)
        h3 = soup.new_tag("h3", **{"class": "article-title"})
        a = soup.new_tag("a", href=f'/blog/{slug}.html')
        a.string = title
        h3.append(a)
        content_div.append(h3)
        excerpt = soup.new_tag("p", **{"class": "article-excerpt"})
        excerpt.string = f"Explore the latest in {category} with this insightful post."
        content_div.append(excerpt)
        read_more = soup.new_tag("a", **{"class": "read-more", "href": f'/blog/{slug}.html'})
        read_more.string = "Read More "
        icon = soup.new_tag("i", **{"class": "fas fa-arrow-right"})
        read_more.append(icon)
        content_div.append(read_more)
        article.append(content_div)
        return article

    def _get_today_date(self):
        from datetime import datetime
        return datetime.now().strftime('%B %d, %Y')

    def update_all_sidebars(self):
        """
        Ensures ALL blog posts in the blog folder have updated sidebars for recent and featured posts.
        """
        N = 5
        blog_files = sorted(self.blog_dir.glob("*.html"), key=lambda x: x.stat().st_mtime, reverse=True)
        # Collect latest N recent posts (title, filename)
        recent_posts = []
        for post_file in blog_files:
            post_title = self._extract_title_from_post(post_file)
            if post_title:
                recent_posts.append((post_title, post_file.name))
            if len(recent_posts) >= N:
                break
        featured_posts = recent_posts[:N]
        # For each post, update sidebar, excluding itself from recent
        for post_file in blog_files:
            this_title = self._extract_title_from_post(post_file)
            # Exclude itself from recent, but keep featured as global
            filtered_recent = [(title, fname) for title, fname in recent_posts if fname != post_file.name][:N]
            self._update_sidebar_in_post(post_file, filtered_recent, featured_posts)
        print("All blog post sidebars updated with latest recent and featured posts.")

    def _get_navbar_html(self):
        """
        Returns the EXACT HTML for the navbar as used in index.html/about.html, including the burger menu, for pixel-perfect replication.
        """
        return '''<header>
    <div class="container">
        <div class="logo">
            <a href="../index.html">Rohan Unbeg</a>
        </div>
        <nav>
            <ul class="nav-links">
                <li><a href="../index.html">Home</a></li>
                <li><a href="../blog.html">Blog</a></li>
                <li><a href="../about.html">About</a></li>
                <li><a href="../contact.html">Contact</a></li>
            </ul>
            <div class="burger">
                <div class="line1"></div>
                <div class="line2"></div>
                <div class="line3"></div>
            </div>
        </nav>
    </div>
</header>'''

    def _ensure_mainjs_script(self, soup):
        """
        Ensures that <script src="../js/main.js"></script> is present before </body>.
        """
        script_tag = soup.new_tag("script", src="../js/main.js")
        # Check if script is already present
        for tag in soup.find_all("script"):
            if tag.get("src") == "../js/main.js":
                return  # Already present
        if soup.body:
            soup.body.append(script_tag)

    def _get_favicon_links(self):
        """
        Returns favicon link tags for use in <head> (not for blog posts in /blog/).
        """
        return '''<link rel="icon" type="image/png" sizes="32x32" href="../favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="../favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="../apple-touch-icon.png">
<link rel="manifest" href="../site.webmanifest">'''

    def update_site_references(self):
        """
        Updates references to blog posts in index.html and blog.html, ensuring only existing posts are shown.
        Removes references to deleted/non-existent posts from the blog folder.
        Also updates sidebars in all blog posts.
        """
        from bs4 import BeautifulSoup
        import re
        # Get all current blog post filenames (just the filename, no path)
        blog_files = set(f.name for f in self.blog_dir.glob("*.html"))
        # --- Update blog.html ---
        blog_html_path = self.base_dir / "blog.html"
        if blog_html_path.exists():
            with open(blog_html_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
            posts_grid = soup.find("div", class_="posts-grid")
            if posts_grid:
                cards = posts_grid.find_all("article", class_="article-card")
                for card in cards:
                    a_tag = card.find("a", href=True)
                    if a_tag:
                        href = a_tag.get("href")
                        # Extract filename from href (handles /blog/, blog/, and relative)
                        match = re.search(r"(?:/|^)blog/([^/?#]+\.html)", href)
                        if match:
                            post_file = match.group(1)
                        else:
                            # Try to match any .html file in href
                            match2 = re.search(r"([^/?#]+\.html)", href)
                            post_file = match2.group(1) if match2 else None
                        if not post_file or post_file not in blog_files:
                            card.decompose()  # Remove card for deleted post
                # Limit number of cards (e.g., 9)
                article_cards = posts_grid.find_all("article", class_="article-card")
                max_cards = 9
                for card in article_cards[max_cards:]:
                    card.decompose()
            with open(blog_html_path, "w", encoding="utf-8") as f:
                f.write(str(soup))
            print("blog.html updated to remove references to deleted posts.")
        else:
            print("Warning: blog.html not found.")

        # --- Update index.html ---
        index_html_path = self.base_dir / "index.html"
        if index_html_path.exists():
            with open(index_html_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
            articles_grid = soup.find("div", class_="articles-grid")
            if articles_grid:
                cards = articles_grid.find_all("article", class_="article-card")
                for card in cards:
                    a_tag = card.find("a", href=True)
                    if a_tag:
                        href = a_tag.get("href")
                        match = re.search(r"(?:/|^)blog/([^/?#]+\.html)", href)
                        if match:
                            post_file = match.group(1)
                        else:
                            match2 = re.search(r"([^/?#]+\.html)", href)
                            post_file = match2.group(1) if match2 else None
                        if not post_file or post_file not in blog_files:
                            card.decompose()  # Remove card for deleted post
                # Limit number of cards (e.g., 6)
                article_cards = articles_grid.find_all("article", class_="article-card")
                max_cards = 6
                for card in article_cards[max_cards:]:
                    card.decompose()
            with open(index_html_path, "w", encoding="utf-8") as f:
                f.write(str(soup))
            print("index.html updated to remove references to deleted posts.")
        else:
            print("Warning: index.html not found.")

        # --- Update all sidebars in blog posts ---
        self.update_all_sidebars()
        print("Site references updated. Only existing blog posts are now shown. Sidebars refreshed.")

def main():
    parser = argparse.ArgumentParser(description="Blog Automation Tool for Rohan Unbeg's Blog")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    create_parser = subparsers.add_parser("create", help="Create a new blog post")
    create_parser.add_argument("title", help="Title of the blog post")
    create_parser.add_argument("category", help="Category of the blog post")
    create_parser.add_argument("--content", "-c", help="File containing the post content")
    create_parser.add_argument("--image", "-i", help="Path to feature image for the post")
    
    list_parser = subparsers.add_parser("list", help="List all blog posts")
    
    delete_parser = subparsers.add_parser("delete", help="Delete a blog post")
    delete_parser.add_argument("slug", help="Slug of the post to delete")
    
    update_refs_parser = subparsers.add_parser("update_refs", help="Update site references to remove invalid posts")
    
    args = parser.parse_args()
    automator = BlogAutomator()
    
    if args.command == "create":
        content = args.content if args.content else None
        automator.create_post(args.title, args.category, content, args.image)
    elif args.command == "list":
        automator.list_posts()
    elif args.command == "delete":
        automator.delete_post(args.slug)
    elif args.command == "update_refs":
        automator.update_site_references()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
