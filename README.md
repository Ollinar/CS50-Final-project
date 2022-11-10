# **QUIZER**
#### Video Demo: - [ ]Url here
#### Description: This Is the final project for CS50 that I've decided to make. It's a a simple web application about making, sharing, and taking quizes. 

#### **Implemented Pages:**
* A page to register
* A page to login
* A logout button in nav bar
* Index page when a user first visits the site
* Index page when a user is logged in
* A page with list of quizes
* A page to make a quiz
* A page to take a quiz
* A page to show the score the user got

#### **To be Implemented Pages:**
* A page that shows the ranking of people that took a quiz - I still can't decide how this should be implemented. It could either be public that everyone can see it, or private that only the quiz creator can see it.
* A page to change password - new idea
* A page to manage quizes made by user - new idea
* An about page - new idea


## **List of features in each pages**

### **All pages**
##### **Implemented features**
* A nav bar with off canvas menu thaat contain either Login and Register wheen the user is not logged in, or logout when the user is logged in. It also contain social media links for creators. It only redirects to Facebook.com and twitter.com for now though.
##### **To be implemented feature**
* A button or link in off canvas menu that redirect to a change password if or when that page is implemented.
* A button for enabling dark theme
* A button to redirect to about if or when that is implemented
* A footer
### **Welcome page**
##### **Implemeted feature**
* A button that redirects the user to register page
* A button that redirects the user to login page
##### **To be implemented feature**
* A proper welcoming text - Can't think of one, I'm not creative enough :sweat_smile:
### **Register page**
##### **Implemented feature**
* Username, Password, Confirm password field and a submit button
* Username is verified, makes sure its not invalid or taken
* password is verified, makes sure its valid (Minimum of 8 characters long, Atleast 1 Capital letter, Small letter, Number)
* Flash the user if something is invalid
##### **To be implemented feature**
* A better form verification/flashing. When there is an error, it wouldn't reload the whole page  thus keeping the things that the user have already inputted. - I dont know how to do this, I'm guessing with JavaScript. Im not good at it though :upside_down_face:
### **Login Page**
##### **Implemented features**
* A Username and Password field and a submit button
* Username and Password is verified making sure its valid and matches
##### **To be implemented features**
* A show password button

### **User Homepage**
##### **Implemented features**
* Buttons to redirect to Make quiz and the list of quizes
##### **To be implemented features**
* A history of quiz taken and its score
* A list of Quiz that the user made
### **Make Quiz page**
##### **Implemented features**
* Add question
* Remove question
* Add answer on each question with maximum of 4
* Remove answer on each question 
* Correct answer field for the right answer out of all answers in each question

##### **To be implemented features**
* A better implementation of these features that makes it so it doesnt clear the already filled out field when page is modified

### **Quiz list**
##### **Implemented features**
* List of all the quiz in the database
* Take quiz button on every quiz listed
##### **To be implemented features**
* Sort feature
* Search feature
### **Take Quiz**
##### **Implemented features**
* Each qustion is displayed
* Answers for each question is displayed as radion button
* When submitted, app checks each user's answer on each question if it matches the correct answer set by the quiz maker.
* Keeps track of the number of correct answer and redirect to score page
##### **To be implemented features**
* A more slick looking layout of take quiz page
### **Score**
##### **Implemented features**
* Shows the score the user got from the quiz taken
##### **To be implemented features**
* A more creative way to display score
* Table to show user's answer and the correct answer