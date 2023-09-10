import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

ApplicationWindow {
    width: 400
    height: 500
    visible: true
    title: "Home Page"
    flags: Qt.MSWindowsFixedSizeDialogHint

    // Theme
    Material.theme: Material.Dark
    Material.accent: Material.Orange

    QtObject {
        id: internal

        function isFormValid() {
            return usernameField.text !== "" && serverAddrField.text !== ""
        }

        function showJoinRoom(valid) {
            if (isFormValid()) {
                const component = Qt.createComponent("join_room.qml")
                const win = component.createObject()
                visible = false
                win.show()
            }
        }

        function showCreateRoom(valid) {
            if (isFormValid()) {
                const component = Qt.createComponent("create_room.qml")
                const win = component.createObject()
                visible = false
                win.show()
            }
        }

    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 6
        Item {
            Layout.fillHeight: true
        }
        TextField {
            id: serverAddrField
            width: 300
            text: "localhost"
            selectByMouse: true
            placeholderText: "Enter Server address"
            Layout.fillWidth: true
            Layout.maximumWidth: 500
            Layout.margins: 12
            Layout.alignment: Qt.AlignHCenter
        }
        TextField {
            id: usernameField
            width: 300
            text: ""
            selectByMouse: true
            placeholderText: "Enter your name"
            Layout.fillWidth: true
            Layout.maximumWidth: 500
            Layout.margins: 12
            Layout.alignment: Qt.AlignHCenter
        }
        Button {
            id: joinRoomButton
            text: "Join Room"
            Layout.alignment: Qt.AlignHCenter
            onClicked: internal.showJoinRoom()
        }
        Button {
            id: createRoomButton
            text: "Create Room"
            Layout.alignment: Qt.AlignHCenter
            onClicked: internal.showCreateRoom()
        }
        Item {
            Layout.fillHeight: true
        }
    }
}
