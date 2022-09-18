$(document).ready(() => {
    let app = firebase.app();
    var db = firebase.firestore();

    console.log('Ready!');
    db.collection("settings").doc("setting")
    .onSnapshot(function(doc) {
        let data = doc.data();

        $('#language_select').val(data['language']);

        console.log("Current data: ", data);
    });

    $('#language_select').change(function () {
        console.log('setting language:', this.value);

        db.collection("settings").doc("setting").set({
            language: this.value
        });
    });
});