import os

SITE_URL = "https://rohanunbeg.com"
BLOG_DIR = "blog"
SITEMAP_FILE = "sitemap.xml"

# Main site pages
main_pages = [
    "index.html",
    "blog.html",
    "about.html",
    "contact.html",
    "robots.txt"
]

def get_blog_post_urls():
    urls = []
    for fname in os.listdir(BLOG_DIR):
        if fname.endswith(".html"):
            urls.append(f"{SITE_URL}/{BLOG_DIR}/{fname}")
    return urls

def generate_sitemap():
    urls = [f"{SITE_URL}/{page}" for page in main_pages]
    urls += get_blog_post_urls()
    sitemap = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for url in urls:
        sitemap.append("  <url>")
        sitemap.append(f"    <loc>{url}</loc>")
        sitemap.append("  </url>")
    sitemap.append("</urlset>")
    return "\n".join(sitemap)

if __name__ == "__main__":
    sitemap_str = generate_sitemap()
    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write(sitemap_str)
    print(f"Sitemap updated with {len(main_pages)} main pages and {len(get_blog_post_urls())} blog posts.")
