<?php

$servername = "46.28.109.13";
$username = "div_tristan";
$password = "div_@85ax987+258xi_fdk";
$dbname = "fdkDB";
$port = 3306;

$dsn = "mysql:host=$servername;port=$port;dbname=$dbname";
try {
    $pdo = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
   // echo "Connection failed: " . $e->getMessage();
}

?>
