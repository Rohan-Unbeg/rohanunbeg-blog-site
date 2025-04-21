# Rohan Unbeg Blog Site

A modern, responsive static blog site focused on AI and developer tools. This site is built with HTML, CSS, and JavaScript.

## Features

-   Clean and modern design
-   Fully responsive layout for all screen sizes
-   Category filtering for blog posts
-   Newsletter subscription form
-   Contact form
-   Social media integration
-   Optimized for fast loading

## Project Structure

```
rohanunbeg-blog-site/
├── css/
│   └── styles.css
├── js/
│   └── main.js
├── images/
│   ├── hero-bg.jpg (not included - placeholder)
│   ├── post1.jpg (not included - placeholder)
│   ├── post2.jpg (not included - placeholder)
│   └── ...
├── blog/
│   └── (individual blog posts will go here)
├── index.html
├── blog.html
├── about.html
├── contact.html
└── README.md
```

## Setup Instructions

1. Clone this repository or download the files.
2. Add your own images to the `images/` directory.
3. Customize the content in the HTML files to match your personal information.
4. Test the site locally by opening `index.html` in your browser.

## Deployment on Cloudflare Pages

1. Push your code to a GitHub repository.
2. Sign in to Cloudflare Dashboard.
3. Go to Pages > Create a project > Connect to Git.
4. Select your repository and configure the build settings:
    - Build command: (leave empty for static sites)
    - Build output directory: / (root)
    - Root directory: / (root)
5. Deploy your site.
6. Configure your custom domain (rohanunbeg.com) in the Cloudflare Pages settings.

## Customization

-   **Colors**: Edit the CSS variables in `css/styles.css` to change the color scheme.
-   **Fonts**: The site uses 'Inter' from Google Fonts. You can change this in the HTML files and CSS.
-   **Content**: Update the text and images in the HTML files to personalize the site.
-   **Logo**: The site currently uses text for the logo. You can replace it with an image by modifying the logo section in the HTML files.

## Adding Blog Posts

To add a new blog post:

1. Create a new HTML file in the `blog/` directory.
2. Use the existing structure from the blog post examples.
3. Update the blog listings in `blog.html` and on the homepage to include your new post.

## Browser Compatibility

This site is compatible with modern browsers including:

-   Chrome
-   Firefox
-   Safari
-   Edge

## License

This project is open source and available for personal and commercial use.

## Credits

-   Fonts: [Google Fonts - Inter](https://fonts.google.com/specimen/Inter)
-   Icons: [Font Awesome](https://fontawesome.com/)

# Blog Automation Tool

A Python script to automate the creation and management of blog posts for the Rohan Unbeg Blog site.

## Features

-   Create new blog posts with proper HTML structure
-   Automatically update the blog index page
-   List all existing blog posts
-   Delete blog posts

## Installation

1. Ensure you have Python 3.6+ installed
2. Install the required dependencies:

```bash
pip install beautifulsoup4
```

## Usage

### Creating a new blog post

```bash
python blog_automation.py create "My Blog Post Title" "Category Name"
```

Add content from a file:

```bash
python blog_automation.py create "My Blog Post Title" "Category Name" --content my_content.txt
```

## Blog Post Creation

### Using the Blog Automation Tool

The blog automation tool supports creating posts from markdown files. You can create new posts using:

```bash
python blog_automation.py create "Your Post Title" "Category Name" --content your-post.md
```

### Supported Markdown Syntax

The blog automation tool supports extensive markdown formatting:

#### Headers

```markdown
# Main Title (h1)

## Section Title (h2)

### Subsection (h3)

#### Smaller Section (h4)

##### Even Smaller (h5)

###### Smallest (h6)
```

#### Text Formatting

```markdown
**Bold Text** or **Bold Text**
_Italic Text_ or _Italic Text_
```

#### Lists

Unordered lists (any of these markers: -, \*, +):

```markdown
-   Item 1
-   Item 2
    -   Subitem 2.1
    -   Subitem 2.2
```

Ordered lists:

```markdown
1. First item
2. Second item
3. Third item
```

#### Links

```markdown
[Link Text](https://example.com)
```

#### Code Blocks

With syntax highlighting:

````markdown
```python
def hello_world():
    print("Hello, World!")
```
````

#### Blockquotes

```markdown
> This is a blockquote
> It can span multiple lines
```

### Example Blog Post

Here's a complete example of a blog post:

````markdown
# The Future of AI Development

An exploration of upcoming AI trends and their impact on software development.

## Introduction

This post discusses the evolving landscape of AI in software development.

### Key Points

-   AI is transforming how we write code
-   Tools are becoming more sophisticated
-   Developer productivity is increasing

## Technical Details

1. Large Language Models
2. Code Generation
3. Automated Testing

> Important: AI tools should augment, not replace, human developers.

## Code Example

```python
def ai_enhanced_function():
    print("AI is helping write this code")
```
````

## Conclusion

_AI tools_ are becoming **essential** for modern development.

````

### CSS Classes and Styling

The generated blog posts will automatically use these CSS classes:

- `.post-header`: Post title and metadata section
- `.post-category`: Category label
- `.post-content`: Main content area
- `.post-meta`: Post metadata (date, read time)

### Images

To add a featured image to your post:

```bash
python blog_automation.py create "Post Title" "Category" --content post.md --image featured.jpg
````

Images should be:

-   JPG format
-   16:9 aspect ratio recommended
-   At least 1200px wide for optimal quality

## File Organization

-   Blog posts are stored in the `blog/` directory
-   Images are stored in the `images/` directory
-   Post filenames are automatically generated from the title

## How It Works

-   The script uses the existing post1.html as a template for new posts
-   It automatically updates blog.html with new post entries
-   All posts are numbered sequentially (post1.html, post2.html, etc.)
-   Images are expected to be in the images directory with names matching post numbers

## Requirements

-   Python 3.6+
-   BeautifulSoup4

## Examples

### Creating a post with content from a file

1. Create a text file (e.g., `new-post.txt`) with your content:

```
This is the first paragraph of my blog post.

This is the second paragraph with more detailed information.

This is the third paragraph with a conclusion.
```

2. Run the command:

```bash
python blog_automation.py create "New AI Tools for 2024" "AI Tools" --content new-post.txt
```

## Notes

-   Make sure to run the script from the root directory of your blog
-   The script will automatically create the blog and images directories if they don't exist
-   You can customize the script to add more features as needed
