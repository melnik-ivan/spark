const USER_STYLE = 'button';
const USER_SELECTED_STYLE = 'button selected';
const MY_MESSAGE_STYLE = 'my-message';
const WS_HOST = 'ws://192.168.100.7:8888/ws';


function handleError(error) {
    //ToDo: real handleError
    console.error(error)
}


function removeElement(list, index) {
    let partOne = list.slice(0, index);
    let partTwo = list.slice(index+1);
    return partOne.concat(partTwo);
}

class User {
    constructor(messenger, options, viewClass=UserView) {
        this.name = options.name;
        this.view = new viewClass(messenger, this);
    }

    display() {
        this.view.display();
    }

    hide() {
        this.view.hide();
    }

    select() {
        this.view.select();
    }

    deselect() {
        this.view.deselect();
    }
}


class Message {
    constructor(messenger, options, viewClass=MessageView) {
        this.sender = options.sender;
        this.recipient = options.recipient;
        this.time = options.time;
        this.content = options.content;
        this.view = new viewClass(messenger, this);
    }
    updateView(selectedUser, currentUser) {
        //ToDo: remove these crutches
        const selectedUserIsSender = selectedUser === this.sender;
        const selectedUserIsRecipient = selectedUser === this.recipient;
        const currentUserIsSender = currentUser === this.sender || this.sender === 'echo';
        const currentUserIsRecipient = currentUser === this.recipient;
        const showMessage = selectedUserIsSender && currentUserIsRecipient || currentUserIsSender && selectedUserIsRecipient;
        if (showMessage) {
            if (this.view.widget === false){
                this.view.display();
            }
        } else {
            if (this.view.widget !== false) {
                this.view.hide();
            }
        }
    }

    display() {
        this.view.display();
    }

    hide() {
        this.view.hide();
    }
}


class UserView {
    constructor(messenger, user) {
        this.user = user;
        this.messenger = messenger;
        this.widget = false;
    }

    display() {
        if (this.widget === false) {
            this.widget = document.createElement('button');
            this.widget.innerHTML = this.user.name;
            this.widget.className = USER_STYLE;
            this.widget.onclick = this.onClick();
            document.getElementById('users').appendChild(this.widget);
        } else {
            handleError('User already displayed.');
        }
    }

    hide() {
        if (this.widget !== false) {
            this.widget.remove();
            this.widget = false;
        } else {
            handleError('It is not possible to hide the user who is not displayed.');
        }

    }

    select() {
        if (this.widget !== false) {
            this.widget.className = USER_SELECTED_STYLE;
        } else {
            handleError('It is not possible to select the user who is not displayed.')
        }
    }

    deselect() {
        if (this.widget !== false) {
            this.widget.className = USER_STYLE;
        } else {
            handleError('It is not possible to deselect the user who is not displayed.')
        }
    }

    onClick () {
        return this.messenger.onClickUser(this.user);
    }
}


class MessageView {
    constructor(messenger, message) {
        this.message = message;
        this.messenger = messenger;
        this.template = `
            <div class="message block">
              <div class="header">
                <label>sender:</label>
                <p class="sender">` + this.message.sender.name + `</p>
                <p class="time">` + this.message.time + `</p>
              </div>
              <p class="content">` + this.message.content + `</p>
            </div>
        `;
        this.widget = false;
    }

    display() {
        if (this.widget === false) {
            this.widget = document.createElement('li');
            if (this.message.sender === this.messenger.getCurrentUser()) {
                this.widget.className = MY_MESSAGE_STYLE;
            }
            this.widget.innerHTML = this.template;
            document.getElementById('messages').appendChild(this.widget);
          } else {
            handleError('Message already displayed.')
        }
    }

    hide() {
        if (this.widget !== false) {
            this.widget.remove();
            this.widget = false;
        } else {
            handleError('It is not possible to hide a message that is not displayed');
        }

    }
}


class Messenger {
    constructor(currentUserOptions, userClass=User, messageClass=Message) {
        this.userClass = userClass;
        this.messageClass = messageClass;
        this.currentUser = new userClass(this, currentUserOptions);
        this.currentUser.display();
        this.selectedUser = this.currentUser;
        this.messagePool = [];
        this.selectUser(this.currentUser);
        this.userPool = [this.currentUser];
    }

    getCurrentUser() {
        if (this.currentUser === false) {
            handleError('No user specified.');
        }
        return this.currentUser;

    }

    addUser(userOptions) {
        let user = new this.userClass(this, userOptions);
        user.display();
        this.userPool.push(user);
    }

    removeUser(user) {
        if (user === this.selectedUser) {
            this.selectUser(this.getCurrentUser());
        }
        user.hide();
        this.userPool = removeElement(this.userPool, this.userPool.indexOf(user));
    }

    selectUser(user) {
        this.selectedUser.deselect();
        this.selectedUser = user;
        this.selectedUser.select();
        this.updateDisplayedMessages();
    }

    onClickUser(user) {
        let messenger = this;
        let onUser = user;
        return () => {
            messenger.selectUser(onUser);
        }
    }

    addMessage(messageOptions) {
        let message = new this.messageClass(this, messageOptions);
        this.messagePool.push(message);
        this.updateDisplayedMessages();
    }

    updateDisplayedMessages() {
        let selectedUser = this.selectedUser;
        let currentUser = this.currentUser;
        this.messagePool.map(
            message => {
                message.updateView(selectedUser, currentUser)
            }
        )

    }
}