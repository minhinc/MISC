import QtQuick
import QtQuick.Controls

Dialog {
property alias text: ltModal.text
 contentItem: ScrollView {
  Text {
  id: ltModal
  color:"black"
  text: ""
  }
 }
standardButtons: Dialog.Ok | Dialog.Cancel
//closePolicy:Popup.CloseOnEscape
closePolicy:Popup.NoAutoClose
modal:true
}
