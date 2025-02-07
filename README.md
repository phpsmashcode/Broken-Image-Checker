# Broken-Image-Checker

Overview

The Broken Image Checker is a Python script that crawls a given website, checks all images on its pages, and identifies broken image links. The results are saved in a CSV report.

Features

Crawls a website starting from a given URL.

Checks all images for broken links (404 errors, timeouts, etc.).

Saves a detailed report of broken images, including:

Page URL where the image was found.

Image URL.

HTTP status.

Image's alt text (if available).

Image location in the page.

Multi-threaded for fast processing.

Option to limit the number of pages to crawl.

Creates a report in a image_reports directory.

Prerequisites

Ensure you have Python installed (Python 3.6+ recommended). Install required dependencies using:

pip install requests beautifulsoup4

Usage

Run the script with:

python website_image_checker.py

You will be prompted to:

Enter the website URL to check (including http:// or https://).

(Optional) Enter the maximum number of pages to crawl (leave blank for unlimited).

Example Output

Website Broken Image Checker
============================

Enter website URL to check (include http:// or https://): https://example.com
Enter maximum number of pages to check (press Enter for unlimited): 10

Starting check...

Checking page 1: https://example.com
Pages checked: 1
Images checked: 15
Broken images found: 2
...
Crawl completed in 45.32 seconds
Total pages checked: 10
Total images checked: 120
Total broken images: 5

Saving report to: image_reports/broken_images_example.com_20250207_123456.csv
Report saved successfully!

Output Report

A CSV report is generated in image_reports/, containing the following columns:

Page URL: The webpage where the broken image was found.

Image URL: The URL of the broken image.

Status: HTTP status or error message.

Alt Text: The image's alternative text.

Location: Approximate HTML location of the image.

If no broken images are found, the report will indicate this.

License

This project is licensed under the MIT License.

Contributing

Feel free to contribute! Fork the repository, make your changes, and submit a pull request.

Author

Developed by Hariprasad Vijayan.

Contact

For issues or suggestions, open an issue on GitHub
