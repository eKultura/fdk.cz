<?php


### ### ###  ### ### ###  ### ### ###
# TEMP FILE UNTIL ROUTING WILL WORK #
### ### ###  ### ### ###  ### ### ###



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
            $_SESSION["username"] = $result['username'];
            $_SESSION["user_id"] = $result['user_id'];

            $update_sql = $pdo->prepare("UPDATE FDK_users SET last_login = NOW() WHERE user_id = ?");
            $update_sql->execute([$_SESSION["user_id"]]);
            // Insert activity log
            $log_sql = $pdo->prepare("INSERT INTO FDK_activity_log (user_id, user_action, description, date_time) VALUES (?, ?, ?, NOW())");
            $log_sql->execute([$_SESSION["user_id"], 'User Login', 'User successfully logged in.']);

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
    <link href="https://getbootstrap.com/docs/5.3/assets/css/docs.css" rel="stylesheet">
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
    
    <!--POP OVER -->
    <span class="d-inline-block text-dark" tabindex="0" data-bs-toggle="popover" data-bs-trigger="hover focus" data-bs-content="<?php echo $translations['sign_in_sidebar_text'] ?>">
      <button class="btn border border-white" type="button" disabled=""><h1 class="text-dark">Prihlašení </h1></button>
    </span>

                <?php if (!isset($_SESSION["username"])): ?>
        <form method="post">
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
            <a href="./registrace.php" class="mt-2"><?php echo $translations['sign_in_form_new_user'] ?></a>
        </form>
    
                <?php else: ?>
                    <div class="alert alert-info">Jste již přihlášen/a jako <?= htmlspecialchars($_SESSION["username"]); ?>. <br>
                    <a href="/odhlaseni">Odhlášení</a>. <br><a href="./">Přejít na domovskou stránku.</a></div>
                <?php endif; ?>
    </main>

        </div>
    </div>
</div>



    <?php include "./includes/footer.php" ?>

    <script src="tooltips.js"></script>



</body>
</html>
