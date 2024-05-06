<?php

$language = 'cs';

include './assets/languages.php';

if (isset($_GET['lang']) && array_search($_GET['lang'], $languages) !== false) {
    $language = $_GET['lang'];
}

?>
