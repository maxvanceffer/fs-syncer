import QtQuick 2.4
import QtQuick.Controls 1.2
import QtQuick.Window 2.2
import QtQuick.Dialogs 1.2
import QtQuick.Layouts 1.2

Item {
    id: dialog

    width: 400

    function create() {
        var options = {
            watch_path: newWatchPath.text,
            server_path: newServerPath.text,
            name: newName.text,
            hostname: newHostname.text,
            accepts: newAccept.text.split(','),
            key: newPrivateKey.text,
            events: eventsMonitor.getEvents(),
            user: newUsername.text
        }

        store.create_channel(options)
        return true
    }

    FileDialog {
        id: folderDialog
        title: "Please choose a folder for monitor"
        folder: shortcuts.home
        selectFolder: true

        onAccepted: {
            console.log("You chose: " + folderDialog.fileUrls)
            newWatchPath.text = folderDialog.fileUrls[0].replace('file://', '')
        }

        onRejected: {
            console.log("Canceled")
        }
    }

    FileDialog {
        id: keyDialog
        title: "Please choose ssh key"
        folder: shortcuts.home
        nameFilters: [ "PEM keys (*.pem)", "Public ssh key (*.pub)" ]
        onAccepted: {
            console.log("You chose: " + folderDialog.fileUrls)
            newPrivateKey.text = folderDialog.fileUrls[0].replace('file://', '')
        }

        onRejected: {
            console.log("Canceled")
        }
    }

    ColumnLayout {
        id: config_layout
        anchors.fill: parent
        anchors.margins: 6

        spacing: 6

        Label {
           text: "Name channel *"
           Layout.fillWidth: true
        }

        TextField {
           id: newName
           Layout.fillWidth: true

           Component.onCompleted: text = channel ? channel.watch_path : ''
        }

        Label {
           text: "Host *"
           Layout.fillWidth: true
        }

        TextField {
           id: newHostname
           Layout.fillWidth: true

           Component.onCompleted: text = channel ? channel.host : ''
        }

        Label {
           text: "User *"
           Layout.fillWidth: true
        }

        TextField {
           id: newUsername
           Layout.fillWidth: true

           Component.onCompleted: text = channel ? channel.user : ''
        }

        Label {
           text: "Monitor path"
           Layout.fillWidth: true
        }

        RowLayout {

            TextField {
                id: newWatchPath
                Layout.fillWidth: true

                Component.onCompleted: text = channel ? channel.watch_path : ''
            }

            Button {
                text: "Select path"
                onClicked: folderDialog.open()
            }
        }

        Label {
           text: "Server path"
           Layout.fillWidth: true
        }

        RowLayout {

            TextField {
                Layout.fillWidth: true
                id: newServerPath

                Component.onCompleted: text = channel ? channel.server_path : ''
            }
        }

        Label {
           text: "Event for monitor"
           Layout.fillWidth: true
        }

        GridLayout {
            id: eventsMonitor

            Layout.fillWidth: true

            Repeater {
                id: repeaterEvents
                model: ListModel {
                    ListElement {name: qsTr("Created");value: "created"; selected: true}
                    ListElement {name: qsTr("Moved");value: "deleted"; selected: true}
                    ListElement {name: qsTr("Deleted");value: "created"; selected: true}
                    ListElement {name: qsTr("Modified");value: "modified"; selected: true}
                    ListElement {name: qsTr("Directory moved");value: "dir_moved"; selected: true}
                }

                delegate: CheckBox {
                    text: name

                    height: 25

                    onCheckedChanged: selected = checked

                    Component.onCompleted: checked = (channel ? channel.has_event(value) : selected)
                }
            }

            function getEvents () {
                var events = []
                for(var i in repeaterEvents.model.count) {
                    if (model.get(i).selected)
                        events.push(model.get(i).value)
                }

                return events
            }
        }

        Label {
           text: "Accept file extensions (regexp comma separated)"
           Layout.fillWidth: true
        }

        TextField {
           id: newAccept
           Layout.fillWidth: true
        }

        Label {
           text: "PEM key (leave empty for default)"
           Layout.fillWidth: true
        }

        RowLayout {

            TextField {
                id: newPrivateKey
                Layout.fillWidth: true
            }

            Button {
                text: "Select path"
                onClicked: folderDialog.open()
            }
        }
    }

    Component.onCompleted: wizard.height = config_layout.height + 100
}