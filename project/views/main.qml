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

    ColumnLayout {
        anchors.fill: parent
        spacing: 6
        Item {
            Layout.fillHeight: true
        }
        TextField {
            id: username
            width: 300
            text: ""
            selectByMouse: true
            placeholderText: "Enter your name"
            Layout.fillWidth: true
            Layout.margins: 12
        }
        Button {
            text: "Join Room"
            Layout.alignment: Qt.AlignHCenter
        }
        Button {
            text: "Create Room"
            Layout.alignment: Qt.AlignHCenter
        }
        Item {
            Layout.fillHeight: true
        }
    }
}
