# QuizGameV3

So I may've started this in December, maybe January, but I've had to deal with Assignments, other Things I like working on, my oversized Garden, and sleeping. That is an incomplete list.<br/>
Anyway, now it's July, and I've gotten to making good progress.<br/>

<br/>(I've also decided that I can make this in a different, better way, that I'll do after I've finished this version so that I have a basis to work off for that)<br/>
Unfinished Sections of this README indicate features that are included within the Code already, or will be in the future<br/>

Sorry Aimee if you see this, but despite all the Modules you taught over the last 2 years, I didn't do any prior Design, or Wireframes, nor proper documented testing / using PyTest.

---

# WARNINGS
## File Issues
If it doesn't run properly, it might be because so far it has only been ran and tested in Visual Studio Code, with the Folder Open, not running from the main.py file, which will produce different starting files.<br/>
There is a provision to try and offset this issue, however I'm not sure if it works, as I haven't tested it yet.
## Required Python Packages
This Application uses the PyGame and Pillow Python Packages in order to play Audio Clips and handle Image Files, ensure you have these Packages Installed before attempting to run the program.

---

# Account Details
## Login
If you dont want to create an account, then use 'stephenaccount3' as the username, and 'coloursyay' as the password, in order to access the application.
## Create Account
You can create your own account, using the Create Account Page.<br/>
You provide a Username and a Password, and then choose the Colours you'd like for your profile.<br/>
You can select Window Colours, Button Colours, Label Colours, and Entry Colours. Each has Background and Foreground Options, which must have a minimum of a 4.5:1 Colour Contrast Ratio, to be legal.<br/>
Label, Button and Entry Colours also must have a minimum of a 7:1 Colour Contrast Ratio to the Window Colour, in order to be permitted.
## Password Encryption
Passwords are Encrypted using a Caesar Cypher applied individually to Consonants, Vowels, Symbols, and Digits.
These shifts all differ, and are randomly generated at Account Creation, and each time the User changes their Password thereafter.
As this is a (now not so) basic Quiz Game, password security wasn't a major consideration, however this is a nice attempt at some form.
## Guest Accounts
Guest Accounts are a Type of Account that cannot be accessed when the user logs out.
They use the default Colour Scheme of the Application (Colours on the Login Page), and can only complete Quizzes, being sent straight to the Quiz Setup Page.

---

# Home Page
At the top of the Home Page, the Users Username, and High Score is displayed, along with a range of Menu Options, which allow the user to:
- Setup + Play a Quiz
- Edit Questions
- Edit Topics, Colours, or Audios
- View their Account
- View a Leaderboard (Not Implemented Yet)
- Logout, Exit, or Center the Application

---

# Components
## Audios
Audio Clips are used after Each Question to add a bit of auditory feedback that you have answered the question.<br/>
Audios aren't categorised, so an Audio used for a Correct Answer on one Question, may be uesd for an Incorrect Answer on another Question, this will potentially be rectified in the future, to provide consistency, and to minimise confusion over whether an answer was Correct or not.
## Colours
Colours are used throughout the program, customisable on a per Account Basis for the Window Background, Buttons, Entries, and Labels.<br/>
There is a minimum Colour Contrast Ratio of 4.5:1, for Widget Background and Text Colours, and also Widgets compared to the Background, to ensure that there is a clear difference between the Background, and the Foreground, and that Text is readable.<br/>
Colours used on Closed Question Answers don't have a Minimum Contrast to the Background, due to the wide array of colours that can be used, however Answers can't use Red, Green, or Indigo as Colours, due to their Use in Answer Checking.
## Topics
Topics are used to allow the Users decide what they would like Questions about, such as Coding Questions, or Questions about the Space Shuttle.<br/>
Topics have a Background and Foreground Colour, and are displayed on the Right Hand Side during the Quiz.<br/>
A Question can have at most 7 Topics attatched to it.<br/>
When setting up their Quiz, the User can select as many topics as they like.

---

# Questions
## Closed Questions
Typical Multiple Choice Question, as featured in previous versions.<br/>
However, now a Question can have 2-4 Answer Options, instead of the Mandated 4 of Previous Versions.
## Open Questions
Open Questions are Questions that allow the Player to enter their own Answer, which will then be deemed Correct or Incorrect if it includes Required and/or Acceptable Words
## Order Questions
Order Questions allow the Player to order a series of Items in order to Answer the question, such as ordering Space Shuttle Orbiters by Missions Flown.
The Items, of which there are up to 12, are displayed to the user, where they can then order the Items, from 1 to (up to) 12.
The Player will only get the Available Points if they get all the Items ordered correctly.
## Image Questions
**HALF IMPLEMENTED**<br/>
It is possible to create and edit Image Questions, however they will be unusable in the Quiz, as the Toggle to include them is disabled.<br/>
May replace these with Audio Questions so I don't have to make design modifications to the page, or just not include either all together

---

# Hints
Each Question can have up to 2 Hints with it, a Text Hint, and an individualised Hint to the Question Type.
Each Hint costs 1/3rd of the Original Points Value of the Question, rounded to the nearest .1 of a point.
## Text Hints
Text Hints are available for inclusion on ***All*** Question Types.<br/>
These are short pieces of text that hint at the Answer to the Question
## Closed Question Hint: *50/50*
*50/50* Hints are available for inclusion on ***Closed*** Question Types, where the question has 4 Answer Options.<br/>
These hints remove 2 of the incorrect answers, leaving the player with the Correct Answer, and an Incorrect Answer.
## Open Question Hint: *Provide Word*
*Provide Word* Hints are available for inclusion on ***Open*** Question Types.<br/>
These hints provide the user with one of the required (or optional) words contained within the Answer.
## Order Question Hint: *Place One*
*Place One* Hints are available for inclusion on ***Order*** Question Types.<br/>
These hints provide the position of an answer, which the user is then unable to edit.

---

## Question Creation
This Feature allows the User to create their own Questions for the Quiz, from 1 of the 3 types available.
Users enter the Question Text, and select what Hints they'd like the Question to have, providing the relevant details.
Users also select the Question Topics, Difficulty, Points Available, and the 2 Audio Files (Which must be different).
Users also provide a Fun Fact for the Question, that is displayed after the user has provided their answer.

## Question Editing
This allows Users to Edit Questions, with the ability to alter every detail of a Question.
On Closed Questions, Answer Option Colours can also be altered.
(NOTE: At Present, editing a question requires the reselection of its Topics)

---

# Quiz System
## Closed Questions
## Open Questions
## Order Questions
## Hints
## Scoring
## Retaking Quizzes

---

## Question Review
## Past Quizzes

---

## Leaderboards
