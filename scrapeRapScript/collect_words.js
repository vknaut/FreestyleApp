/*Creative Commons Attribution-ShareAlike (CC BY-SA)*/


/*
    LISTEN TO CHANGES IN WORD CONTAINER.
        USE WITH THE NEW WORD BUTTON
 */

var collectedWords = [];

function observeWordChanges() {
    var wordContainer = document.getElementById('word');

    // Callback function to execute when mutations are observed
    var callback = function(mutationsList, observer) {
        for(var mutation of mutationsList) {
            if (mutation.type === 'childList' || mutation.type === 'characterData') {
                var newWord = wordContainer.innerText.trim();
                // Check if the new word is not already in collectedWords to avoid duplicates
                if (!collectedWords.includes(newWord)) {
                    collectedWords.push(newWord);
                    if (collectedWords.length % 50 === 0) {
                        console.log("Collected words: ", collectedWords.length);
                    }                // Add any additional logic you need for newWord here
                }
            }
        }
    };

    var observer = new MutationObserver(callback);
    var config = { childList: true, characterData: true, subtree: true };

    // Start observing
    observer.observe(wordContainer, config);

    // Use this function to later stop observing
    function disconnectObserver() {
        observer.disconnect();
    }

    return disconnectObserver;
}

// start observing call
var stopObserving = observeWordChanges();

// Use stopObserving() when you want to stop.




/**
 * Function to click new word
 */
function clickButtonAtInterval(buttonId, interval) {
    // Find the button by its ID
    const button = document.getElementById(buttonId);

    // Check if the button exists
    if (!button) {
        console.error('Button with ID "' + buttonId + '" not found.');
        return;
    }

    // Set up the interval to click the button
    const intervalId = setInterval(() => {
        console.log('Clicking button:', buttonId);
        button.click();
    }, interval);

    console.log('Interval set up. To stop, use: clearInterval(' + intervalId + ');');

    // Return the interval ID so it can be cleared outside this function
    return intervalId;
}

// Example usage: 
var wordPollingInterval = clickButtonAtInterval('wordButton', 50);




/**
 * 
 * Downloads the updated list of words and log the count of new unique words
 */
function promptForExistingFile() {
    var fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.style.display = 'none';
    fileInput.onchange = function(e) {
        var file = e.target.files[0];
        if (file) {
            var reader = new FileReader();
            reader.onload = function(e) {
                var existingWords = e.target.result.split('\n').map(function(word) {
                    return word.trim();
                }).filter(function(word) {
                    return word.length > 0;
                });
                // Combine + remove duplicates
                var combinedWords = Array.from(new Set([...existingWords, ...collectedWords]));
                downloadUpdatedList(combinedWords, existingWords.length);
            };
            reader.readAsText(file);
        }
    };
    document.body.appendChild(fileInput);
    fileInput.click();
    document.body.removeChild(fileInput);
}

function downloadUpdatedList(words, existingWordCount) {
    clearInterval(wordPollingInterval); // Stop collecting 
    var newUniqueWordsCount = words.length - existingWordCount;
    console.log(`${newUniqueWordsCount} new unique words have been collected.`);
    words.sort();
    var textToSave = words.join("\n");
    var blob = new Blob([textToSave], {type: "text/plain"});
    var url = URL.createObjectURL(blob);
    var downloadLink = document.createElement('a');
    downloadLink.href = url;
    downloadLink.download = 'UpdatedWordsList.txt';
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
    URL.revokeObjectURL(url);
    collectedWords = []; // Reset collectedWords
}

promptForExistingFile();





// old timed logic

// var collectedWords = [];
// // Start collecting with 2-second interval
// var wordPollingInterval = setInterval(function() {
//     var currentWord = document.getElementById('word').innerText;
//     if (!collectedWords.includes(currentWord)) {
//         collectedWords.push(currentWord);
        
//         if (collectedWords.length % 50 === 0) {
//             console.log("Collected words: ", collectedWords.length);
//         }
//     }
// }, 2000);
