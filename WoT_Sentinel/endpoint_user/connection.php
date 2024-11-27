<?php
$servername = "db_service";
$username = "root";
$password = "secret";
$dbname = "scheme_info";
$port = 3306;

$conn = new mysqli($servername, $username, $password, $dbname, $port);

if ($conn->connect_error) {
    die("Connection failed!!!!!!!!: " . $conn->connect_error);
}

?>