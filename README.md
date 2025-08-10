# QuizGameV3

So I may've started this in December, maybe January, but I've had to deal with Assignments, other Things I like working on, my oversized Garden, and sleeping. That is an incomplete list.<br/>
Anyway, now it's July, and I've gotten to making good progress.<br/>

<br/>(I've also decided that I can make this in a different, better way, that I'll do after I've finished this version so that I have a basis to work off for that)<br/>

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
## Guest Accounts
These don't function yet, these will be added closer to the end of development, as I'm thinking of limiting Guest Accounts to only being able to do Quizzes.<br/>
I also consider this a Low Priority Feature.

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
**NOTE**: Order Question Hints aren't yet functional, but do cost points
**NOTE**: If the Player doesn't use the standard 1-x Consecutive Indexing (ie 1-2-3-4-...), the System will break, and you won't be able to continue the quiz. This will be patched at some point.
## Image Questions
**HALF IMPLEMENTED**<br/>
I've decided I'm not adding these til I'm done with all the first 2 types of questions, and til the quiz and all related things work.<br/>
It is possible to create and edit Image Questions, however they will be unusable in the Quiz, as the Toggle to include them, like with Order Questions, is disabled.<br/>
May replace these with Audio Questions so I don't have to make design modifications to the page, or just not include either all together

---

# Hints
## Text Hints
## Closed Question Hint: 50/50
## Open Question Hint: Provide Word
## Order Question Hint: Place One

---

## Question Creation
## Question Editing

---

# Quiz System
## Closed Questions
## Open Questions
## Order Questions
## Hints
## Scoring
## Question Review
