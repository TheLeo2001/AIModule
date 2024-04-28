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
            }
        });
    }
});
