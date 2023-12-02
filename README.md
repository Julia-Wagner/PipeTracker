# **PipeTracker**

PipeTracker is an inventory management application specifically designed for plumbers. The project was born out of the real-world challenges of a self-employed plumber. Built with a user-centered approach, PipeTracker manages inventory for plumbing businesses and simplifies the invoicing process for plumbers.

# **Planning**

I tried to structure my planning phase using the 5 UX planes - strategy, scope, structure, skeleton and surface. The planning process was iterative and while getting a better idea of the project´s scope and speaking to my customer about his needs for the application these planes changed creating a user-centered design for PipeTracker.

## **Strategy Plane**

My initial idea for this project was to create an application for my husband´s plumbing business. He is self-employed and I created his Logo, Designs and Website. So I wanted to make a real-world application where I could put this to use.

After talking to him about possible applications he might need that would be suitable for this project, the idea of an inventory tool - **PipeTracker** - quickly came to life. In the following parts of the readme I will refer to my husband as my customer, as the application is built with his real-world needs in mind.

### **Target Audience**

As this project is intended to be a specific real-world application for my husband, he and possible employees are my target audience or customers. But in general, a tool like this could be used for all plumbing companies so a few characteristics for my target audience would be the following.

- A plumbing company that wants to keep track of its inventory with an online application.
- Anybody who wants to manage stock items and have an overview of the current value they have in stock.
- A plumber who wants to easily create a delivery note from the stock items used for a customer. 

### **Site Goals**

- Create an easy-to-use inventory tool.
- Adapt the application specifically for plumbing businesses.
- Simplify the invoicing process for plumbers.
- Give an overview of items in stock.
- Implement CRUD functionalities for stock items, delivery notes and categories.
- Make the application responsive, so it can be used on desktop, tablet and mobile screen-sizes.
- Allow easy adaption to create a scalable application that could be used for other (plumbing) businesses too.

## **Scope Plane**

To get a better understanding of what the application will look like I wrote down the features and sorted them into necessary and nice-to-have features.

**Necessary Features:**

- Plumber can log in to the application.
- Plumber can register to the application.
- Stock items can be added, updated and deleted.
- Stock items are linked to categories.
- Plumber has an overview of the current value (in €) that is in the inventory.

**Nice-to-have Features:**

- Create a delivery note - remove items from stock by adding them to a delivery note for a customer.
- Employees can log in but have another role with different permissions (for example they don´t see the price).
- Images can be uploaded for categories.
- Plumber can make a list of items to order that can be exported as a CSV/PDF file.
- Items can be added by scanning a QR code.
- Datanorm (file format for stock items used by plumbing wholesalers) can be imported and automatically update the price for stock items.

## **Structure Plane**

From the features defined above I was able to create epics and break these down into user stories.

### **Epic: User Authentication**

| User Story                                                                                                           | Priority       |
|----------------------------------------------------------------------------------------------------------------------|----------------|
| As a **new user**, I want to **register to the application**, so that I can **manage my inventory**.                 | **MUST HAVE**  |
| As an **existing user**, I want to **login to the application**, so that I can **access my inventory**.              | **MUST HAVE**  |
| As a **site owner**, I want to **manage user roles**, so that I can **choose who can access sensitive information**. | **COULD HAVE** |

### **Epic: Stock Items**
| User Story                                                                                                            | Priority        |
|-----------------------------------------------------------------------------------------------------------------------|-----------------|
| As a **site user**, I want to **create and view categories**, so that I can **organize my inventory**.                | **MUST HAVE**   |
| As a **site user**, I want to **upload images for categories**, so that I can **identify items easier**.              | **SHOULD HAVE** |
| As a **site user**, I want to **create and view stock items**, so that I can **organize my inventory**.               | **MUST HAVE**   |
| As a **site user**, I want to **update stock items**, so that I can **correctly maintain my inventory**.              | **MUST HAVE**   |
| As a **site user**, I want to **delete stock items**, so that I can **remove items from my inventory**.               | **MUST HAVE**   |
| As a **site user**, I want to **have an overview of my stock items**, so that I can **quickly find the item I need**. | **MUST HAVE**   |

### **Epic: Statistics**
| User Story                                                                                                            | Priority        |
|-----------------------------------------------------------------------------------------------------------------------|-----------------|
| As a **site user**, I want to **have a dashboard with statistics**, so that I can **make decisions for my business**. | **SHOULD HAVE** |

### **Epic: Delivery Notes**
### **Epic: Cart**
### **Epic: Export/Import**

## **Skeleton Plane**

### **Wireframes**

I created wireframes for desktop, tablet and mobile for each of the main parts of the application.

<details>
    <summary><strong>Landing Page</strong></summary>  
    <img src="docs/wireframes/landing_page.png">
</details>

<details>
    <summary><strong>Dashboard</strong></summary>  
    <img src="docs/wireframes/dashboard.png">
</details>

<details>
    <summary><strong>Categories</strong></summary>  
    <img src="docs/wireframes/categories.png">
</details>

<details open>
    <summary><strong>Stock Items</strong></summary>  
    <img src="docs/wireframes/stock_items.png">
</details>

<details>
    <summary><strong>Cart</strong></summary>  
    <img src="docs/wireframes/cart.png">
</details>

<details>
    <summary><strong>Delivery notes</strong></summary>  
    <img src="docs/wireframes/delivery_notes.png">
</details>

<details>
    <summary><strong>Add delivery note</strong></summary>  
    <img src="docs/wireframes/add_delivery_note.png">
</details>

<details>
    <summary><strong>Detail delivery note</strong></summary>  
    <img src="docs/wireframes/detail_delivery_note.png">
</details>

### **Database Schema**

After discussing the needed features for the application, I started creating my database schema. With every iteration of talking to my customer about the needed features and stored information, the schema grew. The final adaptions were made while creating the wireframes for the application.

As it might be necessary for my customer to create subcategories for categories, I decided to follow the approach of [this article about categories and subcategories](https://dcblog.dev/mysql-categories-and-subcategories). I added a *parent_id* field with a default of *0* to **Category**. If the *parent_id* of a category matches the id of another category instead of *0*, it is a subcategory. 

![Database Schema](docs/screenshots/database_schema.png)
*Database Schema for PipeTracker*

## **Surface Plane**

### **Design**

As mentioned above, I already created a [website](https://p-wagner.at/), as well as all the designs and logos for my customer´s company before starting this project. I will use the existing design for this project. As a reference, here is what the company´s business card I designed looks like.

![Business card](docs/screenshots/business_card.jpg)
*Existing design created by myself*

I used shades of blue and the background representing water as it is fitting for a plumbing company. The logo is my customer´s name with the services he offers.

From this existing design, I created the color scheme for this project. I used [contrast-grid.eightshapes.com](https://contrast-grid.eightshapes.com/?version=1.1.0&background-colors=&foreground-colors=%23274060%0D%0A%2300B2CA%0D%0A%23041020%0D%0A%23f9f9f9&es-color-form__tile-size=regular&es-color-form__show-contrast=aaa&es-color-form__show-contrast=aa&es-color-form__show-contrast=aa18&es-color-form__show-contrast=dnp) to check the contrast and possible color combinations.

![Color contrast](docs/screenshots/color_contrast.png)
*Accessibility/contrast check for color scheme*

I will use the same fonts for this project as I used on the website. **Roboto** and **Montserrat** are both Google Fonts and fit well with the logo and design of the company.
