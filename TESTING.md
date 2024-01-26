# **Testing**

## **Table of Contents**

<!-- TOC -->
* [**Testing**](#testing)
  * [**Table of Contents**](#table-of-contents)
  * [**Manual Testing**](#manual-testing)
  * [**Validation**](#validation)
    * [**HTML Validation**](#html-validation)
    * [**CSS Validation**](#css-validation)
    * [**JavaScript Validation**](#javascript-validation)
    * [**Python Validation**](#python-validation)
<!-- TOC -->

## **Manual Testing**

I started this project by setting everything up and deploying it right away. While developing new features, I tested them on the local version. After finishing and pushing features or parts of them, I tested them on the deployed project.

I always tested new input by entering incorrect information and trying to break it. This way I ensured correct error handling and feedback to the user.

I regularly tested the application in different browsers and devices, like my phone and tablet. When I found a bug while testing on my phone, I created a **Bug Issue** on my Kanban board and provided details and screenshots.

The *#peer-code-review* channel on Code Institute´s Slack was used to get some feedback from other students. I also sent the link to my project to friends and family asking them to test it.

I tested to a minimum screen width of **300px** and a maximum screen width of **3440px** with my monitor. To test **Safari** and **iOS devices** I used [BrowserStack](https://www.browserstack.com/).

## **Validation**

### **HTML Validation**

I used the [HTML W3C Validator](https://validator.w3.org/) to validate all of my HTML files. I validated each page of the application by right-clicking on the deployed page, selecting *View page source* and pasting the code to the validator.

![HTML validation](docs/testing/html_validation.png)

I did not get any warnings or errors, the full validation results can be found here:

- [Index page (logged out)](docs/testing/validation_index.pdf)
- [Registration](docs/testing/validation_register.pdf)
- [Login](docs/testing/validation_login.pdf)
- [Logout](docs/testing/validation_logout.pdf)
- [Dashboard](docs/testing/validation_dashboard.pdf)
- [Choose a Category](docs/testing/validation_category.pdf)
- [Choose a Subcategory (with breadcrumbs)](docs/testing/validation_subcategory.pdf)
- [Add a Category](docs/testing/validation_add_category.pdf)
- [Edit a Category](docs/testing/validation_edit_category.pdf)
- [Stock Items table](docs/testing/validation_items.pdf)
- [Stock Items search results](docs/testing/validation_items_search.pdf)
- [Add a Stock Item](docs/testing/validation_add_item.pdf)
- [Edit a Stock Item](docs/testing/validation_edit_item.pdf)
- [Stock Item Detail](docs/testing/validation_item_detail.pdf)
- [CSV File Upload](docs/testing/validation_upload.pdf)
- [Basket](docs/testing/validation_basket.pdf)

### **CSS Validation**

### **JavaScript Validation**

### **Python Validation**
