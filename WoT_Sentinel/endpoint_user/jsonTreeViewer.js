var wrapper = document.getElementById("wrapper");
/*$.get('data_container.php', function (data) {
    var dataStr = data;
  })*/
var dataStr = '{ "firstName": "Leo", "lastName": "Hinojosa", "phones": ["123-45-67", "987-65-43"]}';
try {
    var data = JSON.parse(dataStr);
} catch (e) {}
var tree = jsonTree.create(data, wrapper);