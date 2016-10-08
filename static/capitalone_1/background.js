//Sending to popup
var myURL = 'aaa';

//Sending data to content script

var options = {
type: "basic", 
title: "My first popup",
message: "Cool",
iconUrl: "logo.png"
};

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    console.log(sender.tab ?
                "from a content script:" + sender.tab.url :
                "from the extension");
	  
	 if(sender.tab.url.indexOf("amazon") !== -1){
		 options.title = "Upcoming payment for Amazon Prime";
		 options.message = "You will be charged $59.99 on Jan 12."
	 }
	 if(sender.tab.url.indexOf("spotify") !== -1){
		 options.title = "Upcoming payment for Spotify Premium";
		 options.message = "You will be charged $9.99 on Oct 8."
	 }		
	  	  

chrome.notifications.create(options, callback);

function callback(){
	
}
	  
	  
	  
    if (request.greeting == "hello")
      sendResponse({farewell: "goodbye"});
	  
	  
	  
	  
	  
	  
  });