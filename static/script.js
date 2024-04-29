// static/script.js

$(document).ready(function() {
    $("#send-btn").click(function() {
        sendMessage();
    });

    $("#user-input").keypress(function(event) {
        if (event.which == 13) {
            sendMessage();
        }
    });

    $("#voice-input").click(function() {
        startVoiceInput();
    });

    $("#speak-btn").click(function() {
        speakTranslation();
    });

    function sendMessage() {
        var userMessage = $("#user-input").val();
        if (userMessage.trim() !== "") {
            $("#chat-box").append("<div class='chat-message'><p class='user-message'>" + userMessage + "</p></div>");
            $("#user-input").val("");
            sendUserMessage(userMessage);
        }
    }

    function sendUserMessage(message) {
        $.ajax({
            type: "POST",
            url: "/chat",
            data: { user_message: message },
            success: function(response) {
                $("#chat-box").append("<div class='chat-message'><p class='bot-message'>" + response + "</p></div>");
                if (response.includes("translation of")) {
                    $("#speak-btn").show();
                    $("#speak-btn").attr("data-translation", response.split("is '")[1].split("'")[0]);
                    detectTargetLanguage(response.split(" in ")[1].split(" is")[0]);
                } else {
                    $("#speak-btn").hide();
                }
            }
        });
    }

    function startVoiceInput() {
        $("#user-input").val("Listening...");
        $.ajax({
            type: "POST",
            url: "/voice",
            success: function(response) {
                $("#user-input").val(response);
                sendMessage();
            }
        });
    }

    function speakTranslation() {
        var translation = $("#speak-btn").attr("data-translation");
        var targetLanguage = $("#speak-btn").attr("data-target-language");
        var langCode = targetLanguage;
        var utterance = new SpeechSynthesisUtterance(translation);
        utterance.lang = langCode;
        window.speechSynthesis.speak(utterance);
    }
    

    
});
