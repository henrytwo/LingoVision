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

    db.collection("settings").doc('setting').collection('translation_history')
      .orderBy("timestamp", 'desc')
      .limit(10)
      .onSnapshot(function(querySnapshot) {
        var items = [];

        querySnapshot.forEach(function(doc) {
          if (items.length < 10) {
              items.push(doc.data());
          }
        });

        let html = '';

        for (let item in items) {
            let data = items[item];
            console.log(item)

            html += '<div class="border mx-2 greens rounded" style="text-align: left; padding: 10px; margin-bottom: 10px; background-color: #EFEFEF">' +
                (new Date(data['timestamp'] * 1000)).toString() + '<hr/>' +
                '<b>' + data['start_lang'] + ':</b> ' + data['source_text'] + '<hr>' +
                '<b>' + data['end_lang'] + ':</b> ' + data['translated_text'] +
                '</div>'
        }

        $('#scrolly').html(html);
      })
});