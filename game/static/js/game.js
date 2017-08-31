// list of words existing in boggle board, populated in template
var solvedWords = [];

// represents the words the user has found
var userWords = [];

// constant representing number of columns in word bank
var WORDS_PER_ROW = 4;

// amount of milliseconds left in game
var timeRemaining;

// game length (3 min) in milliseconds
var GAME_LENGTH = 3000; // 3 * 60 * 1000;

// the letter tiles of the board
var board = [];

// how often (in milliseconds) the decrement counter loop executes
var REFRESH_INTERVAL = 1000;

// boolean indicating the status of the game
var gamePaused = false;

var score = 0;

$(document).ready(function (){
    // initially Pause is disabled, Start enabled
    $("#pause").prop("disabled", true);

    // populate the score
    $("#score").text("+ " + score);

    $("#submit").click(function (){
        var word = $("#word").val().trim().toLowerCase();
        
        if (isValidWord(word)){
            // add to user's found words, update table
            userWords.push(word);

            // clear the textbox
            $("#word").val("");

            // set textbox background to normal color
            $("#word").css("background-color", "#fff");

            addToTable(word);
            updateScore(word);

            $("#score").text("+ " + score);
        }
        else {
            // turn the textbox background to light red
            $("#word").css("background-color", "#ffb2b2")
        }
    });

    $("#start").click(function (){
        gamePaused = false;

        $("#start").prop("disabled", true);
        $("#pause").prop("disabled", false);

        // reveal the tile characters
        $(".letter").css("visibility", "visible");

        if (timeRemaining == undefined){
            timeRemaining = GAME_LENGTH;

            var timer = setInterval(function (){
                if (!gamePaused){
                    timeRemaining -= REFRESH_INTERVAL;

                    if (timeRemaining >= 0){
                        var minutes = Math.floor((timeRemaining / 1000) / 60);
                        var seconds = Math.floor((timeRemaining / 1000) % 60);

                        $("#timeRemaining").text(minutes + ":" + ((seconds < 10) ? ("0"+seconds) : seconds));
                    }
                    else {
                        // kill timer from running
                        clearInterval(timer);
                        sendGameData();
                    }
                }
            }, REFRESH_INTERVAL);
        }

        $("#word").focus();
    });

    $("#pause").click(function (){
        gamePaused = true;

        $("#pause").prop("disabled", true);
        $("#start").prop("disabled", false);

        // hide the tiles
        $(".letter").css("visibility", "invisible");
    });

    /* Stopped using html <form> because submitting caused page
       to unexpectedly focus on different area. Since <form> isn't
       being used, must catch ENTER key presses in input text 
       and fire Submit button. 
    */
    $("#word").keypress(function (e){
        var key = e.which;
        if (key == 13){ // ENTER key pressed
            $("#submit").click();
        }
    });

    /* Word must exist in solved dictionary of words and not have been found already */
    function isValidWord(word){
        return (solvedWords.indexOf(word) > -1) && (userWords.indexOf(word) == -1);
    }

    /* Add provided word to table of user solved words */
    function addToTable(word){
        word = word.charAt(0).toUpperCase() + word.slice(1);
        table = $("#wordBank").find("tbody");

        var lastRow = table.find("tr").last();
        if (lastRow.find("td").length >= WORDS_PER_ROW){
            // add new row containing 'word'
            table.append($("<tr>").append($("<td>").text(word)));
        }
        else {
            lastRow.append($("<td>").text(word));
        }
    }

    function getBoggleScore(word){
        if (word.length < 3){
            return 0;
        }
        else if (word.length <= 4){
            return 1;
        }
        else if (word.length == 5){
            return 2;
        }
        else if (word.length == 6){
            return 3;
        }
        else if (word.length == 7){
            return 5;
        }
        else {
            return 11;
        }
    }

    function updateScore(word){
        score += getBoggleScore(word);
    }

    function sendGameData(){
        console.log(userWords);
        $.ajax({
            type: "POST",
            url: "gameover",
            data: {
                // break the board down into 4 row variables since django doesn't support 
                // requests with multidimensional lists
                "row0": board[0],
                "row1": board[1],
                "row2": board[2],
                "row3": board[3],
                "words": userWords
            },
            success: function (data){
                console.log("success");
                console.log(data);
                gameOverModal();
            },
            failure: function (data){
                console.log("failure");
                console.log(data);
                gameOverModal();
            },
        });
    }

    function gameOverModal(score, highScore){
        $("#myModal").modal("show");
        var displayText = "";

        if (highScore){
            displayText += "Congratulations! You cracked the High Scores list. Click on the <a href=\"/highscore\">link</a> to view."
            // gather their name here too?
        }
        else {
            displayText += "You finished the game with " + score + " points. Click <a href=\"/game/\">here</a> to play again.";
        }

        $("#gameOverText").append(displayText);
    }

});
