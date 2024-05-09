<?php


### ### ###  ### ### ###  ### ### ###
# TEMP FILE UNTIL ROUTING WILL WORK #
### ### ###  ### ### ###  ### ### ###



session_start();

if (isset($_SESSION["user_name"])) {
    header("Location: ./"); // Redirect to home if already logged in
    exit;
}
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


$chyba = '';

if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["login"])) {
    $loName = $_POST["name"] ?? '';
    $loPassword = $_POST["password"] ?? '';

    $sql = $pdo->prepare("SELECT * FROM FDK_users WHERE username = ? LIMIT 1");
    $sql->execute([$loName]);
    $result = $sql->fetch();

    if ($result) {
        $hashed_password = $result['password_hash'];
        if (password_verify($loPassword, $hashed_password)) {
            $_SESSION["user_name"] = $result['username'];
            $_SESSION["user_id"] = $result['user_id'];

            header("Location: ./");
            exit;
        } else {
            $error_message = $translations['sign_in_error_incorrect_login_information'];
        }
    } else {
        $error_message =  $translations['sign_in_error_user_not_found'];
    }
}
?>
<!DOCTYPE html>
<html lang="<?= $language ?>">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title><?php echo $translations['sign_in_page_title'] ?></title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

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
                <?php echo $translations['sign_in_sidebar_text'] ?>
            </div>
        </div>
        <!-- Obsah -->
        <div class="col-md-9 col-12">

    <main class="form-signin w-100 m-auto text-center mt-1 mb-5">
        <form method="post">
            <h1 class="h3 mb-3 fw-normal">Sign in</h1>

        <?php if (!empty($error_message)) echo "<div class='alert alert-danger'>$error_message</div>"; ?>

            <div class="form-floating">
                <input type="text" class="form-control mb-2" id="floatingInput" placeholder="name@example.com" name="name" required>
                <label for="floatingInput"><?php echo $translations['sign_in_form_name'] ?></label>
            </div>

            <div class="form-floating">
                <input type="password" class="form-control mb-2" id="floatingPassword" placeholder="<?php echo $translations['sign_in_form_password'] ?>" name="password" required>
                <label for="floatingPassword"><?php echo $translations['sign_in_form_password'] ?></label>
            </div>

            <?php if (!empty($chyba)): ?>
                <div class="alert alert-danger mt-2 mb-2"><?= $chyba; ?></div>
            <?php endif; ?>

            <button class="btn btn-primary w-100 py-2 mb-3" type="submit" name="login"><?php echo $translations['sign_in_form_button'] ?></button>
            <a href="./registrace" class="mt-2"><?php echo $translations['sign_in_form_new_user'] ?></a>
        </form>
    </main>

        </div>
    </div>
</div>



    <?php include "./includes/footer.php" ?>



</body>
</html>
