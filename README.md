<h1>Piabetes</h1>
<h3>Information Retrieval Software For Diabetics</h3>
<p>
This project was designed for my brother, who has type 1 diabetes, but I've released the source here so that anybody can use it. The project was created because whenever we were out and about, we would look up carb information on our phones. Quite often, we would have bad service, and loading 1 page could take 10 minutes. This, combined with having to search repeatedly, made for a long, cold meal. We could usually text, however. This is how Piabetes works. A Raspberry Pi, running at the users home, will be running Piabetes. The user texts a TextMagic number, and Piabetes receives this. It searches Wolfram Alpha for information, and texts it's findings back to the user. This allows the user to get information from the internet, without actually having to connect via 3G or other cellular data service. The whole thing is written in python, making it versatile for non-raspi users. Simply leave it running on a desktop computer that's connected to the internet, and it'll work the same.
</p>
<hr>
<h3>About</h3>
<p>
Piabetes sends several pieces of useful information back whenever you request a food. Let's go ahead and dissect one of these messages.
  <ul>
    <li>
      <h3>The Name</h3>
      <p>This is the name of the food. In the event that information for the food is not available, this label will likely not be included. If you text Piabetes "Crinkle Fries", it will likely return with a certain brand of crinkle fries. This occurs to help clarify what information, and to help you be able to tell if it's correct. Sometimes the reply is a bit vague, such as if you text "Cherry Pie", it may simply return "pie". This is okay, as the information being returned <i>is</i> for cherry pie. If you would <i>really</i> like to make sure, you can request info for another type of pie, and cross check the information. Most likely, as long as the pies are different, the information will be as well.</p>
    </li>
    <li>
      <h3>The Quantity</h3>
      <p>This is the quantity for the information returned. 30 grams of grapes will likely contain more carbs than just 10 grams, and the amount you're looking for can be requested specifically (check <a href = "https://github.com/Martianmellow12/Piabetes/blob/master/Usage.md#send-amounts">this</a> part of the usage page for details). If you do not send a specific quantity, this value may vary from food to food, though the information related to it (carbs, dietary fiber) will be accurate for the quantity. If an "N/A" is received, a specific quantity was most likely omitted, and the food you requested most likely has variable size, such as a fruit. To fix this, enter a quantity, such as "12 gram:banana", or "0.4 lb:apple".</p>
    </li>
    <li>
      <h3>The Carbs</h3>
      <p>This item shows how many carbs in the quantity shown above. This will be accurate to whatever food is listed in the name field. Whenever you're requesting a food, <i>please</i> enter a quantity, as this will make the carb data more accurate. Receiving an "N/A" here most likely means that there wasn't any information on this food, or the requested quantity of this item is not available.</p>
    </li>
    <li>
      <h3>The Dietary Fiber</h3>
      <p>In some cases, diabetics can subtract the amount of dietary fiber in food from the carb count, meaning that if a slice of cake has 20 carbs, but 1 gram of dietary fiber, they would only be administered insulin for 19 carbs. This information is given for exactly that reason. As with carbs, entering a quantity with the request will make this data much more accurate. Receiving an "N/A" here most likely means that there wasn't any information on this food, or the requested quantity of this item is not available.</p>
    </li>
  </ul>
</p>
<h3>Information Retreival Speed</h3>
<p>Retreiving the information from Wolfram Alpha can take some time, even on a fast internet connection. This, combined with the speed of sending texts, can start to slow down the exchange. To combat this, I have Piabetes store all requests for later use, which cuts down the Wolfram request time from 12 seconds to less than 1 second. While theres nothing I can do about texting speed, Piabetes is written to treat TextMagic as a sort of queue. You can send 10 messages to Piabetes before receiving information for the first, and you'll receive info on them all around the same time.<br>
Current Response Time: <b>33 seconds</b><br>
Current Response Time With Library File: <b>18 seconds</b><br>
The speeds will continue to be improved as new versions are optimized and released</p>
<h3>Special Thanks</h3>
<p>I'd like to thank a few people, without whom this project would have died back at v1.0</p>
<ul>
  <li>Tom Dubick, for introducing me to Python and the Raspberry Pi, and for mentoring me in all things code</li>
  <li>Matthew "Oscar" Kersting, my little brother and inspiration for this project</li>
  <li>Dominick Pulsone, who tested the software for me even though it was useless to him (he was the reason I redesigned the query function to work more efficiently)</li>
</ul>
<p>Without these people, Piabetes would just be some unfinished code taking up space on my hard drive</p>
