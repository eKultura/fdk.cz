<?php
### ### ###  ### ### ###  ### ### ###
### ### ###   Universal   ### ### ###
### ### ###   includes    ### ### ###
session_start();
include './includes/db_connection.php';
include './includes/settings.php';
include './includes/functions.php';
include './assets/languages.php';

/*  
// ROUTES doesn't work
$routes = include "./assets/routes.php";

if (isset($routes[$language][$urlParameter])) {
    $targetPath = $routes[$language][$urlParameter];
} else {
    // default redirect if URL parameter not found
    $targetPath = $routes[$language]['index'];
}

// perform the redirect
header("Location: $targetPath", true, 301);
exit();
*/

$translations = include "./assets/translations/$language.php";

if (isset($_GET['lang']) && array_search($_GET['lang'], $languages) !== false) {
    $language = $_GET['lang'];
}
### ### ###  ### ### ###  ### ### ###
### ### ###  / Universal  ### ### ###
### ### ###  / includes   ### ### ###


$error_message = '';

if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['register'])) {
    $name = $_POST['name'] ?? '';
    $email = $_POST['email'] ?? '';
    $password = $_POST['password'] ?? '';
    $date = date('Y-m-d H:i:s');

    $hashed_password = password_hash($password, PASSWORD_DEFAULT);

    try {
        $sql = "INSERT INTO FDK_users (username, password_hash, email, created) VALUES (?, ?, ?, ?)";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$name, $hashed_password, $email, $date]);

        if ($stmt->rowCount() > 0) {
            $_SESSION['user_id'] = $pdo->lastInsertId(); // Ukládáme ID nově vytvořeného uživatele
            $_SESSION['user_name'] = $name; // Ukládáme jméno uživatele pro zobrazení a další použití
            header("Location: ./?success=new");
            exit();
        } else {
            $error_message = $translations['registration_error_registraton'];
        }
    } catch(PDOException $e) {
        if ($e->getCode() == 23000) {
            // Chyba unikátnosti
            $error_message = $translations['registration_error_user_exist'];
        } else {
            $error_message = "Chyba připojení: " . $e->getMessage();
        }
    }
}
?>
<!DOCTYPE html>
<html lang="<?= $language ?>">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title><?php echo $translations['registration_page_title'] ?></title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fdk.cz/assets/style.css" rel="stylesheet">

</head>
<body>



    <?php include "includes/header.php"; ?>



<div class="container mt-5">
    <div class="row">
        <!-- Sidebar -->
        <div class="col-md-3 d-none d-md-block">
            <div class="sidebar-module">
                <!--<h3>Testovací provoz</h3>-->
                <!-- Obsah sidebaru -->
                <?php echo $translations['registration_sidebar_text'] ?>
            </div>
        </div>
        <!-- Obsah -->
        <div class="col-md-9 col-12">



            <main class="form-signin w-100 m-auto text-center mt-1 mb-5">
                <form method="post">
                    <h1 class="h3 mb-3 fw-normal"><?php echo $translations['registration_form_sign_in'] ?></h1>
                    <?php if (!empty($error_message)) echo "<div class='alert alert-danger'>$error_message</div>"; ?>



                <div class="form-floating">
                    <input type="email" class="form-control mb-2" id="floatingInput" placeholder="email" name="email">
                    <label for="floatingInput"><?php echo $translations['registration_form_email'] ?></label>
                </div>
                <div class="form-floating">
                    <input type="text" class="form-control mb-2" id="floatingInput" placeholder="<?php echo $translations['registration_form_name'] ?>" name="name">
                    <label for="floatingInput"><?php echo $translations['registration_form_name'] ?></label>
                </div>
                <div class="form-floating">
                    <input type="password" class="form-control mb-2" id="floatingPassword" placeholder="<?php echo $translations['registration_form_password'] ?>" name="password">
                    <label for="floatingPassword"><?php echo $translations['registration_form_password'] ?></label>
                </div>



                    <button class="btn btn-primary w-100 py-2 mb-3" type="submit" name="register"><?php echo $translations['registration_form_create_account'] ?></button>
                    <a href="./login.php"><?php echo $translations['registration_form_already_have_account_text'] ?></a>
                </form>
            </main>




        </div>
    </div>
</div>



    <?php include "./includes/footer.php" ?>



</body>
</html>
