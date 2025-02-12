# 🛠️ Broken Image Checker

## 📌 Overview  
The [**Broken Image Checker**](https://github.com/phpsmashcode/Broken-Image-Checker) is a Python script that crawls a given website, checks all images on its pages, and identifies broken image links. The results are saved in a CSV report.

[**Visit Repository**](https://github.com/phpsmashcode/Broken-Image-Checker)

---

## 🚀 Features  
- ✅ Crawls a website starting from a given URL.  
- ✅ Checks all images for broken links (404 errors, timeouts, etc.).  
- ✅ Saves a detailed report of broken images, including:  
  - **Page URL** where the image was found.  
  - **Image URL**.  
  - **HTTP status**.  
  - **Image's alt text** (if available).  
  - **Image location** in the page.  
- ✅ Multi-threaded for fast processing.  
- ✅ Option to **limit the number of pages** to crawl.  
- ✅ Creates a **report in an `image_reports/` directory**.  

---

## 📋 Prerequisites  

Ensure you have Python installed (**Python 3.6+ recommended**). Install required dependencies using:  

```sh
pip install requests beautifulsoup4
```

## 💻 Usage

Clone the repository:
```
git clone https://github.com/phpsmashcode/Broken-Image-Checker.git
```

Run the script with:

```sh
python broken-image-checker.py
```

## 📌 You Will Be Prompted To:  

- 🔹 **Enter the website URL** to check (including `http://` or `https://`).  
- 🔹 (**Optional**) **Enter the maximum number of pages** to crawl (leave blank for unlimited).  

---

## 📜 License  

This project is licensed under the **MIT License**.

---

## 🤝 Contributing  

🚀 Feel free to contribute! **Fork the repository, make your changes, and submit a pull request.**

---

## 👤 Author  

Developed by **Hariprasad Vijayan**.

---

## 📬 Contact  

For issues or suggestions, **open an issue on GitHub**. 📩
