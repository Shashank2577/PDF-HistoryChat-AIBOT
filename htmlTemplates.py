css = '''
<style>
/* Basic chat styles */
.chat-message {
    display: flex;
    margin: 10px 0;
}

.avatar {
    margin: 0 10px;
}

/* Styling for user's message */
.user-message {
    background: #e1e1e1; /* Light gray background for the user's message */
    color: #333; /* Dark text color */
}

.avatar-image {
    background-color: #3498db; /* Blue background for the avatar */
    color: #fff; /* White text color */
    border-radius: 50%;
    width: 40px; /* Adjust the size as needed */
    height: 40px; /* Adjust the size as needed */
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}

.message {
    background: #f1f1f1; /* Light gray background for the message */
    border-radius: 10px;
    padding: 10px;
}

.bot-message {
    background: #3498db; /* Blue background for the bot's message */
    color: #fff; /* White text color */
}

/* Modern message content styles */
.message-content {
    font-family: 'Helvetica Neue', sans-serif; /* Choose a modern font */
    font-size: 16px;
    line-height: 1.4;
}

/* Animation on hover */
.message-content:hover {
    transform: scale(1.05);
    transition: transform 0.3s;
}
</style>

'''

# bot_template = '''
# <div class="chat-message bot">
#     <div class="avatar">
#         <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
#     </div>
#     <div class="message">{{MSG}}</div>
# </div>
# '''

# user_template = '''
# <div class="chat-message user">
#     <div class="avatar">
#         <img src="https://i.ibb.co/rdZC7LZ/Photo-logo-1.png">
#     </div>    
#     <div class="message">{{MSG}}</div>
# </div>
# '''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <div class="avatar-image">
            <span class="avatar-text">AI</span>
        </div>
    </div>
    <div class="message bot-message">
        {{MSG}}
    </div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <div class="avatar-image">
            <span class="avatar-text">You</span>
        </div>
    </div>
    <div class="message user-message">
        {{MSG}}
    </div>
</div>
'''

