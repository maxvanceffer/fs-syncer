import QtQuick 2.4
import QtQuick.Controls 1.2
import QtQuick.Window 2.2
import QtQuick.Dialogs 1.2
import QtQuick.Layouts 1.2

import Example 1.0

Window {
    width: 500
    height: 500
    visible: true

    Loader {
        id: channelDialogLoader
        active: false

        property var channel
        property var page: 'initial'

        sourceComponent: Component {
            Dialog {
                id: channelDialog
                width: 400
                height: 400

                contentItem: Wizard {
                    width: channelDialog.width
                    height: channelDialog.height
                    onDone: channelDialogLoader.active = false
                }

                Component.onCompleted: open()
            }
        }
    }

    // Lets pretend this is your ChannelsListing
    ListView {
        id: channelsList
        anchors.fill: parent
        anchors.margins: 6
        model: store.channels

        delegate: Item {
            width: channelsList.width
            height: 60

            property bool isHovered: false

            Rectangle {
                height: 1
                color: "#60646D"
                anchors.bottom: parent.bottom;
                anchors.left: parent.left;
                anchors.right: parent.right
            }

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 6
                spacing: 2

                RowLayout {
                    Text {
                        text: name
                        font.pixelSize: 15
                        font.bold: true

                        Layout.fillWidth: true
                    }

                    Image {
                        id: edit_btn
                        smooth: true
                        opacity: isHovered ? 1 : 0
                        source: 'images/edit.svg'
                        Layout.fillWidth: false
                        Layout.fillHeight: false
                        Layout.preferredWidth: 25
                        Layout.preferredHeight: 25

                        Behavior on opacity {NumberAnimation {duration: 350;}}

                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                channelDialogLoader.active = false
                                channelDialogLoader.page = 'ssh'
                                channelDialogLoader.channel = modelData
                                channelDialogLoader.active = true
                            }
                        }
                    }

                    Image {
                        smooth: true
                        opacity: isHovered ? 1 : 0
                        source: running ? 'images/pause.svg' : 'images/run.svg'
                        Layout.fillWidth: false
                        Layout.fillHeight: false
                        Layout.preferredWidth: 25
                        Layout.preferredHeight: 25

                        Behavior on opacity {NumberAnimation {duration: 350;}}

                        MouseArea {
                            anchors.fill: parent
                            onClicked: running ? modelData.stop() : modelData.start()
                        }
                    }
                }

                RowLayout {
                    spacing: 6
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    Text {
                        text: qsTr("Status:")
                        font.pixelSize: 12
                        font.bold: true
                        lineHeight: 12
                        color: "#60646D"
                    }

                    Text {
                        text: running ? qsTr("Monitoring") : qsTr("Stopped")
                        font.pixelSize: 12
                        lineHeight: 12
                        color: running ? "#2CC990" : "#60646D"
                    }
                }
            }

            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                propagateComposedEvents: true

                onEntered: isHovered = true
                onExited: isHovered = false
            }
        }
    }

    Rectangle {
        id: controls_background
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.leftMargin: -1
        anchors.rightMargin: -1
        anchors.bottomMargin: -1
        anchors.topMargin: -6
        anchors.top: controls.top
        border.width: 1
        border.color: '#D2D7D3'
        color: '#E7E7E7'
    }

    Row {
        id: controls
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: 6
        spacing: 6

        Button {
            text: "Add sync channel"
            onClicked: {
                channelDialogLoader.channel = store.new_channel(store)
                channelDialogLoader.active = true
            }
        }

        Button {
            text: "Start all"
            enabled: store.count > 0
            onClicked: store.start_all()
        }

        Button {
            text: "Stop all"
            enabled: store.count > 0
            onClicked: store.stop_all()
        }
    }
}