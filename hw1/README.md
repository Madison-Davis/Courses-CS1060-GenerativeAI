# cs1060-Madison-Davis-hw1

Contributors: 
- Madison Davis (Github Username: Madison-Davis, Email: madisondavis@college.harvard.edu)
- GitHub URL: https://github.com/Madison-Davis/cs1060-Madison-Davis-hw1
- Netlify Deployed URL: https://68ba45a080a874ddccbbc1af--soft-gecko-30aa8a.netlify.app/
- I did not use Bolt for the full-length of the project due to credit limits.  I started with Bolt in class, then used ChatGPT for the majority of my individual work.  Therefore, I do not have a Bolt URL (this is fine as per Ed post #4).
- If you would like to preview the repo on Bolt, here are the steps!
    - On Bolt.new, import the the repository https://github.com/Madison-Davis/cs1060-Madison-Davis-hw1
    - Prompt bolt to install npm install so you can run react-scripts.
    - Then, tell Bolt to (1) navigate to the adorable-dogs-app folder in the repository, if not there already, and (2) run npm start.  If Bolt is having file-path issues getting there, then just manually use Bolt's terminal at the bottom to do the same steps.
    - Look at the preview tab for the end-result.
    - DO NOTE!  I'd recommend using Chrome.  On Safari, Bolt runs into some extra security issues that sometimes won’t allow images from APIs to load.  So if you load the repo onto Bolt with Safari and see images as question marks, it’s due to their security measure on Cross-Origin-Resource-Policy.  Chrome bypasses this.  It’s not necessarily a bug, but just something to be aware of.

Work Description:
- I worked on the second option for the Assignment: a service built on top of a public API.  Here, I created a web browser app through React that makes pretend profiles of dogs.  To increase the complexity from class examples, I incorporate two APIs: RandomUserAPI and Dog CEO API.  The idea of the app was to browse through fake profiles (not real people's pets, for privacy reasons) of dogs with information such as images and name data, and be able to like their profiles.  Think of it like a cuter version of social media for dogs!  It's inspired from my volunteer work in pet shelters.
- I started initially with a few prompts from Bolt and then into GPT to get a rough outline of the page (the banner, side-bar, and main menu page).  From there, I did additional steps to improve the CSS styling by creating animations, gradient-colorations for a more aesthetic appeal, custom stylings of text, and better-margined image displays).  Finally, I extrapolated off of some of the initial work given from the model.  For example, I altered the region nomenclature that dogs could be assigned to and used mapping functions to allow the display quantity to be easily adjusted in code.

Issues Encountered: 
- I ran into dependency issues.  Sometimes the model would utilize the newest and latest versions, such as tailwind and React, that are considered to be volatile and not compatible with all the old information.  It required downgrades at times and for me to switch to easier dependencies.
- For Netlify, I ran into build issues where I did not specify the proper path.  Moreover, I because the AI gave me code that had to be in a specific ordering for the useEffect function in React, I had some errors where components were used before they were defined.


Hours To Complete: 4

<br><br>
Here is what it looks like in Bolt:
<br><br>
<img width="1531" height="945" alt="Screenshot 2025-09-08 at 10 08 48 AM" src="https://github.com/user-attachments/assets/12ada0be-03a9-46eb-a01d-cdb3bbb6ab62" />

<br><br><br>
Here is what it looks like in Netlify:
<br><br>
<img width="1536" height="808" alt="Screenshot 2025-09-04 at 10 18 45 PM" src="https://github.com/user-attachments/assets/e847abd5-c763-4032-bfee-cd8a89e39231" />

https://github.com/user-attachments/assets/d973d1a3-e2ca-4120-851e-b5c9b901b7b0



