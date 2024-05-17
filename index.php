<?php
session_start();
// ### ### ###  ### ### ###  ### ### ###
// ### ### ###   INCLUDES   ### ### ###
// ### ### ###  ### ### ###  ### ### ###
include './includes/db_connection.php';
include './includes/settings.php';
include './includes/functions.php';

//$routes = include "./assets/routes.php";

include './assets/languages.php';
$translations = include "./assets/translations/$language.php";

if (isset($_GET['lang']) && array_search($_GET['lang'], $languages) !== false) {
    $language = $_GET['lang'];
}
// ### ### ###  ### ### ###  ### ### ###
// ### ### ###  / INCLUDES   ### ### ###
// ### ### ###  ### ### ###  ### ### ###

$welcome_message = '';
$welcome_message_new_user = '';
if (isset($_GET['success']) && $_GET['success'] == 'new') {
    $welcome_message_new_user = "<div class='alert alert-success' role='alert'>Vítejte na našem webu! Vaše registrace byla úspěšná.</div>";
}
if (isset($_GET['success']) && $_GET['success'] == 'logout') {
    $welcome_message_new_user = "<div class='alert alert-success' role='alert'>Odhlášení bylo úspěšné.</div>";
}

if (isset($_SESSION["username"])) {
    $username = $_SESSION["username"];
    $welcome_message = "Vítejte, <strong>$username</strong>! Jsme rádi, že jsi tu.";
} else {
    $welcome_message = "Vítejte na našem webu! Pro plný přístup prosím <a href='./prihlaseni.php'>přihlaste se</a> nebo <a href='./registrace'>vytvořte účet</a>.";
}

//navbar logout 
if(array_key_exists('logout', $_POST))
{
   unset($_SESSION['username']);
   header("Location: ?");
}

?>
<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo $translations['index_title'] ?></title>
    <!-- BOOTSTRAP -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://getbootstrap.com/docs/5.3/assets/css/docs.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

    <link href="https://fdk.cz/assets/style.css" rel="stylesheet">
    <link rel="stylesheet" href="css/index.css">
    </head>
<body>

<div id="sidebar">
    <h3>Navigácia</h3>
    <a class="sidebar-link" href="#welcome-message">Úvod</a>
    <a class="sidebar-link" href="./add-task.php">Pridať úlohy</a>
    <a class="sidebar-link" href="#all-categories">Všetky kategórie</a>
    <a class="sidebar-link" href="#all-tasks">Všetky úlohy</a>
</div>

<div id="main-content">
    <?php include "includes/header.php"; ?>

    <div id="welcome-message">
        <?php echo $welcome_message; ?>
        <?php echo $welcome_message_new_user; ?>
    </div>

  

    <!-- ALL CATEGORIES -->
    <h1 id="all-categories" class="text-center" id="task-header">Všetky kategórie</h1>
    <div class="categories">
        <div class="category text-center">
            <img src="https://img.freepik.com/free-vector/computer-programming-camp-abstract-concept-illustration_335657-3921.jpg?w=740&t=st=1715671724~exp=1715672324~hmac=641e20463145d796f8ba48cfc3aac38ffa0d71cd01d7c3e5630413d3e9248a38" width="100px" alt="">
            <p>frontend</p>
        </div>
        <div class="category text-center">
            <img src="https://img.freepik.com/free-vector/desktop-smartphone-app-development_23-2148683810.jpg?t=st=1715686938~exp=1715690538~hmac=4b6bc30ed1434d9b80921d5ca010e1a8db5039fa02cbb877d14ea8c3ccbf184d&w=740" width="100px" alt="">
            <p>backend</p>
        </div>
        <div class="category text-center">
            <img src="https://img.freepik.com/free-vector/reading-news-latest-world-events-breaking-stories-comments-issues-girl-reading-internet-article-smartphone-device-social-media-concept-illustration_335657-2076.jpg?w=740&t=st=1715687158~exp=1715687758~hmac=8df62e7c61943e8b8afb8caeb91b59d10b6c743b6fd3bd0e4ce6c28ec12d2b06" width="100px" alt="">
            <p>ios</p>
        </div>
        <div class="category text-center">
            <img src="https://img.freepik.com/free-vector/bug-fixing-software-testing-computer-virus-searching-tool-devops-web-optimization-antivirus-app-magnifier-cogwheel-monitor-design-element_335657-2640.jpg?t=st=1715687081~exp=1715690681~hmac=ca3353a7f6d179ef8296b67253f46b9697e0a41020e5c5cfcf2be253d956b1d4&w=740" width="100px" alt="">
            <p>testing</p>
        </div>
    </div>

    <!-- ALL TASKS -->
    <div id="all-tasks" class="ukoly">
        <div class="ukol text-center">
            <!-- kategoria -->
            <img src="https://img.freepik.com/free-vector/computer-programming-camp-abstract-concept-illustration_335657-3921.jpg?w=740&t=st=1715671724~exp=1715672324~hmac=641e20463145d796f8ba48cfc3aac38ffa0d71cd01d7c3e5630413d3e9248a38" width="auto" alt="">
            <p><b>Vylepšiť frontend</b></p>
            <p>Martin -> Tristan</p>
            <p>vysoká</p>
            <p>Prebieha</p>
        </div>
    </div>

    <?php include "./includes/footer.php"; ?>
    <
