//Sending to popup
var myURL = 'aaa';

//Sending data to content script
chrome.runtime.onConnect.addListener(function(port){
  port.postMessage({greeting:"hello"});
});