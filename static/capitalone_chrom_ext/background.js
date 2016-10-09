//Sending to popup
var myURL = 'aaa';

//Sending data to content script

var options = {
type: "basic", 
title: "My first popup",
message: "Cool",
iconUrl: "logo3.png"
};

var type;
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    console.log(sender.tab ?
                "from a content script:" + sender.tab.url :
                "from the extension");
	  
	 if(sender.tab.url.indexOf("amazon") !== -1){
		 options.title = "Upcoming payment for Amazon Prime";
		 options.message = "You will be charged $59.99 on Jan 12.";
         options.buttons = [{'title': "Unsubscribe"}];
         type = 'amazon'
	 }
	 if(sender.tab.url.indexOf("spotify") !== -1){
		 options.title = "Upcoming payment for Spotify Premium";
		 options.message = "You will be charged $9.99 on Oct 8.";
         options.buttons = [{'title': "Unsubscribe"}];
         type = 'spotify'
	 }		
	  	  
var myNotificationID;
chrome.notifications.create(options, function(id) {
    myNotificationID = id;
});

function callback(){
	
}
    if (request.greeting == "hello")
      sendResponse({farewell: "goodbye"});  
  });

chrome.notifications.onButtonClicked.addListener(function(notifId, btnIdx) {
    // console.log(notifId);
    // console.log(btnIdx);
    // console.log(type);
    // console.log(myNotificationID);
      if(type == "spotify"){
          window.open("https://www.spotify.com/us/account/cancel/");
      }
      if(type == "amazon"){
          window.open("https://www.amazon.com/gp/primecentral?ie=UTF8&*Version*=1&*entries*=0&");
      }
 });