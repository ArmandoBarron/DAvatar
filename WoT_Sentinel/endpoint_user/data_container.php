<?php
$servername = "localhost";
$username = "root";
$password = "secret";
$dbname = "scheme_info";
$port = "33060";

$conn = new mysqli($servername, $username, $password, $dbname, $port);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT * FROM containers WHERE id_container = '1ccc55a3f77e'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        $str = str_replace("'",'"',$row["td_scheme"]);
        $str = str_replace('\\', '',$str);
        //json_decode($data)
        echo ($str);
    }
}

$conn->close();


$myfile = fopen("newfile.txt", "w") or die("Unable to open file!");
fwrite($myfile, $str);
fclose($myfile);

?>