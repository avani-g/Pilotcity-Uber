// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';
const api_base = "http://127.0.0.1:5000/getScores/";

//document.addEventListener('DOMContentLoaded',Login);

let GetURL = document.getElementById('GetURL');



/*
chrome.storage.sync.get('color', function(data) {
  changeColor.style.backgroundColor = data.color;
  changeColor.setAttribute('value', data.color);
});*/


//GetURL.onclick = function(element) {
//  getCurrentTabUrl();
//};

//document.getElementById('getText').onclick = function(element) {
//  chrome.tabs.executeScript( {
//  code: "window.getSelection().toString();"
//}, function(selection) {
//
//  document.getElementById("selectedtext").innerHTML = selection[0];
//});
//};

function modifyDOM() {
        //You can play with your DOM here or check URL against your regex
        console.log('Tab script:');
        console.log(document.body);
        document.body.style.background = "blue"
		return true;
    }

document.getElementById('analyzeTextButton').onclick = function(element) {
  chrome.tabs.executeScript( {
  code: "window.getSelection().toString();"
}, function(selection) {
  	fetch('http://127.0.0.1:5000/getScores/'+selection[0]).then(r => r.text()).then(result => {
    // Result now contains the response text, do what you want...
	console.log(result);
    document.getElementById("analyzeTextButton").style.display = 'none';
	document.getElementById("analyzedText").innerHTML = result;

})
});
};

/**
 * Get the current URL.
 *
 * @param {function(string)} callback called when the URL of the current tab
 *   is found.
 */
function getCurrentTabUrl() {

  // Quercy filter to be passed to chrome.tabs.query - see
  // https://developer.chrome.com/extensions/tabs#method-query
  
  var queryInfo = {
    active: true,
    currentWindow: true
  };  
  chrome.tabs.query(queryInfo, (tabs) => {
    // chrome.tabs.query invokes the callback with a list of tabs that match the
    // query. When the popup is opened, there is certainly a window and at least
    // one tab, so we can safely assume that |tabs| is a non-empty array.
    // A window can only have one active tab at a time, so the array consists of
    // exactly one tab.
    var tab = tabs[0];

    // A tab is a plain object that provides information about the tab.
    // See https://developer.chrome.com/extensions/tabs#type-Tab
    var url = tab.url;

    // tab.url is only available if the "activeTab" permission is declared.
    // If you want to see the URL of other tabs (e.g. after removing active:true
    // from |queryInfo|), then the "tabs" permission is required to see their
    // "url" properties.
    console.assert(typeof url == 'string', 'tab.url should be a string');
	
    
	//alert("current url is--" + url);
	document.getElementById('url').innerHTML = url;
	
	
  });

  // Most methods of the Chrome extension APIs are asynchronous. This means that
  // you CANNOT do something like this:
  //
  // var url;
  // chrome.tabs.query(queryInfo, (tabs) => {
  //   url = tabs[0].url;
  // });
  // alert(url); // Shows "undefined", because chrome.tabs.query is async.
}
