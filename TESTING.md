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
*HTML validation result for all pages*

I did not get any warnings or errors, the full validation results can be found here:

- [Index page (logged out)](docs/testing/validation_index.pdf)
- [Registration](docs/testing/validation_register.pdf)
- [Login](docs/testing/validation_login.pdf)
- [Logout](docs/testing/validation_logout.pdf)
- [Dashboard](docs/testing/validation_dashboard.pdf)
- [Choose a category](docs/testing/validation_category.pdf)
- [Choose a subcategory (with breadcrumbs)](docs/testing/validation_subcategory.pdf)
- [Add a category](docs/testing/validation_add_category.pdf)
- [Edit a category](docs/testing/validation_edit_category.pdf)
- [Delete a category](docs/testing/validation_category_confirm_delete.pdf)
- [Stock items table](docs/testing/validation_items.pdf)
- [Stock items search results](docs/testing/validation_items_search.pdf)
- [Add a stock item](docs/testing/validation_add_item.pdf)
- [Edit a stock item](docs/testing/validation_edit_item.pdf)
- [Delete a stock item](docs/testing/validation_item_confirm_delete.pdf)
- [Stock item detail](docs/testing/validation_item_detail.pdf)
- [CSV file upload](docs/testing/validation_upload.pdf)
- [Basket](docs/testing/validation_basket.pdf)
- [Delivery notes](docs/testing/validation_delivery_notes.pdf)
- [Add a delivery note](docs/testing/validation_add_note.pdf)
- [Edit a delivery note](docs/testing/validation_edit_note.pdf)
- [Delete a delivery note](docs/testing/validation_note_confirm_delete.pdf)
- [Delivery note detail](docs/testing/validation_note_detail.pdf)
- [Add a customer](docs/testing/validation_add_customer.pdf)

### **CSS Validation**

I used the [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) to validate my custom CSS code, the CSS created by Tailwind was not tested. My custom CSS code was validated without errors.

![CSS validation](docs/testing/css_validation.png)
*CSS validation result for custom CSS*

### **JavaScript Validation**

[JSHint](https://jshint.com/) was used to test my JavaScript code. Warnings that occur because of the use of ES6 variables can be resolved by adding `/* jshint esversion: 6 */` as a comment in the first line of JSHint. `/*globals $:false */` can be added to avoid warnings because of the use of *jQuery*.

My project has a **base.js** file containing JavaScript code that is needed on every page. JavaScript code that is only needed for certain pages, was included at the necessary templates directly. No errors or warnings were found for my JavaScript code.

![JS validation base.js](docs/testing/validation_base_js.png)
*JS validation result for base.js*

![JS validation templates](docs/testing/validation_template_js.png)
*JS validation result for template files*

### **Python Validation**
